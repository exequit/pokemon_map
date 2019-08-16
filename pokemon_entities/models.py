from django.db import models


class PokemonElementType(models.Model):
    '''The Pokemon object contains a lot of pokemons
    
        Parameters:

        Attributes:
            title (CharField): name of element type
            image (ImageField): image of element
            strong_against (ManyToManyField: PokemonElementType): element against which this is effective 

        Methods:

    '''

    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка', blank=True,
                              null=True, upload_to="elements")
    strong_against = models.ManyToManyField(
        "PokemonElementType", verbose_name='Силён против', blank=True)

    def __str__(self):
        return "{title}".format(title=self.title)



class Pokemon(models.Model):
    '''The Pokemon object contains a lot of pokemons
    
    Parameters:

    Attributes:
        title (CharField): name of pokemon in russian
        title_en (CharField): name of pokemon in english 
        title_jp (CharField): name of pokemon in japan
        description (TextField): description of pokemon
        image (ImageField): image of pokemon
        element_type (ManyToManyField: PokemonElementType): element types which pokemon has   
        previous_evolution (ForeignKey: Pokemon): pokemon from which current pokemon evolve           
    
    Methods:

    '''
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
    '''The Pokemon entity object contains a lot of pokemon entities
    
    Parameters:

    Attributes:
        pokemon (ForeignKey: Pokemon): current pokemon 
        latitude (FloatField): lantitude of pokemone  
        longitude (FloatField): longtitude of pokemon
        appear_at (DateTimeField): date and time when pokemon appear
        disappear_at (DateTimeField): date and time when pokemon disappear
        level (IntegerField): level of pokemon
        health (IntegerField): health of pokemon
        strength (IntegerField): strength of pokemon
        defence (IntegerField): defence of pokemon
        stamina (IntegerField): stamina of pokemon

    Methods:

    '''

    pokemon = models.ForeignKey(
        Pokemon, verbose_name='Покемон', on_delete=models.PROTECT)
    latitude = models.FloatField('Ширина')
    longitude = models.FloatField('Долгота')
    appear_at = models.DateTimeField('Появится в', blank=True, default=None)
    disappear_at = models.DateTimeField('Пропадет в', blank=True, default=None)
    level = models.IntegerField('Уровень', blank=True, default=0)
    health = models.IntegerField('Здоровье', blank=True, default=0)
    strength = models.IntegerField('Атака', blank=True, default=0)
    defence = models.IntegerField('Защита', blank=True, default=0)
    stamina = models.IntegerField('Выносливость', blank=True, default=0)

    def __str__(self):
        return "{pok}({lat};{lon})".format(
            pok=self.pokemon.title, lat=self.latitude, lon=self.longitude
        )
