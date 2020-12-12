import ast
import typing
import pprint
import itertools
import statistics
import sys

import astpretty
import astroid.manager
import astroid.nodes
import astroid.node_classes
from pylint.pyreverse import inspector

import astroid.helpers


def extract_methods(
    cls: astroid.nodes.ClassDef,
) -> typing.Tuple[typing.Dict[str, typing.List[str]], typing.Set[str]]:
    """Extracts all methods and attributes of a class, including inherited
    methods.
    For methods, extract all attributes accessed. Skip __init__().
    """
    # Mapping of method name -> attributes accessed
    methods: typing.Dict[str, typing.List[str]] = {}
    # All attributes owned by this class, including inherited attributes,
    # and attributes
    all_attributes: typing.Set[str] = set(cls.instance_attrs)

    for method in cls.mymethods():
        finder = AstSelfFinder()
        finder.visit(method)
        attributes_accessed = set(finder.attr_names_accessed)

        if method.name != "__init__":
            methods[method.name] = attributes_accessed

    return methods, all_attributes


def compute_tcc(cls: astroid.nodes.ClassDef) -> int:
    """Computes the TCC of a class."""
    methods, attributes = extract_methods(cls)

    k = len(methods)
    if k <= 1:
        print(f"TCC: Ignoring class {cls.name} because it has only {k} method")
        return None

    # Contains methods that access a common attribute, i.e CAU
    cau_methods: typing.Set[typing.Tuple[str, str]] = set()
    for method1, method2 in itertools.combinations(methods, 2):
        if methods[method1] & methods[method2]:
            cau_methods.add((method1, method2))
    return len(cau_methods) / (k * (k - 1) / 2)


def compute_lscc(cls) -> typing.Optional[None]:
    methods, attributes = extract_methods(cls)

    l = len(attributes)
    k = len(methods)
    if l == 0 and k == 0:
        print("input error : there is no attribue and method")
        return None
    elif (l == 0) and (k > 1):
        return 0
    elif (l > 0 and k == 0) or k == 1:
        return 1
    else:
        sum = 0
        for attr_name in attributes:
            count = 0
            for method, attrs_accessed in methods.items():
                if attr_name in attrs_accessed:
                    count += 1

            # for method_name in cls.mymethods():
            #     if method_name.name == "__init__":
            #         pass
            #     else:
            #         finder = AstSelfFinder()
            #         finder.visit(method_name)
            #         if attr_name in finder.attr_names_accessed:
            #             count = count + 1
            sum = sum + (count * (count - 1))
        sum = sum / (l * k * (k - 1))
        return sum


class ProjectScore(typing.NamedTuple):
    """Scores of a project"""

    lscc: float
    tcc: float


def compute_project_score(project_path: str) -> ProjectScore:
    """Computes the score for a project.

    Returns:
        A namedtuple with the fields:
            obj.lscc: LSCC score
            obj.tcc:  TCC score
    """
    # Clear Astroid cache so that it always returns the correct result
    astroid.manager.AstroidManager().clear_cache()

    project = inspector.project_from_files([project_path], project_name="the-project")
    linker = inspector.Linker(project, tag=True)
    # We need this to make the linker actually work on the project
    linker.visit_project(project)

    tcc_values = []
    lscc_values = []

    for module in project.modules:
        for statement in module.body:
            if isinstance(statement, astroid.nodes.ClassDef):
                tcc = compute_tcc(statement)
                lscc = compute_lscc(statement)
                print(f"{statement.name} LSCC = {lscc}, TCC = {tcc}")
                tcc_values.append(tcc)
                lscc_values.append(lscc)

    lscc_values = [x for x in lscc_values if x is not None]
    tcc_values = [x for x in tcc_values if x is not None]
    return ProjectScore(
        lscc=statistics.mean(lscc_values or [0]),
        tcc=statistics.mean(tcc_values or [0]),
    )


class AstSelfFinder:
    """Custom AST walker for astroid
    Needed because we don't have an equivalent of ast.walk() or ast.NodeVisitor
    in astroid.
    """

    def __init__(self):
        self.attr_names_accessed = set()

    def visit(self, node: astroid.node_classes.NodeNG):
        if isinstance(node, (astroid.nodes.Attribute, astroid.nodes.AssignAttr)):
            # Detect self.attr_name (read) or self.attr_name = something (write)
            if isinstance(node.expr, astroid.nodes.Name) and node.expr.name == "self":
                # print(f"    Attribute access detected: self.{node.attrname}")
                self.attr_names_accessed.add(node.attrname)

        for child in node.get_children():
            self.visit(child)


# def find_uses_of_self(fn_node) -> typing.List[str]:
#     """Given an AST node representing an instance method, attempts to find names
#     of all instance attributes used by this function.
#     """
#     attr_names = []
# for node in ast.walk(fn_node):
#     # Detect self.attr_name
#     if isinstance(node, astroid.nodes.Attribute):
#         if isinstance(node.value, astroid.nodes.Name) and node.id == "self":
#             print(f"    Attribute access detected: self.{node.attr}")
# return attr_names


def main(project_path: str) -> None:
    print(compute_project_score(project_path))
    # print("Cache id, again:", id(astroid.manager.AstroidManager.brain.astroid_cache))


if __name__ == "__main__":
    main(sys.argv[1])
