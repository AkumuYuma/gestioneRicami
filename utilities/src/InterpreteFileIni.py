from Prodotto import Prodotto
import datetime as d 
import configparser as c
from GestoreDatiMateriePrime import GestoreDatiMateriePrime


    

class InterpreteFileIni: 
    """
    Classe per interpretare un file ini passato come argomento e creare un corrispondente prodotto. 
    Permette anche di scrivere un file ini a partire da un tipo Prodotto 
    
    Nel file: 
        * Le date devono essere scritte nel formato aa,mm,gg (al posto della , va bene anche -) 
        * I numeri nel formato x.y
        * L'ordine deve essere: 
            * tipo prodotto (tutto minuscolo, al posto degli spazi usare il carattere _)
            * data Commissione
            * data inizio 
            * data fine 
            * ore di lavoro 
            * filo usato 
            * costo filo 
            * prezzo 
            * acquirente 
    """
    
    def leggiDaFile(self, path: str) -> Prodotto: 
        """Restituisce un oggetto di tipo Prodotto specializzato in base ai dati letti nel file

        Args:
            path (str): Path del file ini da leggere. 

        Raises:
            ValueError: Se il tipo di prodotto specificato nel file è sconosciuto
        """
        nuovoProdotto = Prodotto()
        fileParser = c.ConfigParser()
        fileParser.read(path)
        prodottoLettoDaFile = fileParser["PRODOTTO"]
        
        # Controllo che il tipo di prodotto sia specificato 
        try: 
            tipoProdotto = prodottoLettoDaFile["tipo"]
        except KeyError: 
            print("[DEBUG] Tipo prodotto non specificato. L'errore è fatale. Esco")
            exit(1)

        # Controllo che il tipo sia tra quelli già presenti 
        try: 
            nuovoProdotto.tipoProdotto = tipoProdotto
        except KeyError: 
            # Se non lo è lo inserisco al momento 
            try: 
                GestoreDatiMateriePrime().aggiungiTipoProdotto(tipoProdotto, float(prodottoLettoDaFile["costo"]))
                nuovoProdotto.tipoProdotto = tipoProdotto
            except KeyError: 
                print("[DEBUG] Inserito un nuovo tipo di prodotto ma non specificato il prezzo. \nL'errore è fatale")
                quit()
                

        # Setto date e valori numerici
        for data in ["commissione", "inizio", "fine"]: 
            self._settaData(prodottoLettoDaFile, nuovoProdotto, data)
        for valoreNumerico in ["ore", "filo", "costo_filo", "prezzo"]: 
            self._settaValoreNumerico(prodottoLettoDaFile, nuovoProdotto, valoreNumerico)

        # Setto l'acquirente 
        try: 
            acquirente = prodottoLettoDaFile["acquirente"]
            nuovoProdotto.acquirente = acquirente 
        except KeyError:
            print("[DEBUG] Nessun acquirente inserito, lascio il campo vuoto")

        return nuovoProdotto
    
    def _settaData(self, parserProdotto: c.ConfigParser, prodotto: Prodotto, attributo: str) -> None:
        """Setta le date specificate da attributo

        Args:
            parserProdotto (c.ConfigParser): parser del file ini alla voce "PRODOTTO"
            prodotto (Prodotto): prodotto su cui settare la data
            attributo (str): tipo di data {commissione, inizio, fine}

        Raises:
            ValueError: se attributo non è una delle tre menzionate sopra
        """
        # attributo: commissione-inizio-fine 
        if attributo not in ["commissione", "inizio", "fine"]:
            raise ValueError("Attributo \"" + attributo + "\" non valido")
        
        try:  
            dataStringa = parserProdotto[attributo]
            dataListaStringhe = dataStringa.strip().replace("-", ",").split(",")
            if attributo == "commissione":
                prodotto.dataCommissione = d.date(int(dataListaStringhe[0]), int(dataListaStringhe[1]), int(dataListaStringhe[2]))
            elif attributo == "inizio":
                prodotto.dataInizio = d.date(int(dataListaStringhe[0]), int(dataListaStringhe[1]), int(dataListaStringhe[2]))
            else: 
                prodotto.dataFine = d.date(int(dataListaStringhe[0]), int(dataListaStringhe[1]), int(dataListaStringhe[2]))
        except KeyError:
            print("[DEBUG]: Nessuna data " + attributo + " immessa, campo lasciato vuoto")
    
    def _settaValoreNumerico(self, parserProdotto: c.ConfigParser, prodotto: Prodotto, attributo: str) -> None: 
        """Setta i valori numerici al prodotto

        Args:
            parserProdotto (c.ConfigParser): parser del file ini alla voce "PRODOTTO"
            prodotto (Prodotto): prodotto su cui settare il valore numerico 
            attributo (str): tipo di valore {filo, costo_filo, prezzo}
        Raises:
            ValueError: se attributo non è una delle tre menzionate sopra
        """
        
        if attributo not in ["ore", "filo", "costo_filo", "prezzo"]:
            raise ValueError("Attributo \"" + attributo + "\" non valido")
        
        try: 
            valore = float(parserProdotto[attributo])
            if attributo == "ore":
                prodotto.tempoLavoro = valore
            elif attributo == "filo":
                prodotto.filoUsato = valore 
            elif attributo == "costo_filo":
                prodotto.costoFilo = valore 
            else: 
                prodotto.prezzoTotale = valore 
        except KeyError:
            print("[DEBUG]: Nessun valore " + attributo + " immesso, campo lasciato vuoto")
    

    def scriviProdottoSuFile(self, oggetto: Prodotto, pathFile: str) -> None:
        """Scrive il prodtto passato come parametro su un file ini 

        Args:
            oggetto (Prodotto): oggetto da scrivere su file
            pathFile (str): path del file da scrivere e nome
        """
        parser = c.ConfigParser() 
        parser["PRODOTTO"] = {}
        self._controllaEAggiungi(parser, oggetto)
        with open(pathFile, "w") as f: 
            parser.write(f)

    def _controllaEAggiungi(self, parser: c.ConfigParser, oggetto: Prodotto) -> None:
        """Scannerizza gli attributi dell'oggetto Prodotto e scrive nel parser solo i campi pieni 
        
        Args:
            parser (c.ConfigParser): parser (Attenzione! Viene modificato)
            oggetto (Prodotto): prodotto da scrivere nel parser 
        """

        # devo mappare il nome degli attributi dell'oggetto Prodotto nei nomi dati nel file ini
        alfabeto = {
            "dataCommissione": "commissione", 
            "dataInizio": "inizio",
            "dataFine": "fine", 
            "tempoLavoro": "ore", 
            "filoUsato": "filo", 
            "costoFilo": "costo_filo", 
            "prezzoTotale": "prezzo", 
            "acquirente": "acquirente", 
            "guadagno": "guadagno", 
            "guadagnoOrario": "guadagno_orario"
        }
        for attr in dir(oggetto): 
            # Se un attributo è None non viene proprio inserito nel parser
            # Controllo che l'attributo non sia privato (non inizia con _) e che il campo non sia None
            if not attr.startswith("_") and getattr(oggetto, attr) is not None:
                # Il tipo va gestito diversamente dato che è una tupla
                if attr == "tipoProdotto": 
                    parser["PRODOTTO"]["tipo"] = str(oggetto.tipoProdotto[0])
                    parser["PRODOTTO"]["costo_materiale"] = str(oggetto.tipoProdotto[1])
                else: 
                    parser["PRODOTTO"][alfabeto[attr]] = str(getattr(oggetto, attr))
                
            
    
import sys
import os.path
if __name__ == "__main__":
    interprete = InterpreteFileIni()
    prodotto = interprete.leggiDaFile(os.path.dirname(__file__) + "/../dati/fileConfigurazione/esempio.ini")
    print(prodotto)
    interprete.scriviProdottoSuFile(prodotto, os.path.dirname(__file__) + "/../dati/stampati/provaScrittura.ini")
    
