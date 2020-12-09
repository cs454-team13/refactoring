import astor
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
    
    def __init__(self, fname, src_cls, dst_cls, target):
        super(PushDownMethod, self).__init__(fname, src_cls)
        self.rtype = "PushDownMethod"
        self.dst_cls = dst_cls
        self.target = target

    def create(self):
        super(PushDownMethod, self).create()
        self.dst_cls = findHelper.get_class_from_name(self.refactoredtree, self.dst_cls)
        self.target = findHelper.get_method_from_name(self.src_cls, self.target)

    def apply(self):
        self.create()
        self.src_cls.body.remove(self.target)
        self.dst_cls.body.append(self.target)
        super().write_file()

'''TODO: field-level Refactoring의 경우 class attribute, instance attribute 비교'''

class PullUpField(Refactoring):
    
    def __init__(self, fname, src_cls, target):
        super(PullUpField, self).__init__(fname, src_cls)
        self.rtype = "PullUpField"
        self.target = target

    def create(self):
        super(PullUpField, self).create()
        self.target = findHelper.get_field_from_name(self.src_cls, self.target)

    def apply(self):
        self.create()
        parent = findHelper.find_superclass(self.refactoredtree, self.src_cls)
        self.src_cls.body.remove(self.target)
        parent.body.append(self.target)
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
        self.target = findHelper.get_field_from_name(self.src_cls, self.target)

    def apply(self):
        self.create()
        self.src_cls.body.remove(self.target)
        self.dst_cls.body.append(self.target)
        super().write_file()
    
    
    


