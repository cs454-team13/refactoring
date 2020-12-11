import ast, astor
import FindHelper as findHelper

class Refactoring:

    def __init__(self, fname, src_cls):
        self.fname = fname
        self.rtype = ""
        self.src_cls = src_cls

    def create(self):
        self.origintree = astor.parse_file(self.fname)
        self.refactoredtree = astor.parse_file(self.fname)
        self.src_cls = findHelper.get_class_from_name(self.refactoredtree, self.src_cls)

    def undo(self):
        with open(self.fname, 'w') as f:
            origin_source = astor.to_source(self.origintree)
            f.write(origin_source)
    
    def write_file(self):
        with open("refactored_{}".format(self.fname), 'w') as f:  # DEBUG
        # with open(self.fname, 'w') as f:
            refactored_source = astor.to_source(self.refactoredtree)
            f.write(refactored_source)

class PullUpMethod(Refactoring):
    
    def __init__(self, fname, src_cls, target):
        super(PullUpMethod, self).__init__(fname, src_cls)
        self.rtype = "PullUpMethod"
        self.target = target

    def create(self):
        super(PullUpMethod, self).create()
        self.target = findHelper.get_method_from_name(self.src_cls, self.target)

    def apply(self):
        self.create()
        parent = findHelper.find_superclass(self.refactoredtree, self.src_cls)
        self.src_cls.body.remove(self.target)
        parent.body.append(self.target)
        super().write_file()

'''TODO: PushDown의 경우 어떤 subclass로 옮길지 정하는 조건문 필요'''

class PushDownMethod(Refactoring):
    
    def __init__(self, fname, src_cls, target):
        super(PushDownMethod, self).__init__(fname, src_cls)
        self.rtype = "PushDownMethod"
        self.target = target

    def create(self):
        super(PushDownMethod, self).create()
        self.target = findHelper.get_method_from_name(self.src_cls, self.target)

    def apply(self):
        self.create()
        self.src_cls.body.remove(self.target)
        subclasses = findHelper.find_subclasses(self.refactoredtree, self.src_cls)
        for subclass in subclasses:
            if findHelper.find_method_in_class(subclass, self.target):
                subclass.body.append(self.target)

        super().write_file()

'''TODO: field-level Refactoring의 경우 class attribute, instance attribute 비교'''
''' instance field만 고려하는걸로'''
class PullUpField(Refactoring):
    
    def __init__(self, fname, src_cls, target):
        super(PullUpField, self).__init__(fname, src_cls)
        self.rtype = "PullUpField"
        self.target = target

    def create(self):
        super(PullUpField, self).create()
        self.target = ast.parse("self.{} = None".format(self.target))

    def apply(self):
        self.create()
        parent = findHelper.find_superclass(self.refactoredtree, self.src_cls)
        parentinit = None
        for node in ast.walk(parent):
            if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                parentinit = node
                break
        if parentinit is not None:
            parentinit.body.append(self.target)
        super().write_file()

class PushDownField(Refactoring):
    
    def __init__(self, fname, src_cls, dst_cls, target):
        super(PushDownField, self).__init__(fname, src_cls)
        self.rtype = "PushDownField"
        self.dst_cls = dst_cls
        self.target = target

    def create(self):
        super(PushDownField, self).create()
        self.dst_cls = findHelper.get_class_from_name(self.refactoredtree, self.dst_cls)
        parentinit = None
        for node in ast.walk(self.src_cls):
            if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                parentinit = node
                break
        if parentinit is not None:
            for node in parentinit.body:
                if isinstance(node, ast.Assign):
                    if isinstance(node.targets[0], ast.Attribute) and isinstance(node.targets[0].value, ast.Name) and node.targets[0].value.id == 'self' and node.targets[0].attr == self.target:
                        self.target = node
                        break

    def apply(self):
        self.create()
        parentinit = None
        for node in ast.walk(self.src_cls):
            if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                parentinit = node
                break
        if parentinit is not None:
            parentinit.body.remove(self.target)
        for node in ast.walk(self.dst_cls):
            if isinstance(node, ast.FunctionDef) and node.name == '__init__':
                parentinit = node
                break
        if parentinit is not None:
            parentinit.body.insert(1, self.target)
        super().write_file()