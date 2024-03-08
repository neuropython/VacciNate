from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Vaccine(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, null = True)
    status = models.CharField(max_length=100, default="mandatory")
    quantity_of_doses = models.IntegerField(default=1)
    interval = models.CharField(max_length=100, null=True)

    class Period(models.TextChoices):
        MONTH = 'MO', _('month')
        YEAR = 'YR', _('year')
        DAY = 'DT', _('day')
        NULL = 'NL', _('null')

    period = models.CharField(
        max_length=2,
        choices=Period.choices,
        default=Period.MONTH,
    )

    def __str__(self):
        return self.name

class UserVaccine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=100, default="pending")
    dose = models.IntegerField(default=1)
    next_date = models.DateField(null=True)

    def __str__(self):
        return self.user.username + " - " + self.vaccine.name

