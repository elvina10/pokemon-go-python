from pogoapi import Pokedex


def test_candy_distance():
    # Test evolutions of different forms of the same pokemon
    pokedex = Pokedex()
    assert pokedex.calculate_distance_to_evolve(745, 'Midday') == 250
    assert pokedex.calculate_distance_to_evolve(745, 'Midnight') == 250


def test_evolution_items():
    pokedex = Pokedex()
    # Test that Lickitung evolution requires Sinnoh Stone
    assert pokedex.evolutions.evolutions_by_id[108][0]['item_required'] == 'Sinnoh Stone'