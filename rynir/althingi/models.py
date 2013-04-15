import datetime
from django.db import models


class Flokkur(models.Model):
  stafur = models.CharField(max_length=1)
  nafn = models.CharField(max_length=100)
  abbr = models.CharField(max_length=20)
  lysing = models.CharField(max_length=10000)
  url_vefs = models.CharField(max_length=200)
  url_mynd = models.CharField(max_length=200)

class Thingmadur(models.Model):
  nafn = models.CharField(max_length=100)
  stafir = models.CharField(max_length=10)
  url_vefs = models.CharField(max_length=200)
  url_mynd = models.CharField(max_length=200)

  def flokkur(self, dags=None):
    seta = Flokksseta.objects.filter(thingmadur=self).order_by('-upphaf')
    if not seta:
      return None
    if not dags:
      return seta[0].flokkur
    for s in seta:
      if s.upphaf < dags:
        return s.flokkur
    return None

class Flokksseta(models.Model):
  flokkur = models.ForeignKey(Flokkur)
  thingmadur = models.ForeignKey(Thingmadur)
  upphaf = models.DateTimeField('Gekk i flokkinn')

class Fundur(models.Model):
  fnr = models.CharField(max_length=6)
  lth = models.CharField(max_length=6)
  dags = models.DateTimeField('Dagsetning thingfundar')
  titill = models.CharField(max_length=200)

class Umraeda(models.Model):
  uid = models.CharField(max_length=30)
  fundur = models.ForeignKey(Fundur)
  titill = models.CharField(max_length=200)
  umfang = models.IntegerField()
  timi = models.DateTimeField('Upphaf umraedu')
  efni = models.CharField(max_length=10000)
  url_ferill = models.CharField(max_length=200)

class Kosning(models.Model):
  uid = models.CharField(max_length=30)
  umraeda = models.ForeignKey(Umraeda)
  titill = models.CharField(max_length=200)
  timi = models.DateTimeField('Upphaf umraedu')
  url_skjal = models.CharField(max_length=200)
  cached_sparks = models.CharField(max_length=3*63)

  def sparks(self):
    if not self.cached_sparks:
      sparks = ['%s%s' % (a.thingmadur.flokkur().stafur, a.atkvaedi)
                for a in Atkvaedi.objects.filter(kosning=self)]
      sparks.sort(key=lambda k: {'J':'A', 'N':'B', 'S':'C', 'F':'D'}[k[1]]+k[0])
      self.cached_sparks = ''.join(sparks)
      self.save()
    return self.cached_sparks

class Atkvaedi(models.Model):
  kosning = models.ForeignKey(Kosning)
  thingmadur = models.ForeignKey(Thingmadur)
  atkvaedi = models.CharField(max_length=5)

