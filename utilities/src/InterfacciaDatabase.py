from Prodotto import Prodotto
import sqlite3 as sql
import datetime as d
import re
import os.path 
import pandas as pd

class InterfacciaDatabase: 
    """
        Classe di interfaccia con il database. Deve implementare tutte le query per il db. 
        Si vuole renderla il più indipendente possibile dalla scelta di sqlite. (Eventualmente migrabile su mysql)
    """
    
    DATABASEPATH = os.path.dirname(__file__) + "/../dati/database/prodotti.db"

    def __init__(self) -> None:
        self._connessione = sql.connect(self.DATABASEPATH)
    
    def __del__(self) -> None: 
        self._connessione.close()
    
    def creaTabellaProdotti(self) -> None: 
        """
            Crea la tabella prodotti se non esiste
        """ 
        
        self._connessione.cursor().execute(
            """CREATE TABLE IF NOT EXISTS Prodotti(
                idProdotto INTEGER PRIMARY KEY, 
                tipoProdotto VARCHAR(20),
                costoMateriale REAL, 
                dataCommissione VARCHAR(12), 
                dataInizio VARCHAR(12), 
                dataFine VARCHAR(12), 
                tempoLavoro REAL, 
                filoUsato REAL, 
                costoFilo REAL, 
                prezzoTotale REAL, 
                acquirente VARCHAR(30)
            )""")
        self._connessione.commit()
    
    def inserisciProdotto(self, oggetto: Prodotto) -> int: 
        """Inserisce una riga nella tabella a partire dall'oggetto prodotto

        Args:
            oggetto (Prodotto): Prodotto da inserire
        Returns: 
            int: id dell'oggetto appena inserito 
        """

        # Costruisco una stringa con i nomi degli attributi separati da una ,
        listaAttributi = "" 
        for attr in dir(oggetto): 
            # Non inserisco guadagno e guadagnoOrario, quelli li calcolo a posteriori
            if attr == "guadagno" or attr == "guadagnoOrario": 
                continue

            if not attr.startswith("_") and getattr(oggetto, attr) is not None: 
                if attr == "tipoProdotto": 
                    listaAttributi += "tipoProdotto, "  
                    listaAttributi += "costoMateriale, "
                else: 
                    listaAttributi += attr + ", "
                
        # Costruisco una stringa con i valori degli attributi (nello stesso ordine dei nomi)
        # Le stringhe sono circondate dal simbolo '
        listaValoriAttributi = ""
        for attr in dir(oggetto):
            if attr == "guadagno" or attr == "guadagnoOrario": 
                continue
            if not attr.startswith("_"):
                if attr == "tipoProdotto": 
                    listaValoriAttributi += "'" + str(getattr(oggetto, attr)[0]) + "'" + ", "
                    listaValoriAttributi += str(getattr(oggetto, attr)[1]) + ", "
                elif getattr(oggetto, attr) is not None: 
                    # Se il valore è stringa o data, metto le ' attorno per scriverlo come stringa
                    if isinstance(getattr(oggetto, attr), str) or isinstance(getattr(oggetto, attr), d.date): 
                        listaValoriAttributi += "'" + str(getattr(oggetto, attr)) + "'"+ ", " 
                    else: 
                        listaValoriAttributi += str(getattr(oggetto, attr)) + ", "
        
        # Tolgo le virgole finali    
        listaAttributi = listaAttributi.strip().rstrip(",")
        listaValoriAttributi = listaValoriAttributi.strip().rstrip(",")

        # Inserisco nella tabella
        cursore = self._inoltraQuery("INSERT INTO Prodotti (" + listaAttributi + ")" + 
                          "VALUES (" + listaValoriAttributi + ")") 
        # Confermo i cambiamenti
        self._connessione.commit()
        return cursore.lastrowid

    def _inoltraQuery(self, query: str) -> sql.Cursor: 
        """
            Inoltra al db la query passata come stringa in linguaggio sql 
        """
        return self._connessione.cursor().execute(query)

    def stampaTabella(self, condizione : str = "") -> None: 
        """
            Stampa gli elementi della tabella che matchano la coindizione

        Args:
            condizione (str, optional): Condizione della query. 
            Default = "". Se lasciata vuota stampa l'intera tabella
            
        """
        print(self.toDataframe(condizione))

    def ricercaPerParametro(self, condizione: str = "") -> sql.Cursor:
        """Inoltra una query per selezionare solo gli oggetti specificati nella condizione

        Args:
            condizione (str, optional): Condizione della query 
                        Esempio : prezzototale > 10 
                        Esempio : tipoProdotto = 'TOTE_BAG'  
            Default = "". Se lasciata vuota restituisce l'intera tabella

        Raises:
            ValueError: Se la colonna su cui si vuole applicare la condizione non esiste

        Returns:
            sql.Cursor: Cursore con il risultato della ricerca. 
        """

        if not condizione: 
            cursore = self._inoltraQuery("SELECT * FROM Prodotti")
        
        else: 
            
            # Controllo che il parametro sia tra le colonne
            # Seleziono il parametro splittando la stringa al primo carattere non alfanumerico
            parametro = re.split("[^\w\d]", condizione)[0]
            if parametro not in [nomeParametro[0] for nomeParametro in self._inoltraQuery("SELECT * FROM Prodotti").description]:
                raise ValueError("Errore, la colonna su cui eseguire la condizione non esiste")
            cursore = self._inoltraQuery("SELECT * FROM Prodotti WHERE " + condizione) 

        return cursore 
         
    def aggiornaCampo(self, idProdotto: int, campoDaAggiornare: str, nuovoValore) -> None: 
        """Aggiorna un campo della tabella prodotti con un nuovo valore 

        Args:
            idProdotto (int): id del prodotto da aggiornare. Bisogna trovarlo tramite una ricerca
            campoDaAggiornare (str): campo da aggiornare 
            nuovoValore ([type]): nuovo valore del campo, può essere una stringa o un numero
        """
        query = f"Update Prodotti SET {campoDaAggiornare} = {nuovoValore} WHERE idProdotto = {idProdotto}"
        self._connessione.cursor().execute(query)
        self._connessione.commit()
    
    def toDataframe(self, condizione: str = "") -> pd.DataFrame:
        """Restituisce un dataframe di prodotti corrispondenti alla condizione. Gli indici del df sono gli id dei prodotti nel db. 
        Se nessun argomento viene passato, viene restituito un dataframe con tutta la tabella

        Args:
            condizione (str): condizione di ricerca di prodotti
            default = "". In questo caso nessuna condizione viene inoltrata, viene stampato l'intera tabella

        Returns:
            pd.DataFrame: dataframe di prodotti. L'id del db è usato come indice
        """
        listaNuoviProdotti = []
        listaId = []
        cursore = self.ricercaPerParametro(condizione)
        
        # Creo una lista di prodotti
        for listaAttributi in cursore.fetchall(): 
            listaAttributi = list(listaAttributi)
            # Tolgo l'id
            listaId.append(listaAttributi.pop(0))
            # L'elemento all'indice 1 è il costo della materia prima, lo devo togliere 
            # Al costruttore di Prodotto deve essere passato solo il nome. 
            listaAttributi.pop(1)
            listaNuoviProdotti.append(Prodotto(*listaAttributi))
        
        # Uso la lista di prodotti per creare un dataframe 
        df = pd.DataFrame.from_records([prodotto.to_dict() for prodotto in listaNuoviProdotti])
        # Aggiungo la colonna degli Id 
        df["idProdotto"] = listaId
        # Uso la colonna degli id come colonna indice del df
        df = df.set_index("idProdotto")
        return df 


from InterpreteFileIni import InterpreteFileIni
if __name__ == "__main__": 
    interprete = InterpreteFileIni() 
    oggetto = interprete.leggiDaFile(os.path.dirname(__file__) + "/../dati/fileConfigurazione/esempio.ini")
    interfaccia = InterfacciaDatabase() 
    interfaccia.creaTabellaProdotti()
    interfaccia.stampaTabella("filoUsato > 1")
    # interfaccia.inserisciProdotto(oggetto) 
    # interfaccia.inserisciProdotto(oggetto2) 
    df = interfaccia.toDataframe("tempoLavoro>5")
    print(df)
    # interfaccia.aggiornaCampo(2, "tempoLavoro", 15)
    # interfaccia.stampaTabella()
    # print("Ora stampo la ricerca")
    # interfaccia.stampaDaCursore(interfaccia.ricercaPerParametro("acquirente='Ciccio Gamer'"))
    # interfaccia.stampaDaCursore(interfaccia.ricercaPerParametro("prezzoTotale > 10")) 
