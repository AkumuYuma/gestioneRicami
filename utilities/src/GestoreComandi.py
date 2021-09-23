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
        self._creaParser_cambia_path_scrittura()
        self._creaParser_stampa_database()
        self._creaParser_aggiorna_campo()
    
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

    def help_cambia_path_scrittura(self) -> None:
        print("""Cambia path per la scrittura dei prodotti stampati. Di default è dati/stampati/""")
        self._cambia_path_scrittura_parser.print_help()
    def do_cambia_path_scrittura(self, arg: str) -> None: 
        """Cambia path per la scrittura dei prodotti stampati. Di default è dati/stampati/""" 
        try: 
            parsed = self._cambia_path_scrittura_parser.parse_args(arg.split())
        except SystemExit: 
            return 
        
        if parsed.reset: 
            print() 
            print("Attualmente il path di scrittura dei nuovi file è: ")
            print("Resetto il path di scrittura a quello di default.")
            pathDefault = os.path.dirname(__file__) + "/../../datiPersonali/stampati/"
            # Cambio il path in live
            self.pathScrittura = pathDefault 
            # E modifico il file 
            parser = c.ConfigParser() 
            parser["PATH"] = {}
            parser["PATH"]["value"] = ""
            with open(self.pathFileConfigurazione, "w") as f:
                parser.write(f)
        else: 
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
         
    def help_stampa_database(self) -> None: 
        print("Stampa i prodotti nel database. Senza opzioni stampa tutta la tabella")
        print(self._stampa_database_parser.print_help())
    def do_stampa_database(self, arg: str) -> None: 
        """Stampa 

        Opzioni: 
            -c <criterio di ricerca>: stampa solo i prodotti nel db corrispondenti al criterio
                                    Esempio:
                                        tempoLavoro > 5
                                        guadagno > 10 
                                        dataCommissione = 20-10-10
        """
        try: 
            parsed = self._stampa_database_parser.parse_args(arg.split())
        except SystemExit: 
            return 

        try: 
            if not parsed.condition: 
                print("Stampo la tabella con tutti i prodotti")
                db.stampaTabella()
            else:
                db.stampaTabella(parsed.condition)
        except ValueError: 
            print("Errore, la condizione specificata non è valida")
            return 
    
    
    def help_aggiorna_campo(self) -> None: 
        print("Aggiorna un campo nel database. I parametri non specificati nelle opzioni verranno presi interattivamente")
        print("Per visualizzare il nome corretto di ogni campo, usare stampa_campi")
        self._aggiorna_campo_parser.print_help()
    def do_aggiorna_campo(self, arg: str) -> None: 
        """Aggiorna un campo nel database."""
        try: 
            parsed = self._aggiorna_campo_parser.parse_args(arg.split())
        except SystemExit: 
            return 
        
        self._aggiornaCampoInterattivo(parsed.idProdotto, parsed.campo, parsed.valore)
    
    def do_stampa_campi(self, arg: str) -> None: 
        """
        Stampa una lista con il nome di ogni campo dei prodotti e una breve descrizione. 
        I nomi qui listati sono quelli che vanno passati come argomento --campo al comando aggiorna_prodotto
        """
        print()
        print("Stampo la lista dei campi modificabili con una breve descrizione.")
        print("------------------------------------------------------------------")
        print("Nome del campo: tipoProdotto.")
        print("Descrizione: Tipo di materia prima che si utilizza. Se si inserisce un nuovo tipo, esso verrà registrato automaticamente.")
        print()
        print("Nome del campo: dataCommissione.") 
        print("Descrizione: Data di commissione del lavoro nel formato aa-mm-gg.")
        print()
        print("Nome del campo: dataInizio.") 
        print("Descrizione: Data di inizio del lavoro nel formato aa-mm-gg. Attenzione, non si può settare una data di inizio precedente alla data di commissione")
        print()
        print("Nome del campo: dataFine.") 
        print("Descrizione: Data di fine del lavoro nel formato aa-mm-gg. Attenzione, non si può settare una data di fine precedente alla data di inizio")
        print()
        print("Nome del campo: tempoLavoro.")
        print("Descrizione: Tempo di lavoro impiegato a completare il prodotto, in ore. Necessario per il calcolo del guadagno Orario")
        print()
        print("Nome del campo: filoUsato.")
        print("Descrizione: Quantità di filo utilizzato per completare il lavoro. In numero di matasse. Può essere anche non intero. Necessario per il calcolo del guadagno.")
        print()
        print("Nome del campo: costoFilo.")
        print("Descrizione: Costo del filo (in euro) a matassa. Di default è sempre a 1 ma è modificabile nel caso si utilizzino fili di diverso prezzo. Necessario per il calcolo del guadagno.")
        print()
        print("Nome del campo: prezzoTotale.")
        print("Descrizione: Prezzo a cui il prodotto è stato venduto, necessario per il calcolo del guadagno.")
        print()
        print("Nome del campo: acquirente.")
        print("Descrizione: Acquirente del prodotto. Può essere una stringa qualsiasi, di default è una stringa vuota.")
        print("------------------------------------------------------------------")
        print()
        print("Gli altri campi non sono modificabili.")
        print()


    # Metodi privati
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
    
    
    def _aggiornaCampoInterattivo(self, valoreIdProdotto: int = None, valoreCampo:str = None, valoreNuovoValore = None) -> None: 
        """Aggiorna il campo voluto interattivamente. Chiede da input i campi mancanti

        Args:
            valoreIdProdotto (int, optional): [idProdotto da modificare]. Defaults to None.
            valoreCampo (str, optional): [campo da modificare nel db]. Defaults to None.
            valoreNuovoValore ([type], optional): [nuovo valore da inserire]. Defaults to None.

        Raises:
            EOFError: [Se l'id del prodotto non è valido]
        """
        try: 
            print()
            print("Inserimento dei campi mancanti da input. ctrl-d per interrompere")
            if not valoreIdProdotto: 
                try: 
                    valoreIdProdotto = int(input("Inserire id del prodotto da aggiornare: \n"))
                except:
                    print("Id prodotto non valido, interrompo.")
                    raise EOFError
            if not valoreCampo: 
                valoreCampo = input("Inserire campo da modificare nel database: \n")
            if not valoreNuovoValore: 
                valoreNuovoValore = input("Inserire nuovo valore: \n")
            
            try: 
                db.aggiornaCampo(valoreIdProdotto, valoreCampo, valoreNuovoValore)
                print()
                print("Operazione effettuata con successo, stampo il prodotto modificato.")
                print()
                risultato = InterfacciaDatabase.generaListaProdottiDaCursore(db._inoltraQuery(f"SELECT * FROM Prodotti WHERE idProdotto={valoreIdProdotto}"))
                prodottoModificato = risultato[1][0]
                print("Id prodotto: " + str(risultato[0][0]))
                print(prodottoModificato)
            except Exception as e: 
                print("Errore, nell'aggiornamento del prodotto. Stampo i dettagli: ")
                print(e)
        except EOFError: 
            print("Comando interrotto.")
            return 
        
    # Metodi privati per l'uso di argparse 
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
        
    def _creaParser_cambia_path_scrittura(self) -> None: 
        self._cambia_path_scrittura_parser = ap.ArgumentParser(prog="Cambia path scrittura")
        self._cambia_path_scrittura_parser.add_argument("-r", "--reset", dest="reset", action="store_true", help="Resetta il path di scrittura dei nuovi file a quello di defualt.")
        self._aggiungi_prodotto_parser.set_defaults(reset=False)
    
    def _creaParser_stampa_database(self) -> None: 
        self._stampa_database_parser = ap.ArgumentParser(prog="Stampa database con query")
        self._stampa_database_parser.add_argument("-c", "--condition", type=str, help="""
            -c <criterio di ricerca>: stampa solo i prodotti nel db corrispondenti al criterio
                                    Esempio:
                                        tempoLavoro > 5
                                        guadagno > 10 
                                        dataCommissione = 20-10-10""") 
    
    def _creaParser_aggiorna_campo(self) -> None: 
        self._aggiorna_campo_parser = ap.ArgumentParser(prog="Aggiorna un campo nel db usando l'id")
        self._aggiorna_campo_parser.add_argument("--idProdotto", type=int, help="Id del prodotto da cambiare")
        self._aggiorna_campo_parser.add_argument("--campo", type=str, help="Campo da cambiare. Per sapere il nome corretto usare il comando stampa_campi")
        self._aggiorna_campo_parser.add_argument("--valore", help="Nuovo valore da inserire")