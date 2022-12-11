from pogoapi import Pokedex


def test_creation():
    pokedex = Pokedex()
    print(pokedex.evolutions.evolutions_per_id[108])
    print(pokedex.how_to_evolve(740))
    print(pokedex.calculate_distance_to_evolve(740))
    print(pokedex.calculate_distance_to_evolve(463))
    assert False