# Applicazione per la gestione e il tracciamento di prodotti ricamanti.
Applicazione a linea di comando che permette le operazioni base su un database di prodotti. Operazioni attualmente a disposizione:

# Come usare l'applicazione
1. Installare python ( e pip ) -> (TODO) Inserire link per il download
2. Installare i requirements -> (TODO) Fare file per i requirements
3. Aprire l'app in un terminale com `$ python __init__.py`

# Review delle funzionalità
Per una descrizione completa di ogni comando e delle sue funzionalità usare `$ help <nome comando>` o in alternativa `$ <nome comando> -h` all'interno dell'applicazione.
Per stampare la lista dei comandi a disposizione `$help`.

## Funzionalità di base
- Aggiungere un prodotto al database sia da linea di comando che da file ( con `$ aggiungi_prodotto` );
- Stampare la lista di prodotti nel database secondo condizioni sulle features del prodotto ( con `$ stampa_database` );
- Stampare un prodotto a partire dal suo id nel database ( con `$ stampa_prodotto <id>` ). Il prodotto può essere stampato a schermo o in un file; (Da finire)
- Modificare un campo di un prodotto esistente specificato tramite id ( con `$ aggiorna_campo <id>` );

## Funzionalità di utilità
- Cambiare il path della scrittura dei prodotti stampati ( con `$ cambia_path_scrittura <path>` );
- Stampare il nome dei campi dei prodotti e una breve descrizione ( con `$ stampa_campi` );
- Stampare la lista delle materie prime registrate e i loro prezzi ( con `$ stampa_materie` );

## Albero dei file

```bash
├── datiPersonali
│   ├── nuoviProdotti
│   │   └── esempio.ini
│   └── stampati
│       └──
```
- /datiPersonali/ -> Sono presenti i dati prodotti o inseriti dall'utente. L'utente dovrebbe cambiare i file **solo** in questa cartella.
    - /nuoviProdotti/ -> è dove si inseriscono i file .ini da leggere tramite il comando `$ aggiungi_prodotto`. All'interno è presente un file di esempio commentato.
    - /stampati/ -> è la cartella in cui di default vengono stampati i file con il comando `$ stampa_prodotto`


```bash
└── utilities
    ├── dati
    └── src
```
- /utilities/ -> Sono presenti i file privati dell'app (dati e codice).

```bash
    ├── dati
    │   ├── database
    │   ├── fileConfigurazione
    │   │   ├── esempio.ini
    │   │   └── pathScrittura.ini
    │   └── tipiMateriaPrima
    │       ├── prezziMateriaPrima.json
    │       └── readme.md
```
- /dati/ -> Dati privati dell'app.
    - /database/ -> Contiene il database con i prodotti.
    - /fileConfigurazione/ -> Contiene il file in cui viene salvato il path di scrittura per la stampa dei prodotti
    - /tipiMateriaPrima/ -> Contiene il json dei record di nomi e prezzi materie prime. **Attenzione, cancellando questo file non sarà possibile leggere il database all'interno dell'app! (vedi bug 1)**

```bash
    └── src
        ├── GestoreComandi.py
        ├── GestoreDatiMateriePrime.py
        ├── __init__.py
        ├── InterfacciaDatabase.py
        ├── InterpreteFileIni.py
        ├── main.py
        └── Prodotto.py
```
- /src/. Contiene il codice.
    - init.py -> Entrypoint per avviare l'app.
    - main.py -> Dove è definita la funzione main.
    - GestoreComandi.py -> Classe per il parsing e l'esecuzione dei comandi. ( Uso della libreria cmd ).
    - GestoreDatiMateriePrime.py -> Classe che si interfaccia con il file dei record delle materie prime.
    - InterfacciaDatabase.py -> Classe per l'interfaccia con il database.
    - InterpreteFileIni.py -> Classe per il parsing dei file .ini ( Uso della libreria configparser ).
    - Prodotto.py -> Classe che astrae un prodotto.

## Commento e spiegazione dei file .ini


# Bug trovati:
1. Se ho il database con degli oggetti ma il file prezziMateriaPrima è vuoto non sono in grado neanche di leggere il database con il comando `$ stampa_database`. Teoricamente non dovrebbe essere possibile
avere il database contente un tipo di prodotto non registrato nel json. Questo accade solo se si elimina manualmente il json senza eliminare il databse.
**Possibile soluzione**: Generare un warning che avvisi che i dati dei prodotti sono corrotti e avviare un ciclo per la lettura da linea di comando dei prezzi delle materie prime per ripristinarli.
Sollevare un'eccezione nel metodo `InterfacciaDatabase.generaListaProdottiDaCursore()` che viene catchata nel metodo `GestoreComandi.do_stampa_database()` e manda ad un loop di ripristino dei dati (lettura dei prezzi delle materie prime).

2. Non funziona il confronto tra date nel comando `$ stampa_database` quando si passa come query una condizione sulle date.
**Non è chiaro il perché. Da indagare**.

3. Nella funzione `GestoreComandi._creaPartser_stampa_prodotto()` voglio che l'argomento "idProdotto" sia required ma il metodo `add_argument` dice di non avere un argomento con la keyword "required".
**Da risolvere guardando la documentazione della libreria cmd**


# TODOS (non di codice)
- Inserire i link per scaricare python e pip
- Inserire i requirements per python.

# Funzionalità da inserire
- Comando per eliminare un prodotto dal database;
- Comando per resettare tutto e cancellare il db (e i dati delle materie prime);
- Comando per inserire/modificare/cancellare una materia prima manualmente; ( Così si può usare questo comando nella risoluzione del bug 1. )



