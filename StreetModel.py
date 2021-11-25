import agentpy as ap
from semaforo_c import SemaforoCarro
from semaforo_p import SemaforoPeaton
from carro import Carro
from peaton import Peaton

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

        # Agregamos a los agentes
        """ 
        Random: para asignar posiciones aleatorias 
        empty: ?
        
        
        """
        self.cruce.add_agents(self.carros, [(2, 3), (4, 6)])
        # self.carros[0].x = 2

        for i in range(2):
            if (i == 0):
                self.carros[i].x = 2
                self.carros[i].y = 3

            elif (i == 1):
                self.carros[i].x = 4
                self.carros[i].y = 6

        # carros.x
        # carros[0].x
        
        #print("Hay un total de: " + str(self.p.carros) + " carros")
        # for car in self.carros:
        #     print(car.x)}

    def step(self): 
        #self.cars.agent_method()
        pass
        # self.carros.move_left(2)

    def update(self):
        # self.cars.record('success')
        print("\n" + str(self.carros.x))
        count = 0
        for carro in self.carros:
            count += 1
            if (count % 2 == 0):
                carro.move_left(2)
                # print(carro.x)
                # self.carros[carro].move_left(2)
            else:
                carro.move_right(2)
        
    def end(self):
        self.report('ended', 1) 

        
parameters = {
    'carros': 2, # número de agentes Carro
    'semaforo_peatones': 2, # número de agentes Semáforos para peatones
    'semaforo_carros': 2, # número de agentes Semáforos para carros
    'peatones': 20, # número para agentes Peatones
    'size': 100, # Largo y alto del grid
    'steps': 10, # iteraciones
    'seed': 40,
}

model = StreetModel(parameters)
results = model.run()
print(results)