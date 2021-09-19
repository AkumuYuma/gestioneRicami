from InterpreteFileIni import InterpreteFileIni
from Prodotto import leggiProdottoDaInput 
from InterfacciaDatabase import InterfacciaDatabase
import os
import configparser as c
import cmd
import argparse as ap 

db = InterfacciaDatabase()
interprete = InterpreteFileIni() 


# TODO aggiorna elemento nel db

class GestoreComandi(cmd.Cmd): 
    """
        Classe di gestione comandi 
    """

    intro = ( "Linea di comando per gestione ricami. Digitare help o ? per stampare la lista dei comandi. \n" + 
              "Digitare help comando per avere una descrizione del comando.\n" + 
              "Digitare esci o ctrl + d per uscire. \n \n"
    )     

    prompt = "$ "


    """Prova utilizzo argparse"""
    __test1_parser = ap.ArgumentParser(prog="franco") 
    # L'argomento help qui è la stringa di aiuto per l'opzione --bar
    __test1_parser.add_argument("--bar", help="questa è la stringa di help per l'opzione --bar")
    # Questo metodo viene chiamato quando chiami help test1
    def help_test1(self): 
        # Questo viene stampato per primo. Metti qui il funzionamento generico del comando 
        print("Questo è l'aiuto di test1")
        # Questo stampa l'usage del comando, tutte le opzioni e l'help delle opzioni.
        self.__test1_parser.print_help()
    def do_test1(self, line: str) -> None: 
        # Devo usare il try perchè altrimenti se viene usato male esce dal programma 
        # Invece così se sollevo l'eccezione semplicemente ritorno al command loop 
        # Nota: Comunque bisogna scrivere gli argomenti tutti attaccati perchè sto usando il metodo split
        try: 
            parsed = self.__test1_parser.parse_args(line.split())
        except SystemExit:
            return 
        print("Test1...")
        print(parsed.bar)
        print(parsed)

        


    def preloop(self) -> None:
        pathDefault = os.path.dirname(__file__) + "/../../datiPersonali/stampati/"
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
        self._creaParser_aggiungi_prodotto()
        

    def do_esci(self, arg: str) -> bool: 
        """Esce dal programma"""
        print("Esco dal programma") 
        return True
    def do_EOF(self, arg: str) -> bool:
        """Stesso funzionamento di esci"""
        return self.do_esci(arg)
    

    # funzione help per il comando aggiungi_prodotto
    def help_aggiungi_prodotto(self) -> None: 
        print("""Comando per aggiungere un prodotto, se nessuna opzione specificata, aggiunge da input""")
        self._aggiungi_prodotto_parser.print_help()
    def do_aggiungi_prodotto(self, arg: str) -> None: 
        """Comando per aggiungere un prodotto

        Opzioni:
            -f <pathFile>: aggiungere prodotto da file (da implementare)
            --no-absolute: deve essere specificato l'intero path del file, se non usata basta usare solo il nome del file
        """
        try: 
            parsed = self._aggiungi_prodotto_parser.parse_args(arg.split())
        except SystemExit: 
            return 
        
        if parsed.file: 
            self._aggiungiProdottoDaFile(parsed.file, parsed.relative)
        else: 
            self._aggiungiProdottoDaInput()
    

    # TODO Inserire opzione per ritornare alle impostazioni iniziali del path di scrittura
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
         
    # TODO Usare argparse
    def do_stampa_database(self, arg: str) -> None: 
        """Stampa 

        Opzioni: 
            -c <criterio di ricerca>: stampa solo i prodotti nel db corrispondenti al criterio
                                    Esempio:
                                        tempoLavoro > 5
                                        guadagno > 10 
                                        dataCommissione = 20-10-10
        """
        listaArgomenti = arg.strip().split()
        if not arg: 
            print("Stampo la tabella con tutti i prodotti")
            db.stampaTabella()
        elif listaArgomenti[0] == "-c": 
            if listaArgomenti[1]: db.stampaTabella(listaArgomenti[1])
            else: print("Errore, utilizzo: \nstampa_database -c <condizione>")
                
        
    def _aggiungiProdottoDaInput(self) -> None: 
        """
        Comando per aggiungere un prodotto
        """
        try:
            print()
            print("Aggiungo un prodotto da input. CTRL-d in qualsiasi momento per interrompere")
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
        except EOFError: 
            print("Comando interrotto. \n")
            print()
            return 
    
    def _aggiungiProdottoDaFile(self, nomeFile: str, pathRelativo : bool = True) -> None: 
        """Aggiunge un prodotto dal file specificato 

        Args:
            path (str): path del file. 
            pathRelativo (bool, optional): se a True, utilizza l'argomento path solo come nome del file.
            Altrimenti legge path come path assoluto del file. 
            Defaults to True.
        """
        if pathRelativo: 
            # Se pathRelativo è vero uso il path di default e aggiungo solo il nome del file
            pathDefault = os.path.dirname(__file__) + "/../../datiPersonali/nuoviProdotti/"
            pathAssoluto = pathDefault + nomeFile
        else:
            # Altrimenti il pathAssoluto sarà dato come argomento
            pathAssoluto = nomeFile
        print()
        print("Leggo il prodotto dal file passato")
        nuovoProdotto = interprete.leggiDaFile(pathAssoluto)
        print(nuovoProdotto)
        risposta = input("Corretto? Salvo nel database? [S]i/[N]o \n")
        risposta = risposta.lower().strip()
        if risposta in ["s", "si", "yes", "y"]:
            print("Salvo nel database...")
            idProdotto = db.inserisciProdotto(nuovoProdotto)
            print("Oggetto aggiunto al database con id " + str(idProdotto))
        
    # Metodi privati di argparse 
    def _creaParser_aggiungi_prodotto(self) -> None: 
        """
        Crea le variabili di istanza per il parsing degli argomenti del comando aggiungi_prodotto
        """
        self._aggiungi_prodotto_parser = ap.ArgumentParser(prog="aggiungi_prodotto")
        # Opzioni per aggiungere da file
        self._aggiungi_prodotto_parser.add_argument("-f", "--file", type=str, help = "utilizzo: aggiungi_prodotto -f <path>: aggiungi prodotto da file")
        # Opzione per specificare path relativo o assoluto 
        self._aggiungi_prodotto_parser.add_argument("--relative", dest="relative", action="store_true", help="""Permette di utilizzare come path il path relativo, non è necessario specificarla,
                                            di default è già attiva. Per disattivare vedi --no-relative""")
        self._aggiungi_prodotto_parser.add_argument("--no-relative", dest="relative", action="store_false", help="""Da usare in combinazione con -f. Se viene usata, è necessario specificare il path completo del file.
                                            Altrimenti basta specificare il nome del file inserendolo nella cartella /dati/nuoviProdotti.""")
        # Di default uso il path relativo 
        self._aggiungi_prodotto_parser.set_defaults(relative=True)
        