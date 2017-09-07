from django.db import models


class Algo(models.Model):
    name = models.CharField(max_length=2000)
    signal = models.CharField(max_length=2000)
    trade = models.CharField(max_length=2000)
    ticker = models.CharField(max_length=2000)
    average_pnl = models.FloatField()


