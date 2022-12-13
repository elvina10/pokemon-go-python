from trainer import Trainer
from pogoapi import Pokedex


def just_copy(from_file, to_file):
    trainer = Trainer(from_file)
    trainer.save(to_file)


def sum_of_candies_to_evolve(pokedex, pokemon):
    chain = pokedex.convert_to_basic_pokemon_chain(pokemon)
    needed_candy = 0
    for item in chain:
        print(item)
        from_pokemons, evolution = item
        needed_candy += evolution['candy_required']
    return needed_candy


def calculate_distance_for_unowned(file):
    trainer = Trainer(file)
    pokedex = Pokedex()
    result = []
    for _, pokemon_forms in pokedex.pokemon_forms.forms_by_id.items():
        for pokemon in pokemon_forms:
            #TODO: Check all the forms here
            if trainer.is_caught(pokemon.pokedex_id):
                print('Trainer has already caught pokemon ', pokemon.pokedex_id)
            else:
                if pokemon.pokedex_id in trainer.status_by_id:
                    candy_count = trainer.status_by_id[pokemon.pokedex_id]["candy_count"]
                else:
                    candy_count = 0
                needed_candy = sum_of_candies_to_evolve(pokedex, pokemon)
                missing_candy = needed_candy - candy_count
                distance = missing_candy * pokedex.buddy_distance.distance_per_id[pokemon.pokedex_id]
                result += [(pokemon, missing_candy, distance)]
    return result

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(calculate_distance_for_unowned('current_pokemons'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
