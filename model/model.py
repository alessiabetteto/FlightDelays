import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()  # semplice, non orientato e pesato
        self._airports = DAO.getAllAirports()
        self._idMapAirports= {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a

    def buildGraph(self, nMin):  #nMin fornito dall'utente
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)

        #aggiungo i nodi al grafo
        self._graph.add_nodes_from(nodes)

        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")
        # self.addEdges()
        # print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")
        # self._graph.clear_edges()
        self.addEdgesV2()
        print(f"N nodi: {len(self._graph.nodes)}, n archi: {len(self._graph.edges)}")



    def addEdges(self):   # V1: query facile, python difficile
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)
        """ Queste tratte hanno 2 problemi:
            1. ho archi diretti e inversi quindi dovrò fare la somma a mano
            2. ho archi fra aeroporti che avevo filtrato """

        for t in allTratte:
            # !!!!!!
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:  # attenzione se non facevi questo controllo, ti considerava anche tratte che non esistevano quindi ti aggiungeva i nodi!!! i nodi da 98 diventavano 300
                # se sono già stati aggiunti nel grafo allora posso aggiungerlo
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA):
                    # non aggiungerne un altro ma incrementa solo il peso
                    self._graph[t.aeroportoP][t.aeroportoA]['weight'] += t.peso
                else:
                    self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)

    def addEdgesV2(self):  # query più complessa, python più facile
        allTratte = DAO.getAllEdgesV1(self._idMapAirports)

        for t in allTratte:
            # !!!!!!
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:  # attenzione se non facevi questo controllo, ti considerava anche tratte che non esistevano quindi ti aggiungeva i nodi!!! i nodi da 98 diventavano 300
                # mi basta solo questo perché so che l'arco è unico
                self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)


    def getGraphDetails(self):
        return (len(self._graph.nodes), len(self._graph.edges))


    def getAllNodes(self):
        nodes=  list(self._graph.nodes)
        nodes.sort(key=lambda x:x.IATA_CODE)
        return nodes