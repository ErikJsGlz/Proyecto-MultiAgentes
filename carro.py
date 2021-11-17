import agentpy as ap

#Clase Carro
class Carro(ap.Agent):

    def setup(self):
        self.x = 0
        self.y = 0

    def move_rigth(self, n):
        for i in range(n):
            self.x += 1

    def move_lefth(self, n):
        for i in range(n):
            self.x -= 1
    
    def move_down(self, n):
        for i in range(n):
            self.y -= 1

    def move_up(self, n):
        for i in range(n):
            self.y += 1