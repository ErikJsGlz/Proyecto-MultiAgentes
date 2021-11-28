import agentpy as ap
from semaforo_c import SemaforoCarro
from semaforo_p import SemaforoPeaton
from carro import Carro
from peaton import Peaton

# Para el tiempo
import time
t = 0
elapsed_time = 0

# Importamos JSON
import json
# Posiciones en formato JSON
posJSON = []
currentPos = {}

class StreetModel(ap.Model):

    def setup(self):
        # Iniciamos el contador de segundos
        global t
        t = time.time()

        self.semaforoActivo = 0

        """ Inicializamos los agentes """
        n_carros = self.p.carros
        self.carros = ap.AgentList(self, n_carros, Carro)

        n_semaforo_carros = self.p.semaforo_carros
        self.semaforo_carros = ap.AgentList(self, n_semaforo_carros, SemaforoCarro)

        n_semaforo_peatones = self.p.semaforo_peatones
        self.semaforo_peatones = ap.AgentList(self, n_semaforo_peatones, SemaforoPeaton)

        n_peatones = self.p.peatones
        self.peatones = ap.AgentList(self, n_peatones, Peaton)


        """ Creamos el grid del cruce """
        size = self.p.size
        self.cruce = ap.Grid(self, [size] * 2, track_empty = True)

        """ Agregamos a los agentes de tipo Carro """
        # Definimos la posición de los agentes dentro del Grid
        self.cruce.add_agents(self.carros, [
            (3, -16), 
            (3, -23),
            (-30, -3),
            (-37, -3)
        ])
        # Definimos la posisición de los carros para mandarlo a Unity
        # Para avanzar[0 - 1] -> z++, [2, 3] -> x++
        x_carro = [3, 3, -30, -37]
        z_carro = [-16, -23, -3, -3]
        for i in range(4):
            self.carros[i].x = x_carro[i]
            self.carros[i].y = 0
            self.carros[i].z = z_carro[i]


        """ Agregamos a los agentes de tipo Semaforos """
        # Lo asignamos en posiciones específicas en el grid
        self.cruce.add_agents(self.semaforo_carros, [
            (-7, 7),
            (7, -7)
        ])
        # Definimos a uno de los semáforos como detenido, o Rojo
        self.semaforo_carros[0].status = 0

        self.cruce.add_agents(self.semaforo_peatones, [
            (-6, -7),
            (6, 7)
        ])
        # Definimos la posición de los semaforo para mandarlo a Unity
        x_semaforo_carro = [-7, 7]
        z_semaforo_carro = [7, -7]
        x_semaforo_peatones = [-6, 6]
        z_semaforo_peatones = [-7, 7]

        for i in range(n_semaforo_carros):
            self.semaforo_carros[i].x = x_semaforo_carro[i]
            self.semaforo_carros[i].y = 0
            self.semaforo_carros[i].z = z_semaforo_carro[i]

            pos = {
                "semaforo_carro" + str(i) + "_x" : x_semaforo_carro[i],
                "semaforo_carro" + str(i) + "_y" : z_semaforo_carro[i]
            }
            currentPos.update(pos)

        for i in range(n_semaforo_peatones):
            self.semaforo_peatones[i].x = x_semaforo_peatones[i]
            self.semaforo_peatones[i].y = 0
            self.semaforo_peatones[i].z = z_semaforo_peatones[i]

            pos = {
                "semaforo_peatones" + str(i) + "_x" : x_semaforo_peatones[i],
                "semaforo_peatones" + str(i) + "_y" : z_semaforo_peatones[i]
            }
            currentPos.update(pos)

        posJSON.append(currentPos)

        ### AÑADIR PEATONES ###

    def step(self): 

        # Reiniciamos el currentPos para iniciar las posiciones de los carros
        currentPos = {}

        print("\n")
        # for i in range(4):
        #     print("Carro " + str(i + 1) + " - Posición: (" + str(self.carros[i].x) + ", " + str(self.carros[i].y) + ", " + str(self.carros[i].z) + ")" )
        


        # Si el semáforo 1 está en verde, entonces avanzan los carros en x, si no avanzan los del eje z
        if (self.semaforo_carros[0].status == 1): 
            for i in range(4):
                if (i == 0 or i == 1):
                    self.carros[i].move_right(1)
        
        else:
            for i in range(4):
                if(i == 2 or i == 3):
                    self.carros[i].move_up(1)
    
        # Definimos la posición actual de los carros en un json
        for i in range(4):
            pos = {
                "carro" + str(i) + "_x" : self.carros[i].x,
                "carro" + str(i) + "_y" : self.carros[i].y,
                "carro" + str(i) + "_z" : self.carros[i].z
            }
            currentPos.update(pos)
        for i in range(2):
            estado = {
                "semaforo" + str(i) + "_estado" : self.semaforo_carros[i].status
            }
            currentPos.update(estado)

        # FALTA AÑADIR FUNCIONALIDAD E INTEGRACIÓN DE LOS SEMÁFOROS CON OTROS AGENTES #
        # if (self.semaforoActivo == 0):
        #     self.semaforo_carros[0].changeStatus()
        #     self.semaforoActivo = 1
        #     print("Semaforo 1")
        # else:
        #     self.semaforo_carros[1].changeStatus()
        #     self.semaforoActivo = 0
        #     print("Semaforo 2")
        
        

        # Vemos cuanto tiempo pasó #
        global elapsed_time
        elapsed_time = time.time() - t
        print(elapsed_time)


        posJSON.append(currentPos)

        ### ¿Falta actualizarlo en el grid? ###
        ### AÑADIR ALGUNA FUNCIONALIDAD A LOS PEATONES ###
        ### AÑADIR FUNCIONALIDAD DE LOS SEMÁFOROS ###
        
        
        
    def end(self):
        self.report('ended', 1) 

        
parameters = {
    'carros': 4, # número de agentes Carro
    'semaforo_peatones': 2, # número de agentes Semáforos para peatones
    'semaforo_carros': 2, # número de agentes Semáforos para carros
    'peatones': 20, # número para agentes Peatones
    'size': 100, # Largo y alto del grid
    'steps': 100, # iteraciones
    'seed': 40,
}

model = StreetModel(parameters)
results = model.run()
print(results)

# Guardamos el JSON como archivo
json_object = json.dumps(posJSON, indent = 4)
with open("positions.json", "w") as outfile:
    outfile.write(json_object)