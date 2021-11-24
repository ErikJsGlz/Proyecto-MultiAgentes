import agentpy as ap
import time as t

# Clase Semáforos para Carros
class SemaforoPeaton(ap.Agent):

    def setup(self):
        # Creamos un agente de tipo Semáforo_Carro
        # 0 = rojo, 1 = verde, 2 = amarillo
        self.status = 1

        # 0 = bocina apagada, 1 = bocina encendida
        self.horn = 0

        # posición
        self.x = 0
        self.y = 0
        self.z = 0

        # tiempos por colores, medida -> seg
        self.timeYlw = 5
        self.timeRed = 7

    # Cambia el estatus de verde, a amarillo a rojo
    def changeStatus(self):
        # Cambia el estatus de verde a rojo
        self.status = 0
        t.sleep(self.timeRed)

        # Vuelve su estado a verde
        self.status = 1

    # Sonamos la alarma y cambiamos el estatus
    def honk(self):
        self.horn = 1
        self.changeStatus()
