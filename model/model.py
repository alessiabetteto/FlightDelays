import copy

import networkx as nx
from fastapi._compat import v2

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()  # semplice, non orientato e pesato
        self._airports = DAO.getAllAirports()
        self._idMapAirports= {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a
        self._bestCammino = []
        self._bestScore = 0

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

# !!!!!!!!!!!!!
    def getViciniOrdinati(self, source):
        """ restituisce i vicini ordinati a partire da un aeroporto di partenza source """
        vicini = self._graph.neighbors(source) # gli passiamo il nodo rispetto a cui vogliamo i vicini
        viciniT = []   # lista di tuple
        for v in vicini:
            viciniT.append ( (v, self._graph[source][v]['weight']) )   # sono sicura che l'arco source-v esista perché v fa parte dei vicini
        viciniT.sort(key=lambda x:x[1], reverse=True)   # x[1] corrisponde all'elemento 1 della tupla (v, self._graph[source][v]['weight']) quindi self._graph[source][v]['weight']
        return viciniT


    def hasPath(self, v0, v1):
        """ Restituisce true se esiste un qualche cammino tra v0 e v1 altrimenti false"""
        #nx.node_connected_component(v0)
        # nx.connected_components (restituisce TUTTE le componenti connesse), l'altro metodo ne restituisce solo 1, quella che contiene v0

        return v1 in nx.node_connected_component(self._graph, v0) # mi restituisce true se è contenuto, false altrimenti

    def getPath(self, v0, v1):
        """ Se hasPath mi restituisce true, allora vogliamo sapere quale sia il cammino"""
        # dictOfPredecessors = nx.bfs_predecessors(self._graph, v0)   # cercherà i cammini minimi breadth-first (num min di archi)
        # # ogni nodo sarà una chiave, per ogni nodo mi dice il nodo precedente nell'albero di visita
        # # recupero il percorso all'indietro
        # path = [v1]
        # while path[0] != v0: # finché non sono arrivato a v0, continuo ad aggiungere
        #     path.insert(0, dictOfPredecessors[path[0]])
        #
        # # path = [v0, -----, v1] e lo inizio a riempire dal fondo
        #
        # # potevo anche farlo in depth-first ma veniva più lungo
        # dictOfPredecessors = nx.dfs_predecessors(self._graph, v0)
        #
        # # versione 3
        # path = nx.shortest_path(v0, v1)

        #versione 4
        path = nx.dijkstra_path(self._graph, v0, v1)  # ignora i pesi

        # sono tutti analoghi perché la traccia ci chiedere UN percorso, non uno in particolare

        return path

    def getCamminoOttimo(self, v0, v1, t):
        self._bestCammino = []
        self._bestScore = 0
        parziale = [v0]   # lista che parte da v0, perché il nostro cammino parte da v0, quindi questo nodo ci sarà sicuramente

        self._ricorsione(parziale, v1, t)
        return self._bestCammino, self._bestScore

    def _ricorsione(self, parziale, v1, t):
        """ Verifico se parziale è una slz valida ed in caso la salvo
         Verifico se ha senso continuare ad aggiungere elmenti in parziale, oppure esco
         Se no espando parziale e faccio ricorsione con backtracking"""

        # la slz ottima può essere < o <= a t!
        if parziale [-1] == v1:
            # sono arrivato alla soluzione
            # potenzialmente è una slz accettabile, la confronto con quella trovata finora
            if self._getScore(parziale) > self._bestScore:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)

        # esco se ha raggiunto il num max di tratte
        if len(parziale) == t+1:  # t+1 nodi quindi t archi
            return

        #backtracking
        for n in self._graph.neighbors(parziale[-1]):  # ciclo sui vicini dell'ultimo nodo che ho inserito
            if n not in parziale:  # per non aggiungere doppi nodi
                parziale.append(n)
                self._ricorsione(parziale, v1, t)
                parziale.pop()


    def _getScore(self, parziale):
        sumPesi = 0
        for i in range(0, len(parziale)-1):
            sumPesi += self._graph[parziale[i]][parziale[i+1]]['weight']
        return sumPesi





