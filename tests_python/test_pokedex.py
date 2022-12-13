from pogoapi import Pokedex, Pokemon


def test_candy_distance():
    # Test evolutions of different forms of the same pokemon
    pokedex = Pokedex()
    assert pokedex.calculate_distance_to_evolve(Pokemon(745, 'Midday')) == 250
    assert pokedex.calculate_distance_to_evolve(Pokemon(745, 'Midnight')) == 250


def test_evolution_items():
    pokedex = Pokedex()
    # Test that Lickitung evolution requires Sinnoh Stone
    assert pokedex.evolutions.evolutions_by_pokemon[Pokemon(108, 'Normal')][0]['item_required'] == 'Sinnoh Stone'
    # Test chain of evolutions for Bulbasaur
    from_pokemon, chain = pokedex.convert_to_basic_pokemon_chain(Pokemon(3, 'Normal'))
    assert from_pokemon == Pokemon(1, 'Normal')
    assert len(chain) == 2
