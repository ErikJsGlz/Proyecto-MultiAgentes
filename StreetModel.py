import agentpy as ap
from semaforo_c import SemaforoCarro
from semaforo_p import SemaforoPeaton
from carro import Carro
from peaton import Peaton

class StreetModel(ap.Model):

    # Inicializamos los agentes
    def setup(self):
        
        self.carros = ap.AgentList(self, self.p.carros, Carro)
        self.semaforo_peatones = ap.AgentList(self, self.p.semaforo_peatones, SemaforoPeaton)
        self.semaforo_carros = ap.AgentList(self, self.p.semaforo_carros, SemaforoCarro)
        self.peatones = ap.AgentList(self, self.p.peatones, Peaton)
        
        #print("Hay un total de: " + str(self.p.carros) + " carros")
        # for car in self.carros:
        #     print(car.x)

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
    'carros': 10,
    'semaforo_peatones': 2,
    'semaforo_carros': 2,
    'peatones': 20,
    'steps': 10,
    'seed': 40,
}

model = StreetModel(parameters)
results = model.run()
print(results)