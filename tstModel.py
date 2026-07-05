from model.model import Model

# creiamo un'istanza del modello e chiamerà il metodo buildgraph
# lo facciamo per vedere se il metodo buildgraph nel model finora ha senso

myModel = Model()
myModel.buildGraph(5)
nNodes, nEdges = myModel.getGraphDetails()
print(f"Num nodes:{nNodes}, num edges:{nEdges}")