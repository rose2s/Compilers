class Stack():

    def __init__(self):
        self.items = []
    # Return true is Empty
    def isEmpty(self):
        return self.items == []

    # Add item into stack
    def push(self, item):
        self.items.append(item)

    # Removes top of stack
    def pop(self):
        return self.items.pop()

    # Returns top of stack
    def peek(self):
        return self.items[len(self.items)-1]

    # Returns size of stack
    def size(self):
        return len(self.items)