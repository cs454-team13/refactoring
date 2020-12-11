import ast
import astor

def find_method_in_class(classNode, method):
    for child in ast.walk(classNode):
        if isinstance(child, ast.Call) and isinstance(child.func, ast.Attribute) and child.func.attr == method.name:
            return True
    return False

def find_subclasses(tree, classNode):
    """Find the subclasses of input class.
        Assume the single inheritance

    Args:
        tree:
            AST for a module
            It is made by astor.parse_file()
        classNode:
            It might have subclasses or not.
    Returns:
        return the set of subclasses
        If the classNode doesn't have any subclasses, then return None
    """
    classes = find_all_classes(tree)
    subclasses = []
    for singleClass in classes:
        superclass = find_superclass(tree, singleClass)
        if superclass is None or superclass.name != classNode.name:
            continue
        else:
            subclasses.append(singleClass)
    return subclasses

def find_superclass(tree, classNode):
    """Find the superclass of input class.
        Assume the single inheritance
    Args:
        tree:
            AST for a module
            It is made by astor.parse_file()
        classNode:
            Node of class in the tree
            It might have a superclass or not.
    Returns:
        return the immediate superclass of classNode
        If classNode doesn't have a superclass, then return None
    """
    superclass_name = [superclass.id for superclass in classNode.bases]
    if len(superclass_name) == 0:
        return None
    else:
        return [get_class_from_name(tree, e) for e in superclass_name][0] 

def find_all_classes(astree):
    """Find all classes in input AST.
    Args:
        astree:
            It is made by astor.parse_file()
    Returns:
        return the list of classes
        If there's no any class, then return the empty list
    """
    found_classes = [node for node in ast.walk(astree) if isinstance(node, ast.ClassDef)]
    return found_classes

def find_all_methods(astree):
    """Find all methods in input AST.
    Args:
        astree:
            It is made by astor.parse_file()
    Returns:
        return the list of methods
        If there's no any method, then return the empty list
    """
    found_methods = [node for node in ast.walk(astree) if isinstance(node, ast.FunctionDef) and (node.name.startswith('__') is False)]
    return found_methods

'''TODO: find_all_fields debug'''

def find_all_fields(astree):
    """Find all fields in input AST.
       Assume fields are instance fields
    Args:
        astree:
            It is made by astor.parse_file()
    Returns:
        return the list of fields
        If there's no any field, then return the empty list
    """
    found_fields = set()
    for node in ast.walk(astree):
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Attribute):
                found_fields.add(target)
    # found_fields = [node for node in ast.walk(astree) if isinstance(node, ast.Assign) and  ]
    return found_fields

def get_class_from_name(astree, className):
    classes = find_all_classes(astree)
    found_class = [x for x in classes if x.name == className]
    if len(found_class) > 0:
        return found_class[0]
    else:
        return None

def get_method_from_name(astree, methodName):
    methods = find_all_methods(astree)
    found_method = [x for x in methods if x.name == methodName]
    if len(found_method) > 0:
        return found_method[0]
    else:
        return None

def get_field_from_name(astree, fieldName):
    fields = find_all_fields(astree)
    # TODO: segregate class attribute and instance attribute
    found_field = [x for x in fields if (hasattr(x.targets[0], 'id') and x.targets[0].id == fieldName)]

    # found_field = [x for x in fields if (hasattr(x.targets[0], 'id') and x.targets[0].id == fieldName) or (hasattr(x.targets[0], 'attr') and x.targets[0].attr == fieldName)]
    if len(found_field) > 0:
        return found_field[0]
    else:
        return None