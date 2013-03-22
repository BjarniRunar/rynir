from django.db import models

class Flokkur(models.Model):
  nafn = models.CharField(max_length=100)
  stafir = models.CharField(max_length=1)
  lysing = models.CharField(max_length=10000)
  url_vefs = models.CharField(max_length=200)
  url_mynd = models.CharField(max_length=200)

class Thingmadur(models.Model):
  nafn = models.CharField(max_length=100)
  stafir = models.CharField(max_length=5)
  url_vefs = models.CharField(max_length=200)
  url_mynd = models.CharField(max_length=200)

class Flokksseta(models.Model):
  flokkur = models.ForeignKey(Flokkur)
  thingmadur = models.ForeignKey(Thingmadur)
  upphaf = models.DateTimeField('Gekk i flokkinn')
  endir = models.DateTimeField('Gekk ur flokknum')

class Fundur(models.Model):
  nr = models.CharField(max_length=5)
  dags = models.DateTimeField('Dagsetning thingfundar')
  titill = models.CharField(max_length=200)

class Umraeda(models.Model):
  titill = models.CharField(max_length=200)
  timi = models.DateTimeField('Upphaf umraedu')
  efni = models.CharField(max_length=10000)
  url_ferill = models.CharField(max_length=200)

class Kosning(models.Model):
  umraeda = models.ForeignKey(Umraeda)
  titill = models.CharField(max_length=200)
  timi = models.DateTimeField('Upphaf umraedu')
  url_skjal = models.CharField(max_length=200)

class Atkvaedi(models.Model):
  kosning = models.ForeignKey(Kosning)
  thingmadur = models.ForeignKey(Thingmadur)
  atkvaedi = models.CharField(max_length=5)

