NEGRO = (0, 0, 0)

CAMINO = (210, 210, 210)
BLANCO = (255,255,255)
ROJO = (210, 0, 0)

GRIS = (160, 160, 160)
TIERRA = (169,79,17)
BOSQUE = (101,227,34)
ARENA = (227,154,34)
AGUA = (34, 154, 227)
class Celda:
    def __init__(self, valor):
        self.inicial = valor
        self.juego = valor
        self.original = valor
        self.mascara = ""
        if valor == "%":
            self.mascara = "%"
        else:
            self.mascara = "X"

    def setJuego(self, valor):
        self.juego = valor
    def setMascara(self, valor):
        self.mascara = valor

    def hardReset(self):
        self.juego = self.inicial
        if self.juego == "%":
            self.mascara = "%"
        else:
            self.mascara = "X"

    def resetOriginal(self):
        self.juego = self.original
        self.mascara = "X"

    def resetVisitado(self):
        self.juego = "V"
        self.mascara = "V"

    def setOriginal(self):
        self.original = self.juego

    def setMascara(self, valor):
        self.mascara = valor

    def setJuego2Mascara(self):
        self.mascara = self.juego

    def __str__(self):
        return str(self.juego)

    def isPlayer(self):
        if self.juego == "P":
            return True
        if self.mascara == "P":
            return True
        return False

    def getColor(self, juego):
        color = NEGRO
        #juego
        if juego == False:
            if self.juego == "0":
                color = GRIS
            elif self.juego == "%":
                color = BLANCO
            elif self.juego == "1":
                color = TIERRA
            elif self.juego == "2":
                color = AGUA
            elif self.juego == "3":
                color = ARENA
            elif self.juego == "4":
                color = BOSQUE
        else:#mascara
            if self.mascara == "0":
                color = GRIS
            elif self.mascara == "1":
                color = TIERRA
            elif self.mascara == "%":
                color = BLANCO
            elif self.mascara == "2":
                color = AGUA
            elif self.mascara == "3":
                color = ARENA
            elif self.mascara == "X":
                color = NEGRO
            elif self.mascara == "4":
                color = BOSQUE
        return color;