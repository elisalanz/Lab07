import flet as ft

from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        if self._view.dd_mese.value is None or self._view.dd_mese.value == "":
            self._view.create_alert("Selezionare un mese!")
            return
        mese = int(self._view.dd_mese.value)
        mediaGenova, mediaMilano, mediaTorino = self._model.getUmiditaMediaPerMese(mese)
        self._view.lst_result.controls.append(ft.Text(f"L'umidità media del mese selezionato è:\nGenova: {mediaGenova}\nMilano: {mediaMilano}\nTorino: {mediaTorino}"))
        self._view.dd_mese.value = None
        self._view.update_page()
        self._view.lst_result.controls.clear()

    def handle_sequenza(self, e):
        if self._view.dd_mese.value is None or self._view.dd_mese.value == "":
            self._view.create_alert("Selezionare un mese!")
            return
        mese = int(self._view.dd_mese.value)
        soluzione_ottima, costo_ottimo = self._model.calcola_sequenza(mese)
        txt = f"La sequenza ottima ha costo {costo_ottimo} ed è:\n"
        for situazione in soluzione_ottima:
            txt += f"[{situazione.localita} - {situazione.data}] Umidità = {situazione.umidita}\n"
        self._view.lst_result.controls.append(ft.Text(txt))
        self._view.dd_mese.value = None
        self._view.update_page()
        self._view.lst_result.controls.clear()

    def read_mese(self, e):
        self._mese = int(e.control.value)

