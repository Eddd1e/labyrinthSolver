def moverJugador(self, x, y):
        if 1 <= self.jugador.x+x <= self.b-1 and y == 0:
            if self.mapa[y][x+x].juego != "0" and self.mapa[y][x+x].juego != "V":
                if self.jugador.movimientos == 0:
                        self.mapa[self.jugador.y][self.jugador.x].juego = "V"
                self.mapa[self.jugador.y][self.jugador.x].juego = "V"
                self.mapa[self.jugador.y][self.jugador.x].mascara = "1"
                self.mapa[self.jugador.y][self.jugador.x+x].mascara = "P"

                self.jugador.x = self.jugador.x + x
                self.jugador.agregarTile()
                self.descubrirAlrededor()
        elif 1 <= self.jugador.y+y <= self.h-1 and x == 0:

            if self.mapa[y+y][x].juego != "0" and self.mapa[y+y][x].juego != "V":
                if self.jugador.movimientos == 0:
                        self.mapa[self.jugador.y][self.jugador.x].juego = "V"  
                self.mapa[self.jugador.y][self.jugador.x].mascara = "1"
                self.mapa[self.jugador.y][self.jugador.x].juego = "V"
                self.mapa[self.jugador.y+y][self.jugador.x].mascara = "P"

                self.jugador.y = self.jugador.y + y
                self.jugador.agregarTile()
                self.descubrirAlrededor()