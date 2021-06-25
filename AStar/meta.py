class Meta:

    def __init__(self, x, y, opcional):
        self.x = x
        self.y = y
        self.opcional = opcional
        
    def equals(self,x,y):
        return self.x == x and self.y == y
    
    def getPosT(self):
        return (self.x, self.y)