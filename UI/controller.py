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
        # controlliamo input utente
        if self._choicePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di partenza", color="red"))
            self._view.update_page()
            return

        # se l'utente ha selezionato un aeroporto, tutto ok, chiamiamo il metodo del model
        viciniT = self._model.getViciniOrdinati(self._choicePartenza)
        self._view._txtResults.controls.clear()
        for v in viciniT:
            self._view._txtResults.controls.append(ft.Text(f"{v[0]} - peso: {v[1]}"))

        self._view.update_page()



    def handleTestConnessione(self,e):
        """ Verificare che la connessione esista e se esiste trovare un cammino qualsiasi"""
        if self._choicePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di partenza", color="red"))
            self._view.update_page()
            return

        if self._choiceArrivo is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di arrivo", color="red"))
            self._view.update_page()
            return

        if not self._model.hasPath(self._choicePartenza, self._choiceArrivo):
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text(f"Non ho trovato un cammino tra {self._choicePartenza} e {self._choiceArrivo}", color="red"))
            self._view.update_page()
            return

        path = self._model.getPath(self._choicePartenza, self._choiceArrivo)
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text(f"Ho trovato un cammino tra {self._choicePartenza} e {self._choiceArrivo}. Di seguito i nodi che compongono il cammino:", color="green"))
        self._view.update_page()
        for p in path:
            self._view._txtResults.controls.append(ft.Text(p))
        self._view.update_page()


    def handleCerca(self, e):
        """"""
        t = self._view._txtNTratteMax.value
        # t ci serve intero
        try:
            tInt = int(t)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text(
                    f"Il valore di t deve essere un intero positivo",
                    color="red"))
            self._view.update_page()
            return

        path, score = self._model.getCamminoOttimo(self._choicePartenza, self._choiceArrivo, tInt)
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text(
                f"Cammino tra {self._choicePartenza} e {self._choiceArrivo} trovato",
                color="green"))
        self._view._txtResults.controls.append(
            ft.Text(
                f"Il cammino ha uno score complessivo pari a {score} e contiene i seguenti nodi:",
                color="green"))
        for p in path:
            self._view._txtResults.controls.append(
                ft.Text( p,color="green"))


        self._view.update_page()





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
