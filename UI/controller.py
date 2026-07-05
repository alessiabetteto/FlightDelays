import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choicePartenza = None
        self._choiceArrivo = None

    def handleAnalizza(self,e):
        cMinTxt = self._view._txtInCMin.value
        if cMinTxt == "":
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Inserire un valore numerico:", color="red"))
            self._view.update_page()
            return

        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Inserire un valore intero:", color="red"))
            self._view.update_page()
            return

        # sappiamo che è intero se siamo arrivati qui
        # controllare un valore negativo o 0
        if cMin <=0:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Inserire un valore intero:", color="red"))
            self._view.update_page()
            return

        # se siamo sopravvissuti: grafo
        self._model.buildGraph(cMin)
        nNodes, nEdges = self._model.getGraphDetails()

        # solo dopo aver correttamente creato il grafo, posso riempire il dropdown che contiene gli aeroporti di partenza
        allNodes = self._model.getAllNodes()
        self._fillDropdown(allNodes)



        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(ft.Text("Grafo correttamente creato", color="green"))

        self._view._txtResults.controls.append(ft.Text(f"Il grafo contiente {nNodes} nodi e {nEdges} archi", color="green"))
        self._view.update_page()





    def handleConnessi(self, e):
        pass

    def handleCerca(self, e):
        pass

    def _fillDropdown(self, allNodes):
        for n in allNodes:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data = n, key= n.IATA_CODE, on_click=self._choiceDdPartenza))
            self._view._ddAeroportoA.options.append(ft.dropdown.Option(data = n, key= n.IATA_CODE, on_click=self._choiceDdArrivo))

    def _choiceDdPartenza(self, e):
        self._choicePartenza = e.control.data
        print(f"Hai selezionato come aeroporto di partenza {self._choicePartenza}")

    def _choiceDdArrivo(self, e):
        self._choiceArrivo = e.control.data
        print(f"Hai selezionato come aeroporto di partenza {self._choiceArrivo}")
