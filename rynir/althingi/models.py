import datetime
import locale
from django.db import models


class Flokkur(models.Model):
  stafur = models.CharField(max_length=1)
  nafn = models.CharField(max_length=100)
  abbr = models.CharField(max_length=20)
  lysing = models.CharField(max_length=10000)
  url_vefs = models.CharField(max_length=200)
  url_mynd = models.CharField(max_length=200)

class Thingmadur(models.Model):
  althingi_id = models.CharField(max_length=10)
  nafn = models.CharField(max_length=100)
  stafir = models.CharField(max_length=10)
  url_vefs = models.CharField(max_length=200)
  url_mynd = models.CharField(max_length=200)
  varamadur = models.BooleanField()
  iframbodifyrir = models.CharField(max_length=1)
  cached_vidvera = models.IntegerField(null=True)
  cached_skropadi = models.IntegerField(null=True)
  cached_uppreisnir = models.IntegerField(null=True)

  def frambodsstafir(self):
    words = self.iframbodifyrir.split()
    if words:
      return words[0]
    return ''

  def frambodssaeti(self):
    if not self.iframbodifyrir:
      return 0
    return int(self.iframbodifyrir.split()[2][1:])

  def toppfimm(self):
    saeti = self.frambodssaeti()
    return (saeti > 0) and (saeti <= 5)

  def kaus(self, atkv):
    return Atkvaedi.objects.filter(thingmadur=self, atkvaedi=atkv
                                   ).order_by('-kosning__umraeda__umfang')

  def kaus_ja(self): return self.kaus('J')
  def kaus_nei(self): return self.kaus('N')
  def kaus_ekki(self): return self.kaus('S')
  def kaus_skrop(self): return self.kaus('F')

  def kaus_uppreisn(self):
    return Atkvaedi.objects.filter(thingmadur=self, uppreisn=True
                                   ).exclude(atkvaedi='F'
                                   ).order_by('-kosning__umraeda__umfang')

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

  def drop_caches(self):
    if (self.cached_vidvera is not None or
        self.cached_skropadi is not None or
        self.cached_uppreisnir is not None):
     self.cached_vidvera = self.cached_skropadi = self.cached_uppreisnir = None
     self.save()

  def vidvera(self, refresh=False):
    if refresh or self.cached_vidvera is None:
      self.cached_vidvera = Atkvaedi.objects.filter(thingmadur=self).count()
      self.save()
    return self.cached_vidvera or 0

  def skropadi(self, refresh=False):
    if refresh or self.cached_skropadi is None:
      self.cached_skropadi = Atkvaedi.objects.filter(thingmadur=self,
                                                     atkvaedi='F').count()
      self.save()
    return self.cached_skropadi or 0

  def uppreisnir(self, refresh=False):
    if refresh or self.cached_uppreisnir is None:
      self.cached_uppreisnir = Atkvaedi.objects.filter(thingmadur=self,
                                                       uppreisn=True
                                                       ).exclude(atkvaedi='F'
                                                                 ).count()
      self.save()
    return self.cached_uppreisnir or 0

  def maeting(self):
    return '%.1f' % (10.0 - (10.0 * self.skropadi() / (self.vidvera() or 1)))

  def hlydni(self):
    if self.flokkur().stafur == '_':
      return '10.0'
    return '%.1f' % (10.0 - min(10, 0.05 * self.uppreisnir()))

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

  def atkvaedi(self, v):
    atkv = list(Atkvaedi.objects.filter(kosning=self, atkvaedi=v))
    atkv.sort(key=lambda a: a.thingmadur.flokkur().stafur + a.thingmadur.nafn,
              cmp=locale.strcoll)
    return atkv

  def atkvaedi_ja(self): return self.atkvaedi('J')
  def atkvaedi_nei(self): return self.atkvaedi('N')
  def atkvaedi_satuhja(self): return self.atkvaedi('S')
  def atkvaedi_fjarverandi(self): return self.atkvaedi('F')
  def atkvaedi_uppreisn(self):
    atkv = [a for a in list(Atkvaedi.objects.filter(kosning=self, uppreisn=True
                                                    ).exclude(atkvaedi='F'))
                    if a.thingmadur.flokkur().stafur != '_']
    atkv.sort(key=lambda a: a.thingmadur.flokkur().stafur + a.thingmadur.nafn,
              cmp=locale.strcoll)
    return atkv

class Atkvaedi(models.Model):
  kosning = models.ForeignKey(Kosning)
  thingmadur = models.ForeignKey(Thingmadur)
  atkvaedi = models.CharField(max_length=5)
  uppreisn = models.BooleanField()

