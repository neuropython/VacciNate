from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils import timezone

# Create your models here.

class Vaccine(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100, null = True)
    obligation = models.CharField(max_length=20)
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
    class Status(models.TextChoices):
        MANDATORY = 'mandatory', _('mandatory')
        RECOMENDED = 'recomended', _('recomended')
        NON_MANDATORY = 'non_mandatory', _('non_mandatory')
        
    obligation = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.MANDATORY,
    )


    def __str__(self):
        return self.name

class UserVaccine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE, related_name="vaccine")
    status = models.CharField(max_length=100, default="pending")
    dose = models.IntegerField(default=1)
    fist_date = models.DateField(null=False, default=timezone.now)
    all_dates = models.JSONField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.id:  # This is a new instance
            if not self.vaccine:
                raise ValueError("The vaccine attribute must be set before saving a UserVaccine instance.")
            if self.vaccine.interval == "NL":
                interval = [0]
            else:
                interval = list(map(int, self.vaccine.interval.split(",")))
            if self.vaccine.period == "MO":
                value = 30
            elif self.vaccine.period == "YR":
                value = 365
            elif self.vaccine.period == "DT":
                value = 1
            else:
                value = 0
            self.all_dates = [
                str(self.fist_date + timedelta(days=interval[i]*value)) for i in range(self.vaccine.quantity_of_doses)
                ]
        super(UserVaccine, self).save(*args, **kwargs)
        
    class Status(models.TextChoices):
        DONE = 'done', _('done')
        PENDING = 'pending', _('pending')
        CANCELLED = 'cancelled', _('cancelled')
        
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def __str__(self):
        return self.user.username + " - " + self.vaccine.name

