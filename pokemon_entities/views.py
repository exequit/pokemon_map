import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon
from pokemon_entities.models import PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    '''return dictionary about all pokemons with short information'''
    with open("pokemon_entities/pokemons.json") as database:
        pokemons = json.load(database)['pokemons']

    pokemon_entities = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        current_pokemon = pokemon_entity.pokemon
        add_pokemon(
            folium_map, pokemon_entity.latitude, pokemon_entity.longitude,
            current_pokemon.title, current_pokemon.image.path)

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.image.url if pokemon.image else None,
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    '''return dictionary about current pokemon with information'''
    previous_evolution = None
    next_evolution = None

    try:
        requested_pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except Pokemon.DoesNotExist as no_pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    requested_pokemon_entities = PokemonEntity.objects.filter(
        pokemon=requested_pokemon)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.latitude, pokemon_entity.longitude,
            requested_pokemon.title, requested_pokemon.image.path)

    if (requested_pokemon.previous_evolution):
        previous_evolution = {
            'pokemon_id': requested_pokemon.previous_evolution.id,
            'img_url': requested_pokemon.previous_evolution.image.url if requested_pokemon.previous_evolution.image else None,
            'title_ru': requested_pokemon.previous_evolution.title, }
    if (requested_pokemon.next_evolution.all()):
        next_evolution = {
            'pokemon_id': requested_pokemon.next_evolution.get().id,
            'img_url': requested_pokemon.next_evolution.get().image.url if requested_pokemon.next_evolution.get().image else None,
            'title_ru': requested_pokemon.next_evolution.get().title, }

    pokemon_on_page = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en if requested_pokemon.title_en else '',
        'title_jp': requested_pokemon.title_jp if requested_pokemon.title_jp else '',
        'description': requested_pokemon.description if requested_pokemon.description else '',
        'img_url': requested_pokemon.image.url if requested_pokemon.image else None,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution,
    }

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_on_page})
