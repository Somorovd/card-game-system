from abc import ABC, abstractmethod


class Operation(ABC):
    @abstractmethod
    def eval(self, x):
        pass


class AddOp(Operation):
    def __init__(self, val):
        self.val = val

    def eval(self, x):
        return x + self.val


class MultOp(Operation):
    def __init__(self, val):
        self.val = val

    def eval(self, x):
        return x * self.val


class MaxOp(Operation):
    def __init__(self, val):
        self.val = val

    def eval(self, x):
        return max(x, self.val)


class SetOp(Operation):
    def __init__(self, val):
        self.val = val

    def eval(self, x):
        return self.val
