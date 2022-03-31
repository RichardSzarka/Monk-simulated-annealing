from dataclasses import dataclass


@dataclass
class Garden:   # Triedy reprezentujúca záhradu
    corr_size: []   # Velkosť záhrady
    map: []     # Vykreslená mapa
    rating: int     # Ohodnotenie
    numberOfMoves: int      # Počet ciest mnícha

@dataclass
class Path:     # Trieda reprezentujúca jednu cestu
    number: int     # poradové číslo cesty
    enter: []       # Miesto vstupu cesty
    dir: int        # Smer cesty
