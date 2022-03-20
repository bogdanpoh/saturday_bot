
class Switch:
    def __init__(self, value):
        self.value = value

    def case(self, value, code):
        if self.value == value:
            code()
        return self
