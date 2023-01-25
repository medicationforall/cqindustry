class Base:
    def __init__(self):
        self.width = 75
        self.length = 75
        self.height = 75
        self.make_called = False

    def make(self):
        self.make_called = True

    def build(self):
        if self.make_called == False:
            raise Exception('Make has not been called')

    def dimensions(self):
        return (self.length, self.width, self.height)
