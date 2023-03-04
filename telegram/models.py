from django.db import models

CATEGORIA_CHOICES = [
    ('', ''),
    ('Deputado', 'Deputado'),
    ('Acessor', 'Acessor'),
]

LOCALE_CHOICES = [
        ('', ''),
    ('Federal', 'Federal'),
    ('Estadual', 'Estadual'),
]
class Registrador(models.Model):
    user_ident = models.IntegerField(blank=True)
    nomeuser = models.CharField(max_length=50, blank=True)
    data = models.CharField(max_length=11, blank=True)
    rep_dep = models.CharField(max_length=30, blank=True)
    is_writable = models.CharField(max_length=11, blank=True)
    locale_is = models.CharField(max_length=8,
                  choices=LOCALE_CHOICES,
                  default="")
    tipo = models.CharField(max_length=8,
                  choices=CATEGORIA_CHOICES,
                  default="")
    

    class Meta:
        verbose_name = 'Registradore'

    def __str__(self):
        return self.nomeuser
    


