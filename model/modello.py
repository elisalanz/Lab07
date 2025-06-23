import copy

from database.meteo_dao import MeteoDao
from model.situazione import Situazione

class Model:
    def __init__(self):
        self._situazioni = []
        self.costo_ottimo = -1
        self.soluzione_ottima = []

    def getSituazioni(self):
        if len(self._situazioni) == 0:
            self._situazioni = MeteoDao.get_all_situazioni()
        return self._situazioni

    def calcolaMedia(self, vettore):
        risultato = None
        if len(vettore) != 0:
            somma = 0
            for numero in vettore:
                somma += numero
            risultato = somma / len(vettore)
        return risultato

    def getUmiditaMediaPerMese(self, mese):
        situazioni = self.getSituazioni()
        umiditaGenova = []
        umiditaMilano = []
        umiditaTorino = []
        mediaGenova = None
        mediaMilano = None
        mediaTorino = None
        for situazione in situazioni:
            if situazione.getMese() == mese:
                if situazione.localita == "Genova":
                    umiditaGenova.append(situazione.umidita)
                elif situazione.localita == "Milano":
                    umiditaMilano.append(situazione.umidita)
                elif situazione.localita == "Torino":
                    umiditaTorino.append(situazione.umidita)
                mediaGenova = self.calcolaMedia(umiditaGenova)
                mediaMilano = self.calcolaMedia(umiditaMilano)
                mediaTorino = self.calcolaMedia(umiditaTorino)
        return mediaGenova, mediaMilano, mediaTorino


    # SECONDO PUNTO (fatto a lezione)


    def calcola_sequenza(self, mese):
        self.costo_ottimo = -1
        self.soluzione_ottima = []
        situazioni = MeteoDao.get_situazioni_meta_mese(mese)
        self._ricorsione([], situazioni)
        return self.soluzione_ottima, self.costo_ottimo


    def trova_possibili_step(self, parziale, lista_situazioni):
        giorno = len(parziale)+1 # per cercare giorno successivo
        candidati = []
        for situazione in lista_situazioni:
            if situazione.data.day == giorno:
                candidati.append(situazione)
        return candidati


    def is_admissible(self, candidate, parziale):
        # vincolo sui 6 giorni
        counter = 0
        for situazione in parziale:
            if situazione.localita == candidate.localita:
                counter += 1
        if counter == 6:
            return False
        # vincolo su permanenza (min 3 gg consecutivi nella stessa città)
        # 1) lunghezza di parziale minore di 3
        if len(parziale) == 0:
            return True
        if len(parziale) <3:
            if candidate.localita != parziale[0].localita:
                return False
        # 2) le tre situazioni precedenti non sono tutte uguali
        else:
            if parziale[-1].localita != parziale[-2].localita or parziale[-2].localita != parziale[-3].localita or parziale[-1].localita != parziale[-3].localita:
                if parziale[-1].localita != candidate.localita:
                    return False
        # altrimenti ok
        return True


    def _calcola_costo(self, parziale):
        costo = 0
        # 1) costo umidità
        for situazione in parziale:
            costo += situazione.umidita
        # 2) costo sugli spostamenti
        for i in range(len(parziale)):
            # se i due giorni precedenti non sono stato nella stessa citta in cui sono ora, pago 100
            if i >= 2 and parziale[i-1].localita != parziale[i].localita or parziale[i-2].localita != parziale[i].localita:
                costo += 100
        return costo


    def _ricorsione(self, parziale, lista_situazioni):
        # condizione terminale
        if len(parziale) == 15:
            costo = self._calcola_costo(parziale)
            if self.costo_ottimo==-1 or self.costo_ottimo>costo:
                self.costo_ottimo = costo
                self.soluzione_ottima = copy.deepcopy(parziale)
        # condizione ricorsiva
        else:
            # cercare le citta per il giorno che mi serve
            candidates = self.trova_possibili_step(parziale, lista_situazioni)  # per esplorare meno possibilità
            # provo ad aggiungere una di queste città e vado avanti
            for candidate in candidates:
                # verifica vincoli
                # (i vincoli si possono aggiungere sia nella condizione terminale sia quando aggiungo un altro elemento al parziale)
                if self.is_admissible(candidate, parziale):
                    parziale.append(candidate)
                    self._ricorsione(parziale, lista_situazioni)
                    parziale.pop()