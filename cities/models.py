from django.db import models

class City(models.Model):

    title = models.CharField(verbose_name='Название города', max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class District(models.Model):

    title = models.CharField(verbose_name='Название района', max_length=150)
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return f"{self.title} | {self.city.title}"

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'

class Street(models.Model):

    title = models.CharField(verbose_name='Название улицы', max_length=150)
    district = models.ForeignKey(District, verbose_name='Район', on_delete=models.CASCADE, related_name='streets')

    def __str__(self):
        return f"{self.title} | {self.district.title}"

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'
