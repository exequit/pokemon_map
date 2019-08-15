from django.db import models


class PokemonElementType(models.Model):
    title = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка', blank=True,
                              null=True, upload_to="elements")
    strong_against = models.ManyToManyField(
        "PokemonElementType", verbose_name='Силён против', blank=True)

    def __str__(self):
        return "{title}".format(title=self.title)


class Pokemon(models.Model):
    '''Pokemon model'''
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
    '''model Pokemon entity'''
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
