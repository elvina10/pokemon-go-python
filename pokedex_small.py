import json
import requests


def name_from_names(names_json):
    return names_json["English"]


class Item:
    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        return self.json["id"]

    @property
    def name(self):
        return name_from_names(self.json["names"])

    def __repr__(self):
        return f"({self.id} {self.name})"


class Evolution:
    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        return self.json["id"]

    @property
    def candies(self):
        return self.json["candies"]

    @property
    def item(self):
        item = self.json["item"]
        if not item:
            return None
        else:
            return Item(item)

    @property
    def quests(self):
        return self.json["quests"]

    def __repr__(self):
        return f"{self.id} {self.candies} {self.item} {self.quests}"


class Entry:
    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        return self.json["id"]

    @property
    def dex_no(self):
        return self.json["dexNr"]

    @property
    def evolutions(self):
        evolutions = self.json["evolutions"]
        if not evolutions:
            return []
        return [Evolution(item) for item in evolutions]


def get_data_from_api():
    data = requests.get("https://pokemon-go-api.github.io/pokemon-go-api/api/pokedex.json")
    response = json.loads(data.text)
    response_per_id = {}
    for item in response:
        entry = Entry(item)
        response_per_id[entry.id] = entry
    return response_per_id


def get_id_per_dex_id(per_id):
    result = {}
    for key, entry in per_id.items():
        result[entry.dex_no] = key
    return result


class Pokedex:
    def __init__(self):
        self.pokedex_per_id = get_data_from_api()
        self.id_per_dex_id = get_id_per_dex_id(self.pokedex_per_id)

    def get(self, id):
        return self.pokedex_per_id[id]

    def get_dex_no(self, no):
        return self.get(self.id_per_dex_id[no])

    def how_to_evolve_dex_no(self, no):
        idx = self.id_per_dex_id[no]
        result = []
        for key, pokemon_entry in self.pokedex_per_id.items():
            result += [(key, x) for x in pokemon_entry.evolutions if x.id == idx]
        return result
