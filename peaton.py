import agentpy as ap

# Clase Peaton
class Peaton(ap.Agent):

    def setup(self):
        # Creamos un agente de tipo Peaton
        self.type = 0 # 0 = Sin discapacidad, 1 = con discapacidad
        self.age = 0 # 0 = Adulto, 1 = niño

        # Posición
        self.x = 0
        self.y = 0
        self.z = 0

    """ 
    Funciones para mover al carro en la calle

    Según Unity, nuestra calle estaría en los ejes x,z
    no nos moveríamos sobre 'y', eso significaría que se elevaría o descendería el carro
    """
    def walk_rigth(self, n):
        for i in range(n):
            self.x += 1

    def walk_left(self, n):
        for i in range(n):
            self.x -= 1
    
    def walk_down(self, n):
        for i in range(n):
            self.z -= 1

    def walk_up(self, n):
        for i in range(n):
            self.z += 1