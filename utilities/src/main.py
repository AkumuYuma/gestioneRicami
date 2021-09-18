from GestoreComandi import GestoreComandi
from InterfacciaDatabase import InterfacciaDatabase


def main() -> None: 
    InterfacciaDatabase().creaTabellaProdotti()
    GestoreComandi().cmdloop()
    
