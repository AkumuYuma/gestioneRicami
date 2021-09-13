import datetime as d 
from GestoreDatiMateriePrime import GestoreDatiMateriePrime

class Prodotto: 
    """
        Classe che rappresenta un generico prodotto ricamato. 
    """

     
    def __init__(self, tipoProdotto: str = None, dataCommissione: d.date = None, dataInizio: d.date = None, dataFine: d.date = None, tempoLavoro: float = 0, filoUsato: float = 0, costoFilo: float = 1, prezzo: float = 0, acquirente: str = "") -> None: 

        if tipoProdotto: 
            self.tipoProdotto = tipoProdotto 
        else: self._tipoProdotto : tuple = None 

        self._dataCommissione = dataCommissione 
        self._dataInizio = dataInizio 
        self._dataFine = dataFine 
        self._tempoLavoro = tempoLavoro 
        self._filoUsato = filoUsato 
        self._costoFilo = costoFilo
        self._prezzoTotale = prezzo 
        self._acquirente = acquirente 
        self._guadagno = None 
        self._guadagnoOrario = None 

        # self._tipoProdotto : tuple = None # tipo(0) nome, tipo(1) costo

        # self._dataCommissione : d.date = None  
        # self._dataInizio: d.date = None 
        # self._dataFine : d.date = None
        # self._tempoLavoro : float = 0 # in ore  

        # self._filoUsato : float = 0 # in numero di matasse 
        # self._costoFilo : float = 1 # a matassa 
        # self._prezzoTotale : float = 0 # euro
        # self._guadagno : float = None # euro 
        # self._guadagnoOrario : float = None # euro 

        # self._acquirente : str = "" 
        
    @property 
    def tipoProdotto(self) -> tuple: 
        return self._tipoProdotto 
    @tipoProdotto.setter 
    def tipoProdotto(self, tipo: str) -> None: 
        gestore = GestoreDatiMateriePrime() 
        if tipo in gestore.dizionarioProdotti: 
            self._tipoProdotto = (tipo, gestore.dizionarioProdotti[tipo])
        else: 
           raise KeyError("Tipo prodotto sconosciuto") 

    @property 
    def dataCommissione(self) -> d.date: 
        return self._dataCommissione
    @dataCommissione.setter 
    def dataCommissione(self, giorno: d.date) -> None:
        self._dataCommissione = giorno 
    
    @property 
    def dataInizio(self) -> d.date: 
        return self._dataInizio 
    @dataInizio.setter 
    def dataInizio(self, giorno: d.date) -> None: 
        if isinstance(self.dataCommissione, d.date) and (giorno < self.dataCommissione):
            raise ValueError("Si tenta di inserire data inizio prima della data commissione")
        self._dataInizio = giorno 

    @property 
    def dataFine(self) -> d.date: 
        return self._dataFine 
    @dataFine.setter 
    def dataFine(self, giorno: d.date) -> None:
        if isinstance(self.dataCommissione, d.date) and (giorno < self.dataInizio): 
            raise ValueError("Si tenta di inserire una data di fine precedente alla data di inizio")
        self._dataFine = giorno 
        
    @property 
    def tempoLavoro(self) -> float: 
        return self._tempoLavoro
    @tempoLavoro.setter 
    def tempoLavoro(self, ore: float): 
        if ore <= 0: 
            raise ValueError("Tempo lavoro inserito non valido")
        self._tempoLavoro = ore

    @property
    def filoUsato(self) -> float: 
        return self._filoUsato 
    @filoUsato.setter
    def filoUsato(self, numeroMatasse: float) -> None: 
        if numeroMatasse < 0: 
            raise ValueError("Filo usato negativo")
        self._filoUsato = numeroMatasse 
    
    @property 
    def costoFilo(self) -> float: 
        return self._costoFilo 
    @costoFilo.setter 
    def costoFilo(self, costo: float) -> None: 
        if costo < 0: 
            raise ValueError("Costo filo negativo")
        self._costoFilo = costo
    
    @property 
    def prezzoTotale(self) -> float: 
        return self._prezzoTotale 
    @prezzoTotale.setter 
    def prezzoTotale(self, prezzo: float) -> None: 
        if prezzo < 0: 
            raise ValueError("Prezzo totale negativo")
        self._prezzoTotale = prezzo 
        
    @property 
    def guadagno(self) -> float: 
        self._calcolaGuadagno()
        return self._guadagno 
    
    
    @property 
    def guadagnoOrario(self) -> float: 
        self._calcolaGuadagnoOrario()
        return self._guadagnoOrario

    @property
    def acquirente(self) -> str:
        return self._acquirente
    @acquirente.setter
    def acquirente(self, persona: str) -> None:
        self._acquirente = persona
        

    def __str__(self) -> str:
        risposta = (
            "------------------------------- \n"
            f"Tipo Prodotto: {self.tipoProdotto[0]} \n" 
            f"Costo {self.tipoProdotto[0]}: {self.tipoProdotto[1]:.2f}E al pezzo \n"
            f"Data Commissione: {self.dataCommissione} \n"
            f"Data Inizio: {self.dataInizio} \n" 
            f"Data Fine: {self.dataFine} \n")
        
        # Se posso calcolare il tempo di lavoro lo inserisco 
        if self.tempoLavoro > 0: risposta +=  f"Tempo di lavoro: {self.tempoLavoro} ore\n"
        else: risposta += f"Ore di lavoro non calcolabili per questo oggetto... \n" 
        risposta += (
            f"Filo usato: {self.filoUsato:.2f} matasse \n"
            f"Costo filo: {self.costoFilo:.2f}E a matassa \n"
            f"Prezzo: {self.prezzoTotale:.2f}E \n"
            f"Guadagno: {self.guadagno:.2f}E \n" 
            f"Guadagno orario: {self.guadagnoOrario:.2f}E all'ora \n"
            f"Venduta a: {self.acquirente} \n"
            "-------------------------------"
        )
        return risposta
    
    def _calcolaGuadagno(self) -> float: 
        """Calcola il guadagno e setta il valore dell'attributo

        Raises:
            ValueError: Se prezzo o quantità di filo non impostata
            RuntimeError: Se il tipo prodotto non è stato impostato 
        """
        if self.prezzoTotale == 0 or self.filoUsato == 0: 
            raise ValueError("Impossibile calcolare il guadagno, prezzo o quantità di filo non impostata")
        totaleFilo = self.costoFilo * self.filoUsato 
        if not self.tipoProdotto: 
            raise RuntimeError("Impossibile, calcolare il guadagno, non si è impostato il tipo del prodotto e il suo prezzo")
        self._guadagno = self.prezzoTotale - totaleFilo - self.tipoProdotto[1] 


    def _calcolaGuadagnoOrario(self) -> float: 
        """Calcola il guadagno orario e setta il valore dell'attributo

        Raises:
            ValueError: Se il tempo di lavoro è pari a 0 o non impostato o se l'attributo guadagno non è definito
        """
        if self.tempoLavoro > 0 and self.guadagno:
            self._guadagnoOrario = self.guadagno / self.tempoLavoro 
        else: 
            raise ValueError("Errore, tempo lavoro errato o guadagno non definito")

    
    
if __name__ == "__main__":
    a = Prodotto()
    a.tipoProdotto = "TOTE_BAG"
    a.dataCommissione = d.date(2020, 10, 8)
    a.dataInizio = d.date(2020, 10, 9)
    a.dataFine = d.date(2020, 10, 12)
    a.tempoLavoro = 10 # Ore
    a.filoUsato = 3 
    a.prezzoTotale = 10 
    a.acquirente = "Ciccio"
    print(a)
    