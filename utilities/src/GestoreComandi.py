from InterpreteFileIni import InterpreteFileIni
from Prodotto import leggiProdottoDaInput 
from InterfacciaDatabase import InterfacciaDatabase
import os
import configparser as c
import cmd

db = InterfacciaDatabase()
interprete = InterpreteFileIni() 

# TODO aggiungi_prodotto -f pathfile.ini
# TODO stampa_database 
# TODO cerca_database 

class GestoreComandi(cmd.Cmd): 
    """
        Classe di gestione comandi 
    """

    intro = ( "Linea di comando per gestione ricami. Digitare help o ? per stampare la lista dei comandi. \n" + 
              "Digitare help comando per avere una descrizione del comando.\n" + 
              "Digitare esci o ctrl + d per uscire. \n \n"
    )     

    prompt = "$ "

    def do_stampa_argomenti(self, arg: str) -> None: 
        print(arg)

    def preloop(self) -> None:
        pathDefault = os.path.dirname(__file__) + "/../dati/stampati/"
        self.pathFileConfigurazione = os.path.dirname(__file__) + "/../dati/fileConfigurazione/pathScrittura.ini"
        parser = c.ConfigParser() 
        # Se il file esiste 
        if os.path.exists(self.pathFileConfigurazione):
            parser.read(self.pathFileConfigurazione)
            try: 
                if parser["PATH"]["value"]: 
                    # Se il campo non è vuoto 
                    self.pathScrittura = parser["PATH"]["value"]
                else: 
                    self.pathScrittura = pathDefault
            except KeyError: 
                print("Errore nella lettura del file di configurazione pathScrittura.ini, il valore 'path' non è presente.")
        
    def do_esci(self, arg: str) -> bool: 
        """Esce dal programma"""
        print("Esco dal programma") 
        return True
    def do_EOF(self, arg: str) -> bool:
        """Stesso funzionamento di esci"""
        return self.do_esci(arg)
    
    def do_aggiungi_prodotto(self, arg: str) -> None: 
        """Comando per aggiungere un prodotto

        Opzioni:
            -f <pathFile>: aggiungere prodotto da file (da implementare)
        """
        self._aggiungiProdottoDaInput()
    
    def do_cambia_path_scrittura(self, arg: str) -> None: 
        """Cambia path per la scrittura dei prodotti stampati. Di default è dati/stampati/""" 
        print()
        print("Attualmente il path di scrittura dei nuovi file è: ")
        print(self.pathScrittura)
        nuovoPath = input("Inserire nuovo path (inserire il path completo): \n")
        if os.path.isdir(nuovoPath):
            # Cambio la variabile 
            self.pathScrittura = nuovoPath
            # Scrivo su file 
            parser = c.ConfigParser() 
            parser["PATH"] = {}
            parser["PATH"]["value"] = nuovoPath
            with open(self.pathFileConfigurazione, "w") as f:
                parser.write(f)
        else: 
            print("Path inserito non valido.")
         
    def do_stampa_database(self, arg: str) -> None: 
        """Stampa 

        Opzioni: 
            -c <criterio di ricerca>: stampa solo i prodotti nel db corrispondenti al criterio
                                    Esempio:
                                        tempoLavoro > 5
                                        guadagno > 10 
                                        dataCommissione = 20-10-10
        """
        if not arg: 
            print("Stampo la tabella con tutti i prodotti")
            db.stampaTabella()
        elif arg[0] == "-c": 
            if arg[1]: db.stampaTabella(arg[1:])
            else: print("Errore, utilizzo: \nstampa_database -c <condizione>")
                
        
    def _aggiungiProdottoDaInput(self) -> None: 
        """
        Comando per aggiungere un prodotto
        """
        print()
        print("Aggiungo un prodotto da input")
        nuovoProdotto = leggiProdottoDaInput()  
        print("Stampo il nuovo prodotto: ") 
        print(nuovoProdotto)
        risposta = input("Corretto? Salvo nel database? [S]i/[N]o \n")
        risposta = risposta.lower().strip()
        if risposta in ["s", "si", "yes", "y"]:
            print("Salvo nel database...")
            idProdotto = db.inserisciProdotto(nuovoProdotto)
            print("Oggetto aggiunto al database con id " + str(idProdotto))
            risposta = input("Stampare i dati dell'oggetto su un file? [S]i/[N]o \n")
            risposta = risposta.lower().strip()
            if risposta in ["s", "si", "yes", "y"]:
                print("Stampo l'oggetto.")
                interprete.scriviProdottoSuFile(nuovoProdotto, self.pathScrittura + "prodotto" + str(idProdotto) + ".ini")
                print("Oggetto salvato in: " + self.pathScrittura)
        
            
        