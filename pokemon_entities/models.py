from django.db import models


class PokemonElementType(models.Model):
    """The PokemonElementType object contains pokemon element types and their characteristic features.

    The PokemonElementType model uses for containing pokemon element types with their features like name, 
    image and info about which element which elements (may be zero, one or greater then one) this element 
    is strong against.

    To create pokemon element type you can use this example:
    > PokemonElementType.objects.create(title="Normal") 
    """

    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка', blank=True,
                              null=True, upload_to="elements")
    strong_against = models.ManyToManyField(
        "PokemonElementType", verbose_name='Силён против', blank=True)

    def __str__(self):
        return "{title}".format(title=self.title)


class Pokemon(models.Model):
    """The Pokemon object contains pokemon species and characteristic features of pokemon.

    The Pokemon model uses for containing pokemon species with their features like name, image, 
    common description, previous and next evolution stage, pokemon element types.
    The Pokemon model is in relative with PokemonEntity model and PokemonElementtype model
    respectively by field previous_evolution and field element type. The next evolution is getting
    from previous evolution of Pokemon object. The Pokemon object may have many element types.   

    To create new pokemon specie you can use this example:
    > Pokemon.objects.create(title="Pikachu")
    """

    title = models.CharField('Имя', max_length=200)
    title_en = models.CharField(
        'Имя (англ.)', max_length=200, blank=True, default="")
    title_jp = models.CharField(
        'Имя (яп.)', max_length=200, blank=True, default="")
    description = models.TextField('Описание', blank=True, default="")
    image = models.ImageField('Картинка', blank=True, null=True)
    element_type = models.ManyToManyField(PokemonElementType, blank=True)
    previous_evolution = models.ForeignKey(
        "Pokemon", on_delete=models.SET_NULL, verbose_name='Из кого эволюционировал',
        blank=True, null=True, related_name="next_evolution")

    def __str__(self):
        return "{title}".format(
            title=self.title
        )


class PokemonEntity(models.Model):
    """The PokemonEntity object contains pokemons entities and their characteristic features.

    The PokemonEntity model uses for containing existing pokemon entities with their features 
    like coordinates in map, appear and disappear datetime, level, health,strength, defence,
    stamina for current pokemon entity. The PokemonEntity model is in relative with Pokemon model
    by field pokemon and uses Pokemon object for specifing pokemon specie with current entity. 

    To create new pokemon entity you can use this example:
    > current_pokemon = Pokemon.objects.get(title="Pikachu")
    > PokemonEntity.objects.create(pokemon=current_pokemon,latitude=55.5,longitude=37.6)
    """

    pokemon = models.ForeignKey(
        Pokemon, verbose_name='Покемон', on_delete=models.PROTECT)
    latitude = models.FloatField('Ширина')
    longitude = models.FloatField('Долгота')
    appear_at = models.DateTimeField(
        'Появится в', blank=True, default=None, null=True)
    disappear_at = models.DateTimeField(
        'Пропадет в', blank=True, default=None, null=True)
    level = models.IntegerField('Уровень', blank=True, default=0)
    health = models.IntegerField('Здоровье', blank=True, default=0)
    strength = models.IntegerField('Атака', blank=True, default=0)
    defence = models.IntegerField('Защита', blank=True, default=0)
    stamina = models.IntegerField('Выносливость', blank=True, default=0)

    def __str__(self):
        return "{pok}({lat};{lon})".format(
            pok=self.pokemon.title, lat=self.latitude, lon=self.longitude
        )
