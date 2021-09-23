
import datetime as d
from typing import Type 
from GestoreDatiMateriePrime import GestoreDatiMateriePrime

class Prodotto: 
    """
        Classe che rappresenta un generico prodotto ricamato. 
    """

     
    def __init__(self, tipoProdotto: str = None, dataCommissione: d.date = None, dataInizio: d.date = None, dataFine: d.date = None, tempoLavoro: float = 0, filoUsato: float = 0, costoFilo: float = 1, prezzo: float = 0, acquirente: str = "") -> None: 

        if tipoProdotto: 
            self.tipoProdotto = tipoProdotto 
        else: self._tipoProdotto : tuple = None  # tipo[0] nome, tipo[1] costo
        
        self.dataCommissione = dataCommissione 
        self.dataInizio = dataInizio 
        self.dataFine = dataFine 
        self.tempoLavoro = tempoLavoro 
        self.filoUsato = filoUsato 
        self.costoFilo = costoFilo
        self.prezzoTotale = prezzo 
        self.acquirente = acquirente 
        self._guadagno = None 
        self._guadagnoOrario = None 

        
    @property 
    def tipoProdotto(self) -> tuple: 
        return self._tipoProdotto 
    @tipoProdotto.setter 
    def tipoProdotto(self, tipo: str) -> None: 
        tipo = str(tipo)
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
        # Controllo se il valore inserito è una data o una stringa
        if giorno is not None: 
            if isinstance(giorno, str): 
                dataStringa = giorno.strip().replace(",", "-").split("-")
                giornoData = d.date(int(dataStringa[0]), int(dataStringa[1]), int(dataStringa[2]))
            elif isinstance(giorno, d.date):
                giornoData = giorno
            else: 
                # Se non è nessuna delle due c'è un errore
                raise TypeError("Il giorno inserito non è una data o una stringa")
            self._dataCommissione = giornoData
        else: 
            self._dataCommissione = None 
    
    @property 
    def dataInizio(self) -> d.date: 
        return self._dataInizio 
    @dataInizio.setter 
    def dataInizio(self, giorno: d.date) -> None: 
        if giorno is not None: 
            # Controllo se il valore inserito è una data o una stringa
            if isinstance(giorno, str): 
                dataStringa = giorno.strip().replace(",", "-").split("-")
                giornoData = d.date(int(dataStringa[0]), int(dataStringa[1]), int(dataStringa[2]))
            elif isinstance(giorno, d.date):
                giornoData = giorno
            else: 
                # Se non è nessuna delle due c'è un errore
                raise TypeError("Il giorno inserito non è una data o una stringa")
            
            if self.dataCommissione and (giornoData < self.dataCommissione):
                # Controllo che il giorno inserito non sia precedente alla data di commissione
                raise ValueError("Si tenta di inserire data inizio prima della data commissione")

            self._dataInizio = giornoData 
            
        else: self._dataInizio = None 
    @property 
    def dataFine(self) -> d.date: 
        return self._dataFine 
    @dataFine.setter 
    def dataFine(self, giorno: d.date) -> None:
        if giorno is not None: 
            # Controllo se il valore inserito è una data o una stringa
            if isinstance(giorno, str): 
                dataStringa = giorno.strip().replace(",", "-").split("-")
                giornoData = d.date(int(dataStringa[0]), int(dataStringa[1]), int(dataStringa[2]))
            elif isinstance(giorno, d.date):
                giornoData = giorno
            else: 
                # Se non è nessuna delle due c'è un errore
                raise TypeError("Il giorno inserito non è una data o una stringa")
            
            if self.dataInizio and giornoData < self.dataInizio: 
                raise ValueError("Si tenta di inserire una data di fine precedente alla data di inizio")
            self._dataFine = giornoData
        else: self._dataFine = None
        
    @property 
    def tempoLavoro(self) -> float: 
        return self._tempoLavoro
    @tempoLavoro.setter 
    def tempoLavoro(self, ore: float): 
        # Converto in float, così se ho una stringa o un tipo sbagliato sorge un errore
        ore = float(ore)
        if ore < 0: 
            raise ValueError("Tempo lavoro inserito non valido")
        self._tempoLavoro = ore

    @property
    def filoUsato(self) -> float: 
        return self._filoUsato 
    @filoUsato.setter
    def filoUsato(self, numeroMatasse: float) -> None: 
        numeroMatasse = float(numeroMatasse)
        if numeroMatasse < 0: 
            raise ValueError("Filo usato negativo")
        self._filoUsato = numeroMatasse 
    
    @property 
    def costoFilo(self) -> float: 
        return self._costoFilo 
    @costoFilo.setter 
    def costoFilo(self, costo: float) -> None: 
        costo = float(costo)
        if costo < 0: 
            raise ValueError("Costo filo negativo")
        self._costoFilo = costo
    
    @property 
    def prezzoTotale(self) -> float: 
        return self._prezzoTotale 
    @prezzoTotale.setter 
    def prezzoTotale(self, prezzo: float) -> None: 
        prezzo = float(prezzo)
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
        persona = str(persona)
        self._acquirente = persona
        
    def _to_dict(self) -> dict: 
        """Converte il prodotto in un dizionario

        Returns:
            dict: chiavi: attributi, valori: valori
        """
        return {
            "tipoProdotto": self.tipoProdotto[0], 
            "costoMateriaPrima": self.tipoProdotto[1], 
            "dataCommissione":self.dataCommissione,
            "dataInizio":self.dataInizio,
            "dataFine":self.dataFine,
            "tempoLavoro":self.tempoLavoro,
            "filoUsato":self.filoUsato,
            "costoFilo":self.costoFilo,
            "prezzoTotale":self.prezzoTotale,
            "acquirente":self.acquirente,
            "guadagno":self.guadagno,
            "guadagnoOrario":self.guadagnoOrario
        }

    def __str__(self) -> str:
        risposta = (
            "------------------------------- \n"
            f"Tipo Prodotto: {self.tipoProdotto[0]} \n" 
            f"Costo {self.tipoProdotto[0]}: {self.tipoProdotto[1]:.2f}E al pezzo \n"
            f"Data Commissione: {self.dataCommissione} \n"
            f"Data Inizio: {self.dataInizio} \n" 
            f"Data Fine: {self.dataFine} \n"
            f"Tempo lavoro: {self.tempoLavoro} ore \n"
            f"Filo usato: {self.filoUsato:.2f} matasse \n"
            f"Costo filo: {self.costoFilo:.2f}E a matassa \n"
            f"Prezzo: {self.prezzoTotale:.2f}E \n"
            ) 
        
        if self.guadagno: 
            risposta += f"Guadagno: {self.guadagno:.2f}E \n" 
        else: 
            risposta += f"Guadagno: {self.guadagno} \n" 
            
        if self.guadagnoOrario: 
            risposta += f"Guadagno orario: {self.guadagnoOrario:.2f}E all'ora \n"
        else: 
            risposta += f"Guadagno orario: {self.guadagnoOrario} \n"

        risposta += (
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
        totaleFilo = self.costoFilo * self.filoUsato 
        if self.prezzoTotale != 0 and self.filoUsato != 0 and self.tipoProdotto: 
            self._guadagno = self.prezzoTotale - totaleFilo - self.tipoProdotto[1] 


    def _calcolaGuadagnoOrario(self) -> float: 
        """Calcola il guadagno orario e setta il valore dell'attributo. Se guadagno non c'è o il tempoLavoro è negativo o 0 non fa niente.

        """
        if self.tempoLavoro > 0 and self.guadagno:
            self._guadagnoOrario = self.guadagno / self.tempoLavoro 

# Funzioni helper per la classe Prodotto
def leggiProdottoDaInput() -> Prodotto: 
    """Legge un nuovo prodotto da input

    Returns:
        Prodotto: prodotto registrato
    """
    nuovoProdotto = Prodotto() 
    tipoProdotto = input("Inserire la materia prima (in maiuscolo e con _ al posto degli spazi): ")
    try: 
        nuovoProdotto.tipoProdotto = tipoProdotto 
    except KeyError: 
        print("Il tipo è sconosciuto, lo registro") 
        costo = float(input("Inserire costo materia prima al pezzo (in euro): "))
        GestoreDatiMateriePrime().aggiungiTipoProdotto(tipoProdotto, costo)

    nuovoProdotto.tipoProdotto = tipoProdotto
    dataCommissioneStringa = input("Inserire data di commissione nel formato aa,mm,gg (o aa-mm-gg): ")
    settaDataProdotto(nuovoProdotto, "commissione", dataCommissioneStringa)
    dataInizioStringa = input("Inserire data di inizio: ")
    settaDataProdotto(nuovoProdotto, "inizio", dataInizioStringa)
    dataFineStringa = input("Inserire data di fine: ")
    settaDataProdotto(nuovoProdotto, "fine", dataFineStringa)

    tempoLavoro = input("Inserire ore di lavoro: ")
    settaValoreProdotto(nuovoProdotto, "ore", tempoLavoro)
    filoUsato = input("Inserire filo usato (in numero di matasse): ")
    settaValoreProdotto(nuovoProdotto, "filo", filoUsato)
    costoFilo = input("Inserire costo matassa (se lasciato vuoto verrà usato 1E): ")
    settaValoreProdotto(nuovoProdotto, "costo_filo", costoFilo)
    prezzo = input("Inserire prezzo prodotto: ")
    settaValoreProdotto(nuovoProdotto, "prezzo", prezzo)

    acquirente = input("Inserire acquirente: ")
    nuovoProdotto.acquirente = acquirente

    return nuovoProdotto 
    
def settaDataProdotto(prodotto: Prodotto, tipoData: str, dataStringa: str) -> None:
    """Setta la data nel prodotto passato se nessuna data viene passata, la lascia a None

    Args:
        prodotto (Prodotto): Prodotto di cui settare la data
        tipoData (str): commissione, inizio, fine
        dataStringa (str, optional): Data separata da , o -. 

    Raises:
        ValueError: [description]
    """
    data = dataStringa.strip().replace("-", ",").replace(" ", "").split(",")
    if not tipoData in ["commissione", "inizio", "fine"]:
        raise ValueError("Tipo data non valido")
    # Se la data non è inserita lascio il campo non settato (di default nei prodotti è a None)
    if dataStringa:  
        try:
            if tipoData == "commissione":
                prodotto.dataCommissione = d.date(int(data[0]), int(data[1]), int(data[2])) 
            elif tipoData == "inizio": 
                prodotto.dataInizio = d.date(int(data[0]), int(data[1]), int(data[2])) 
            else: 
                prodotto.dataFine = d.date(int(data[0]), int(data[1]), int(data[2])) 
        except ValueError:
            print("Data inserita non valida lasciato campo vuoto")

def settaValoreProdotto(prodotto: Prodotto, tipoValore: str, valore: str) -> None: 
    """Setta il valore del tipo specificato nel oggetto prodotto

    Args:
        prodotto (Prodotto): Oggetto da aggiornare 
        tipoValore (str): attributo da aggiornare 
        valore (str): Valore. Attenzione. Lasciato in stringa perchè potrebbe essere "" (e quindi non convertibile a float). 
                      In quel caso viene lasciato il valore di default del costruttore. 

    Raises:
        ValueError: Se il tipo passato non è valido
    """
    if tipoValore not in ["ore", "filo", "costo_filo", "prezzo"]:
        raise ValueError("Attributo \"" + valore + "\" non valido.")


    if valore:
        valore = float(valore)
        if tipoValore == "ore":
            prodotto.tempoLavoro = valore
        elif tipoValore == "filo":
            prodotto.filoUsato = valore 
        elif tipoValore == "costo_filo":
            prodotto.costoFilo = valore 
        else: 
            prodotto.prezzoTotale = valore 


if __name__ == "__main__":
    listaAttributi = ["a", "2020-10-10", "2020-10-11", None]
    a = Prodotto(*listaAttributi)
    print(a)
    