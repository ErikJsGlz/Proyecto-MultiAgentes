import agentpy as ap
from semaforo_c import SemaforoCarro
from semaforo_p import SemaforoPeaton
from carro import Carro
from peaton import Peaton

# Importamos JSON
import json
# Posiciones en formato JSON
posJSON = []

class StreetModel(ap.Model):

    def setup(self):
        """ Inicializamos los agentes """
        n_carros = self.p.carros
        self.carros = ap.AgentList(self, n_carros, Carro)

        n_semaforo_peatones = self.p.semaforo_peatones
        self.semaforo_peatones = ap.AgentList(self, n_semaforo_peatones, SemaforoPeaton)

        n_semaforo_carros = self.p.semaforo_carros
        self.semaforo_carros = ap.AgentList(self, n_semaforo_carros, SemaforoCarro)

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

    def step(self): 
        #self.cars.agent_method()
        pass
        # self.carros.move_left(2)

    def update(self):
        
        # Meter agente semáforo #

        print("\n")
        for i in range(4):
            print("Carro " + str(i + 1) + " - Posición: (" + str(self.carros[i].x) + ", " + str(self.carros[i].y) + ", " + str(self.carros[i].z) + ")" )
        
        # Hacemos que avancen los carros
        for i in range(4):
            if (i == 0 or i == 1):
                self.carros[i].move_up(1)
            elif (i == 2 or i == 3):
                self.carros[i].move_right(1)

        for i in range(4):
            pos = {
                "x" : self.carros[i].x,
                "y" : self.carros[i].y,
                "z" : self.carros[i].z
            }
            posJSON.append(pos)
        
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