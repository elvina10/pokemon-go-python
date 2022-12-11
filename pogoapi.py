import requests
import json


def get_json(path):
    data = requests.get("https://pogoapi.net/api/v1/" + path)
    return json.loads(data.text)


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
        evolutions_by_id = {}
        for item in response:
            pokemon_id = item["pokemon_id"]
            evolutions_by_id[pokemon_id] = item["evolutions"]
        self.evolutions_by_id = evolutions_by_id

    def how_to_evolve(self, pokemon_id):
        response = []
        for key, evolutions in self.evolutions_by_id.items():
            for item in evolutions:
                if item["pokemon_id"] == pokemon_id:
                    response += [(key, item)]
        return response


class Pokedex:
    def __init__(self):
        self.buddy_distance = BuddyDistance()
        self.evolutions = Evolutions()

    def how_to_evolve(self, id):
        return self.evolutions.how_to_evolve(id)

    def calculate_distance_to_evolve(self, id):
        how_evolve = self.how_to_evolve(id)
        if not how_evolve:
            return None
        print(how_evolve)
        assert len(how_evolve) == 1
        form_pokemon_id, evolution = how_evolve[0]
        return self.buddy_distance.distance_per_id[form_pokemon_id] * evolution["candy_required"]