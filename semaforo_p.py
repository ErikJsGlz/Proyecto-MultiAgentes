import agentpy as ap
import time as t

# Clase Semáforos para Carros
class Semaforo_Carro(ap.Agent):

    def setup(self):
        # Creamos un agente de tipo Semáforo_Carro
        # 0 = rojo, 1 = verde, 2 = amarillo
        self.status = 1
        # 0 = bocina apagada, 1 = bocina encendida
        self.horn = 0

    def changeStatus(self):
        status = 2
        print(status)
        t.sleep(5)
        status = 0
        t.sleep(5)
        status = 1

    def honk(self):
        self.horn = 1
        t.sleep(7)