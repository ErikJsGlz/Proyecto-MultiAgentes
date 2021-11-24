import agentpy as ap
import time as t

# Clase Semáforos para Carros
class SemaforoCarro(ap.Agent):

    def setup(self):
        # Creamos un agente de tipo Semáforo_Carro
        # 0 = rojo, 1 = verde, 2 = amarillo
        self.status = 1

        # Posición
        self.x = 0
        self.y = 0
        self.z = 0

        # tiempos por colores, medida -> seg
        self.timeYlw = 5
        self.timeRed = 7


    def changeStatus(self):
        #Cambia de verde a amarillo
        self.status = 2
        t.sleep(self.timeYlw)

        # Cambia el estatus de rojo
        self.status = 0
        t.sleep(self.timeRed)

        # Vuelve su estado a verde
        self.status = 1