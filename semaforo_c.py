import agentpy as ap
import time as t

# Clase Semáforos para Carros
class Semaforo_Carro(ap.Agent):

    def setup(self):
        # Creamos un agente de tipo Semáforo_Carro
        # 0 = rojo, 1 = verde, 2 = amarillo
        self.status = 1

    def changeStatus(self):
        status = 2
        print(status)
        t.sleep(5)
        status = 0
        t.sleep(5)
        status = 1


model = Semaforo_Carro();
Semaforo_Carro.changeStatus()