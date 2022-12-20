import requests
import json
from collections import defaultdict


class Pokemon:
    def __init__(self, pokedex_id, form, name):
        self.pokedex_id = pokedex_id
        self.form = form
        self.name = name

    def __hash__(self):
        return hash((self.pokedex_id, self.form))

    def __eq__(self, other):
        return self.pokedex_id == other.pokedex_id and self.form == other.form

    def __repr__(self):
        return f'#{self.pokedex_id} {self.name} {self.form}'


def get_json(path):
    data = requests.get("https://pogoapi.net/api/v1/" + path)
    return json.loads(data.text)


class PokemonForms:
    def __init__(self):
        response = get_json("pokemon_types.json")
        forms_by_id = defaultdict(list)
        for item in response:
            pokedex_id = item["pokemon_id"]
            form = item["form"]
            name = item["pokemon_name"]
            pokemon = Pokemon(pokedex_id, form, name)
            forms_by_id[pokedex_id].append(pokemon)
        self.forms_by_id = forms_by_id

    def forms_for_id(self, id):
        return [pokemon.form for pokemon in self.forms_by_id[id]]


class BuddyDistance:
    def __init__(self):
        response = get_json("pokemon_buddy_distances.json")
        distance_per_id = {}
        for key in response:
            items = response[key]
            for item in items:
                distance_per_id[item["pokemon_id"]] = item["distance"]
        self.distance_per_id = distance_per_id


class Evolutions:
    def __init__(self):
        response = get_json("pokemon_evolutions.json")
        evolutions_by_pokemon = {}
        for item in response:
            pokemon_id = item["pokemon_id"]
            form = item["form"]
            name = item["pokemon_name"]
            pokemon = Pokemon(pokemon_id, form, name)
            evolutions_by_pokemon[pokemon] = item["evolutions"]
        self.evolutions_by_pokemon = evolutions_by_pokemon

    def how_to_evolve(self, pokemon):
        response = []
        for from_pokemon, evolutions in self.evolutions_by_pokemon.items():
            for item in evolutions:
                # TODO type of evolutions should keep Pokemon, not these columsn separately
                if item["pokemon_id"] == pokemon.pokedex_id and item["form"] == pokemon.form:
                    response += [(from_pokemon, item)]
        return response


class Pokedex:
    def __init__(self):
        self.buddy_distance = BuddyDistance()
        self.evolutions = Evolutions()
        self.pokemon_forms = PokemonForms()

    def how_to_evolve(self, pokemon):
        return self.evolutions.how_to_evolve(pokemon)

    def convert_to_basic_pokemon_chain(self, pokemon):
        how_to_evolve = self.evolutions.how_to_evolve(pokemon)
        if not how_to_evolve:
            return [(pokemon, None)]
        print(how_to_evolve)
        _, evolution = how_to_evolve[0]
        for _, e in how_to_evolve:
            assert evolution == e
        from_pokemons = [f for f, _ in how_to_evolve]
        return self.convert_to_basic_pokemon_chain(from_pokemons[0]) + [(from_pokemons, evolution)]

    def calculate_distance_to_evolve(self, pokemon):
        how_evolve = self.how_to_evolve(pokemon)
        if not how_evolve:
            return None
        assert len(how_evolve) == 1
        from_pokemon, evolution = how_evolve[0]
        return self.buddy_distance.distance_per_id[from_pokemon.pokedex_id] * evolution["candy_required"]