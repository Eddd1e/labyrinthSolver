class Nodo:
    def __init__(self, pos, meta, costoA):
        self.valor = pos
        self.costoA = costoA
        self.distanciaM = (abs(pos[0] - meta[0]) + abs(pos[1] - meta[1]))
        self.h = self.costoA + self.distanciaM
        self.estado = "O"
        self.hijos = []

    def equals(self, nodo):
        return self.valor == nodo.valor and self.costoA == nodo.costoA and self.distanciaM == nodo.distanciaM and self.h == nodo.h

    def mejorQue(self, nodo, meta):
        return self.h <= nodo.h and nodo.valor != meta