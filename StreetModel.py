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
steps = []
jsonFile = {}
currentPos = {}

class StreetModel(ap.Model):

    def setup(self):

        # Arreglos para las posiciones de los semáforos
        semaforos_carros = []
        semaforos_peatones = []

        # Tiempo de cambio de los semáforos
        self.tiempo = self.p.tiempo

        """ Inicializamos los agentes """
        self.n_carros = self.p.carros
        self.carros = ap.AgentList(self, self.n_carros, Carro)

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
            (-3, -95), 
            (3, -95),
            (-3, -120),
            (3, -142),
            (-3, -145),
            (3, -172),
            (95, 3),
            (95, -3),
            (110, -3),
            (136, 3),
            (152, -3)
        ])
        # Definimos la posisición de los carros para mandarlo a Unity
        # Para avanzar[0 - 5] -> z++, [6 - 10] -> x++
        # -3 -120
        x_carro = [-3, 3, -3, 3, -3, 3,                95, 95, 110, 136, 152]
        z_carro = [-95, -95, -120, -142, -145, -172,   3, -3, -3, 3, -3]
        for i in range(self.n_carros):
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

        # Añadimos la posicións de los carros
        for i in range(n_semaforo_carros):
            self.semaforo_carros[i].x = x_semaforo_carro[i]
            self.semaforo_carros[i].y = 0
            self.semaforo_carros[i].z = z_semaforo_carro[i]

            semaforo = {
                "x" : x_semaforo_carro[i],
                "y" : 0,
                "z" : z_semaforo_carro[i]
            }
            semaforos_carros.append(semaforo)

        # Añadimos la posición de los semáforos
        for i in range(n_semaforo_peatones):
            self.semaforo_peatones[i].x = x_semaforo_peatones[i]
            self.semaforo_peatones[i].y = 0
            self.semaforo_peatones[i].z = z_semaforo_peatones[i]

            semaforo = {
                "x" : x_semaforo_peatones[i],
                "y" : 0,
                "z" : z_semaforo_peatones[i]
            }
            semaforos_peatones.append(semaforo)


        step = {
            "semaforos_carros": semaforos_carros,
            "semaforos_peatones": semaforos_peatones
        }
        stepInicial = {
            "posicion_inicial": step
        }
        jsonFile.update(stepInicial)

    def step(self): 
        # Añadimos las variables para el tiempo
        global t
        global elapsed_time
        if (t == 0):
            # Iniciamos el contador de segundos según inicien los steps
            t = time.time()

        # Cada step tiene un arreglo de carros y uno de semaforos
        carros = []
        semaforos_carros = []

        # Avanzan hasta que está cerca del semáforo
        for i in range(self.n_carros):
            # EJE Z
            if (i < 6):
                # Si está antes del cruce avanza
                if (self.carros[i].z < -18 or self.carros[i].z > -12):
                    self.carros[i].move_up(0.5)

                # Si el semáforo está en verde, puede avanzar más
                elif (self.semaforo_carros[0].status == 1):
                    self.carros[i].move_up(0.5)
            
            # EJE X
            else:
                if (self.carros[i].x > 18 or self.carros[i].x < 12):
                    self.carros[i].move_left(0.5)

                elif (self.semaforo_carros[1].status == 1):
                    self.carros[i].move_left(0.5)
    
    
        # Definimos la posición actual de los carros en un json
        for i in range(self.n_carros):
            carro = {
                "x": self.carros[i].x,
                "y": self.carros[i].y,
                "z": self.carros[i].z
            }
            carros.append(carro)
        for i in range(2):
            semaforo = {
                "estado": self.semaforo_carros[i].status
            }
            semaforos_carros.append(semaforo)


        # Vemos cuanto tiempo pasó #
        elapsed_time = time.time() - t

        # Tras cierta cantidad segundos cambian de estado los semáforos
        if (elapsed_time > self.tiempo):
            # Reiniciamos el contador a cero para volver a contar 6 segundos
            t = time.time()

            if (self.semaforo_carros[0].status == 1):
                self.semaforo_carros[0].status = 0
                self.semaforo_carros[1].status = 1
            else:
                self.semaforo_carros[0].status = 1
                self.semaforo_carros[1].status = 0

        # Añadimos al json las posiciones y los estados
        step = {
            "carros": carros,
            "semaforos_carros": semaforos_carros
        }
        steps.append(step)
        
        
        
    def end(self):
        steps_json = {
            "steps": steps
        }
        jsonFile.update(steps_json)
        self.report('ended', 1) 

        
parameters = {
    'tiempo': 10, # Tiempo de duración de los semáforos
    'carros': 11, # número de agentes Carro
    'semaforo_peatones': 2, # número de agentes Semáforos para peatones
    'semaforo_carros': 2, # número de agentes Semáforos para carros
    'peatones': 20, # número para agentes Peatones
    'size': 100, # Largo y alto del grid
    'steps': 600, # iteraciones
    'seed': 40,
}

model = StreetModel(parameters)
results = model.run()
print(results)

# Guardamos el JSON como archivo
json_object = json.dumps(jsonFile, indent = 4)
with open("positions.json", "w") as outfile:
    outfile.write(json_object)