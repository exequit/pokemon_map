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
        'Имя (англ.)', max_length=200, blank=True, null=True)
    title_jp = models.CharField(
        'Имя (яп.)', max_length=200, blank=True, null=True)
    description = models.TextField('Описание', blank=True, null=True)
    image = models.ImageField('Картинка', blank=True, null=True)
    element_type = models.ManyToManyField(PokemonElementType)
    previous_evolution = models.ForeignKey(
        "Pokemon", on_delete=models.CASCADE, verbose_name='Из кого эволюционировал',
        blank=True, null=True, related_name="next_evolution")

    def __str__(self):
        return "{title}".format(
            title=self.title
        )


class PokemonEntity(models.Model):
    '''model Pokemon entity'''
    pokemon = models.ForeignKey(
        Pokemon, verbose_name='Покемон', on_delete=models.CASCADE)
    latitude = models.FloatField('Ширина')
    longitude = models.FloatField('Долгота')
    appear_at = models.DateTimeField('Появится в', default=None)
    disappear_at = models.DateTimeField('Пропадет в', default=None)
    level = models.IntegerField('Уровень', default=None)
    health = models.IntegerField('Здоровье', default=None)
    strength = models.IntegerField('Атака', default=None)
    defence = models.IntegerField('Защита', default=None)
    stamina = models.IntegerField('Выносливость', default=None)

    def __str__(self):
        return "{pok}({lat};{lon})".format(
            pok=self.pokemon.title, lat=self.latitude, lon=self.longitude
        )
