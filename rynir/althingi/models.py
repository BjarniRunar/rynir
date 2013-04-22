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
  cached_maeting = models.IntegerField(null=True)
  cached_hlydni = models.IntegerField(null=True)

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

  def maeting(self, refresh=False):
    if refresh or self.cached_maeting is None:
      maettur = Atkvaedi.objects.filter(thingmadur=self
                                        ).exclude(atkvaedi='F').count()
      total = Kosning.objects.count()
      self.cached_maeting = total and int((100 * maettur) / total) or 0
      self.save()
    return self.cached_maeting

  def hlydni(self, refresh=False):
    if refresh or self.cached_hlydni is None:
      maettur = Atkvaedi.objects.filter(thingmadur=self
                                        ).exclude(atkvaedi='F')
      hlydni = 0
      flokkur = self.flokkur()  # FIXME: dags = ??
      for m in maettur:
        votes = Atkvaedi.objects.filter(kosning=m.kosning)
        disagree = agree = 0
        for v in votes:
          if flokkur == v.thingmadur.flokkur():
            if v.atkvaedi == m.atkvaedi:
              agree += 1
            else: 
              disagree += 1
        if agree > disagree:
          hlydni += 1
        elif m.atkvaedi == 'S':
          hlydni += 0.5
      self.cached_hlydni = maettur and int((100 * hlydni) / len(maettur)) or 0
      self.save()
    return self.cached_hlydni

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
  cached_sparks = models.CharField(max_length=3*63, null=True)

  def sparks(self, refresh=False):
    if refresh or self.cached_sparks is None:
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

