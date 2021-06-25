    def estrella(self, closed, opened, raiz, index, raizOriginal):
        print(raiz.valor)
        if not self.estaEn(closed, raiz):
            self.raiz.estado = "C"
            self.jugador.mover(raiz.valor[0], raiz.valor[1])
            self.jugador.costoA = raiz.costoA
            closed.append(raiz)
            self.borrarElemento(opened, copy.deepcopy(raiz))
        if raiz.valor == self.metas[index].getPosT():
            print("meta encontrada")
            self.done = True
            return

        raiz.hijos = self.getCaminos(closed, raiz, opened)
        
        if len(opened)>0 and raiz.hijos:
            opened.sort(key=lambda x: (x.h, x.distanciaM, x.costoA))
            mejorOpened = self.find(raizOriginal, opened[0])
            for h in raiz.hijos:
                if not self.estaEn(closed, h) and not self.estaEn(opened, h):
                    opened.append(copy.deepcopy(h))
            try:
                if mejorOpened.mejorQue(raiz.hijos[0]):
                    #print(mejorOpened.valor,mejorOpened.h ," mejor que: ", raiz.hijos[0].valor, raiz.hijos[0].h)
                    if not self.done:
                        self.estrella(closed, opened, mejorOpened, index, raizOriginal)
            except None as e:
                print("ex")
                return
            else:
                for h in raiz.hijos:
                    if not self.done:
                        self.estrella(closed, opened, h, index, raizOriginal)
        else:
            for h in raiz.hijos:
                if not self.estaEn(closed, h) and not self.estaEn(opened, h):
                    opened.append(copy.deepcopy(h))
            for h in raiz.hijos:
                if not self.done:
                    self.estrella(closed, opened, h, index, raizOriginal)



                    def findMejor(self, raiz, nodo):
            resultado = None
        if raiz.h <= nodo.h and raiz.estado == "O":
            return raiz
        for h in raiz.hijos:
            resultado = self.find(h, nodo)
            if resultado !=None:
                break
        return resultado