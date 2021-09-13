from Prodotto import Prodotto
import sqlite3 as sql
import datetime as d
import re

class InterfacciaDatabase: 
    """
        Classe di interfaccia con il database. Deve implementare tutte le query per il db. 
        Si vuole renderla il più indipendente possibile dalla scelta di sqlite. (Eventualmente migrabile su mysql)
    """
    
    DATABASEPATH = "./dati/database/prodotti.db"

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
    
    def inserisciProdotto(self, oggetto: Prodotto) -> None: 
        """Inserisce una riga nella tabella a partire dall'oggetto prodotto

        Args:
            oggetto (Prodotto): Prodotto da inserire
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
        self._inoltraQuery("INSERT INTO Prodotti (" + listaAttributi + ")" + 
                          "VALUES (" + listaValoriAttributi + ")")
        
        # Confermo i cambiamenti
        self._connessione.commit()

    def _inoltraQuery(self, query: str) -> None: 
        """
            Inoltra al db la query passata come stringa in linguaggio sql 
        """
        return self._connessione.cursor().execute(query)

    def stampaTabella(self) -> None: 
        """
            Stampa la tabella Prodotti
        """
        cursore = self._inoltraQuery("SELECT * FROM Prodotti")
        for nomeColonna in cursore.description: 
            print(str(nomeColonna[0]) + "|", end="")
        print()
        for row in cursore: 
            for value in row: 
                print(str(value) + "|", end="")
            print() 

    def ricercaPerParametro(self, condizione: str) -> sql.Cursor:
        """Inoltra una query per selezionare solo gli oggetti specificati nella condizione

        Args:
            condizione (str, optional): Condizione della query 
                        Esempio : prezzototale > 10 
                        Esempio : tipoProdotto = 'TOTE_BAG'  

        Raises:
            ValueError: Se la colonna su cui si vuole applicare la condizione non esiste

        Returns:
            sql.Cursor: Cursore con il risultato della ricerca. 
        """
        
        # Controllo che il parametro sia tra le colonne
        # Seleziono il parametro splittando la stringa al primo carattere non alfanumerico
        parametro = re.split("[^\w\d]", condizione)[0]
        if parametro not in [nomeParametro[0] for nomeParametro in self._inoltraQuery("SELECT * FROM Prodotti").description]:
            raise ValueError("Errore, la colonna su cui eseguire la condizione non esiste")
        cursore = self._inoltraQuery("SELECT * FROM Prodotti WHERE " + condizione) 
        return cursore 
    
    def stampaDaCursore(self, cursore: sql.Cursor) -> None:
        """Stampa nella posizione in cui si trova il cursore, utilizzato dopo una ricerca
           per stampare il risultato 

        Args:
            cursore (sql.Cursor): cursore con risultato della ricerca
        """
        for row in cursore.fetchall():
            for value in row:
                print(str(value) + "|" , end="")
            print()
         
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
    
    def ottieniProdottidaDbComeLista(self, condizione: str) -> list:
        """Restituisce una lista di prodotti corrispondenti alla condizione

        Args:
            condizione (str): condizione di ricerca di prodotti

        Returns:
            list[Prodotto]: lista di prodotti corrispondenti alla ricerca
        """
        listaNuoviProdotti = []
        cursore = self.ricercaPerParametro(condizione)
        for listaAttributi in cursore.fetchall(): 
            listaAttributi = list(listaAttributi)
            listaAttributi.pop(0)
            listaAttributi.pop(2)
            listaNuoviProdotti.append(Prodotto(*listaAttributi))
        return listaNuoviProdotti 

from creaProdottoDaFile import Interprete
if __name__ == "__main__": 
    interprete = Interprete() 
    oggetto = interprete.leggiDaFile("./dati/fileConfigurazione/provadb.ini")
    oggetto2 = interprete.leggiDaFile("./dati/fileConfigurazione/esempio.ini")
    interfaccia = InterfacciaDatabase() 
    interfaccia.creaTabellaProdotti()
    listaProdotti = interfaccia.ottieniProdottidaDbComeLista("tempoLavoro>39")
    for prodotto in listaProdotti: 
        print(prodotto)
    # interfaccia.inserisciProdotto(oggetto) 
    # interfaccia.inserisciProdotto(oggetto2) 
    # interfaccia.aggiornaCampo(2, "tempoLavoro", 15)
    # interfaccia.stampaTabella()
    # print("Ora stampo la ricerca")
    # interfaccia.stampaDaCursore(interfaccia.ricercaPerParametro("acquirente='Ciccio Gamer'"))
    # interfaccia.stampaDaCursore(interfaccia.ricercaPerParametro("prezzoTotale > 10")) 


# TODO Trova prodotto secondo una condizione, usare il cursore per creare e restituire
#       un array di oggetti prodotto che rispettano la condizione e stamparli a schermo 
#       così poi si può chiedere di stamparli su file