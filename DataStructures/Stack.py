class Stack:
    
    def __init__(self, max_size=None):
        self.items = []
        self.max_size = max_size

    def push(self, item):
        if self.max_size is not None and len(self.items) >= self.max_size:
            raise OverflowError("Stack is full")
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def is_full(self):
        if self.max_size is None:
            return False
        return len(self.items) >= self.max_size

    def __iter__(self):
        return reversed(self.items)  # iterate from top to bottom
