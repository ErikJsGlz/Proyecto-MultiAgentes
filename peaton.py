import agentpy as ap

# Clase Peaton
class Peaton(ap.Agent):
    #Peaton 

    def setup(self):
        # Creamos un agente de tipo Peaton
        self.type = 0 # 0 = Sin discapacidad, 1 = con discapacidad
        self.age = 0 # 0 = Adulto, 1 = niño
        self.x = 0
        self.y = 0
        self.z = 0

    def walk(self):
        self.x += 1