import json 
import os.path
class GestoreDatiMateriePrime: 
    """
        Classe per la gestione dei tipi di materie prime.
        Questa classe deve essere l'unica che si interfaccia direttamente
        con il file json dei dati delle materie prime. 
        
        Permette di inserire un nuovo prodotto (con prezzo)
        e ottenere i prodotti attualmente presenti come dizionario
    """ 

    JSONPATH = os.path.dirname(__file__) + "/../dati/tipiMateriaPrima/prezziMateriaPrima.json"

    def __init__(self) -> None: 
        with open(self.JSONPATH) as jsonFile:
            self._dizionarioProdotti = json.load(jsonFile)
    
    @property 
    def dizionarioProdotti(self) -> dict: 
        return self._dizionarioProdotti

    def aggiungiTipoProdotto(self, nome: str, prezzo: float) -> None: 
        # Aggiungo il file alla struttura in memoria 
        self._dizionarioProdotti[nome] = prezzo
        # Aggiungo il file al json 
        with open(self.JSONPATH, "w") as jsonFile: 
            json.dump(self._dizionarioProdotti, jsonFile)



if __name__ == "__main__": 
    gestore = GestoreDatiMateriePrime() 
    print(gestore.dizionarioProdotti)
    print(type(gestore.dizionarioProdotti["TOTE_BAG"]))
    gestore.aggiungiTipoProdotto("Borsa_piccola", 5.0)