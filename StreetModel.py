import agentpy as ap

class StreetModel(ap.Model):
    def setup(self):
        self.agents = ap.AgentList(self, self.p.agents, MyAgent)
        print("Hola soy una calle!")

    def step(self):
        self.agents.agent_method()

    def update(self):
        self.agents.record('success')
        print("still working")
        
    def end(self):
        self.report('ended', 1) 
parameters = {
    'my_parameter': 42,
    'agents': 3,
    'steps': 10 
}

