import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone
from pokemon_entities.models import Pokemon
from pokemon_entities.models import PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, pokemon_entity_info, image_url=DEFAULT_IMAGE_URL):
    if pokemon['level']:
        popup_message = 'Ур: {0}<br/>Зд: {1}<br/>Сил:{2}<br/>Защ:{3}<br/>Вын:{4}'.format(
            pokemon_entity_info['level'], pokemon_entity_info['health'], pokemon_entity_info['strength'],
            pokemon_entity_info['defence'], pokemon_entity_info['stamina'])
    else:
        popup_message = 'Нет данных'
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [pokemon_entity_info['latitude'], pokemon_entity_info['longitude']],
        tooltip=pokemon_entity_info['title'],
        icon=icon,
        popup=popup_message
    ).add_to(folium_map)


def show_all_pokemons(request):
    '''return dictionary about all pokemons with short information'''
    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.filter(
        appear_at__lte=timezone.now(), disappear_at__gte=timezone.now()).select_related('pokemon')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        pokemon_entity_info = {
            'title': pokemon_entity.pokemon.title,
            'latitude': pokemon_entity.latitude,
            'longitude': pokemon_entity.longitude,
            'level': pokemon_entity.level,
            'health': pokemon_entity.health,
            'strength': pokemon_entity.strength,
            'defence': pokemon_entity.defence,
            'stamina': pokemon_entity.stamina,
        }
        add_pokemon(folium_map, pokemon_entity_info,
                    pokemon_entity.pokemon.image_url)

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
        requested_pokemon = Pokemon.objects.select_related('previous_evolution').prefetch_related(
            'next_evolution', 'element_type', 'element_type__strong_against').get(id=int(pokemon_id))
    except Pokemon.DoesNotExist as no_pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    requested_pokemon_entities = PokemonEntity.objects.filter(
        pokemon=requested_pokemon, appear_at__lte=timezone.now(),
        disappear_at__gte=timezone.now())

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon_entities:
        pokemon_entity_info = {
            'title': requested_pokemon.pokemon.title,
            'latitude': pokemon_entity.latitude,
            'longitude': pokemon_entity.longitude,
            'level': pokemon_entity.level,
            'health': pokemon_entity.health,
            'strength': pokemon_entity.strength,
            'defence': pokemon_entity.defence,
            'stamina': pokemon_entity.stamina,
        }
        add_pokemon(folium_map, pokemon_entity_info,
                    requested_pokemon.image_url)

    if requested_pokemon.previous_evolution:
        requested_previous_evolution = requested_pokemon.previous_evolution
        previous_evolution = {
            'pokemon_id': requested_previous_evolution.id,
            'img_url': requested_previous_evolution.image.url if requested_previous_evolution.image else None,
            'title_ru': requested_previous_evolution.title, }

    next_evolution_set = requested_pokemon.next_evolution.all()
    if next_evolution_set:
        next_evolution = {
            'pokemon_id': next_evolution_set[0].id,
            'img_url': next_evolution_set[0].image.url if next_evolution_set[0].image else None,
        }

    if requested_pokemon.element_type:
        element_type = []
        for element in requested_pokemon.element_type.all():
            element_type.append({'title': element.title,
                                 'img': element.image.url if element.image.url else None,
                                 'strong_against': element.strong_against.all(), })

    pokemon_on_page = {
        'pokemon_id': requested_pokemon.id,
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'img_url': requested_pokemon.image.url if requested_pokemon.image else None,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution,
        'element_type': element_type,
    }

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon_on_page})
