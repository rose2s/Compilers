class List:
    nodeCount = 0
    First = None

    def __init__(self, tokenType, value):
        List.nodeCount += 1
        self.Prior = None                   # Only first Node has Next == None
        self.Next = None                    # Only last  Node has Next == None
        self.Token_type = tokenType    
        self.Token_value = value   

    def getPrior(self):
        return self.Prior

    def setPrior(self, Prior):
        self.Prior = Prior

    def getFirst(self):
        return self.First

    def setFirst(self, node):
        self.First = node

    def getNext(self):
        return self.Next

    def setNext(self,Next):
        self.Next = Next

    def getTokenType(self):
        return self.Token_type

    def getTokenValue(self):
        return self.Token_value

    def getPrior(self):
        return self.Prior

    def getNext(self):
        return self.Next

    def getLastNode(self,node):
        while (node.Next):
            node = node.Next

        return node

    def addNode(self,node,Type,value):
        new = List(Type,value)

        if List.nodeCount > 0:
            last = self.getLastNode(node)
            last.setNext(new)
            new.setPrior(last)

