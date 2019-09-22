class Stack(object):
    """
    在 ExamStandard.process_each_seg_by_sliced_targets函数中初始化;
    在遇到 obj, item, pos等不同tag时，分别初始化响应的stack
    """

    def __init__(self):
        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()


class ObjStack(Stack):
    def __init__(self):
        super().__init__()


class PosStack(Stack):
    def __init__(self):
        super().__init__()


class PartStack(Stack):
    def __init__(self):
        super().__init__()


class ExamItemStack(Stack):
    def __init__(self):
        super().__init__()


class ExamResultStack(Stack):
    def __init__(self):
        super().__init__()


def main():
    stack = Stack()
    print(stack.is_empty())
    stack.push("123")
    print("基类stack: ", stack.stack)

    obj_stack = ObjStack()
    print(obj_stack.is_empty())
    obj_stack.push("肝脏")
    obj_stack.push("肾脏")
    print(obj_stack.stack)
    deleted_obj = obj_stack.pop()
    print("删掉[%s]后的obj_stack: %s" % (deleted_obj, obj_stack.stack))


if __name__ == "__main__":
    main()
