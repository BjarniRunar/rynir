# Rynir project settings
# -*- coding: utf-8 -*-

import locale
locale.setlocale(locale.LC_ALL, '')

from frambod_x13 import FRAMBOD_X13_LISTI
try:
    from local_settings import *
except ImportError:
    import sys
    print >> sys.stderr, ('ERROR: You have to make a local copy of the '
                          'local_settings.py file (see '
                          'local_settings.py-example).')
    exit(1)

# Django settings for rynir project.

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

RYNIR_DIR = ROOT_DIR + '/rynir'

RYNIR_BOKSTAFIR = {
  'Ut': '_',
  'Vi': 'V',
  'Sa': 'S',
  'Sj': 'D',
  'Fr': 'B',
  'Hr': 'O',
  'Pi': 'Þ',
  'Bj': 'A'
}
# Reddingar, thvi skraparinn finnur ekki alveg alla thingmenn eins og er
RYNIR_THINGMENN = {
  '727': {
    'stafir': 'GLG',
    'varamadur': False,
    'nafn': u'Guðfríður Lilja Grétarsdóttir',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/727/727-220.jpg',
    'url_vefs': 'http://www.althingi.is/cv.php4?nfaerslunr=727',
    'flokkur': 'V'
  },
  '1006': {
    'stafir': 'SSS',
    'varamadur': True,
    'nafn': u'Sigurgeir Sindri Sigurgeirsson',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/1006/1006-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=1006',
    'flokkur': 'B',
  },
  '695': {
    'stafir': 'SVÓ',
    'varamadur': False,
    'nafn': u'Steinunn Valdís Óskarsdóttir',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/695/695-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=695',
    'flokkur': 'S',
  },
  '633': {
    'stafir': 'ÞSveinb',
    'varamadur': False,
    'nafn': u'Þórunn Sveinbjarnardóttir',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/633/633-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=633',
    'flokkur': 'S',
  },
  '1011': {
    'stafir': 'APS',
    'varamadur': True,
    'nafn': u'Anna Pála Sverrisdóttir',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/1011/1011-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=1011',
    'flokkur': 'S',
  },
  '999': {
    'stafir': 'ÓBK',
    'varamadur': True,
    'nafn': u'Óli Björn Kárason',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/999/999-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=999',
    'flokkur': 'D',
  },
  '663': {
    'stafir': 'SKK',
    'varamadur': False,
    'nafn': u'Sigurður Kári Kristjánsson',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/663/663-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=663',
    'flokkur': 'D',
  },
  '1027': {
    'stafir': 'HuldA',
    'varamadur': True,
    'nafn': u'Huld Aðalbjarnardóttir',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/1027/1027-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=1027',
    'flokkur': 'B',
  },
  '1124': {
    'stafir': 'VP',
    'varamadur': True,
    'nafn': u'Víðir Smári Petersen',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/1124/1124-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=1124',
    'flokkur': 'D',
  },
  '383': {
    'stafir': 'KolH',
    'varamadur': False,
    'nafn': u'Kolbrún Halldórsdóttir',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/383/383-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=383',
    'flokkur': 'V',
  },
  '1125': {
    'stafir': 'JórE',
    'varamadur': True,
    'nafn': u'Jórunn Einarsdóttir',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/1125/1125-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=1125',
    'flokkur': 'V',
  },
  '1133': {
    'stafir': 'EvaM',
    'varamadur': True,
    'nafn': u'Eva Magnúsdóttir',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/1133/1133-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=1133',
    'flokkur': 'D',
  },
  '1134': {
    'stafir': 'HÞK',
    'varamadur': True,
    'nafn': u'Helena Þ. Karlsdóttir',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/1134/1134-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=1134',
    'flokkur': 'S',
  },
  '1135': {
    'stafir': 'ÓskV',
    'varamadur': True,
    'nafn': u'Ósk Vilhjálmsdóttir',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/1135/1135-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=1135',
    'flokkur': 'S',
  },
  '1126': {
    'stafir': 'BaldJ',
    'varamadur': True,
    'nafn': u'Baldvin Jónsson',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/1126/1126-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=1126',
    'flokkur': 'O',
  },
  '1151': {
    'stafir': 'GHV',
    'varamadur': True,
    'nafn': u'Guðrún H. Valdimarsdóttir',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/1151/1151-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=1151',
    'flokkur': 'B',
  },
  '1136': {
    'stafir': 'BaldÞ',
    'varamadur': True,
    'nafn': u'Baldur Þórhallsson',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/1136/1136-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=1136',
    'flokkur': 'S',
  },
  '686': {
    'stafir': 'HöskÞ',
    'varamadur': False,
    'nafn': u'Höskuldur Þórhallsson',
    'url_mynd': 'http://www.althingi.is/myndir/thingmenn-cache/686/686-220.jpg',
    'url_vefs': 'http://www.althingi.is/altext/cv.php4?nfaerslunr=686',
    'flokkur': 'B',
  },
}

DATABASES = {
    'default': DEFAULT_DB
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Atlantic/Reykjavik'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'rynir.urls'

TEMPLATE_BASE = 'includes/base.html'
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    RYNIR_DIR,
    RYNIR_DIR + '/includes'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'rynir.althingi',
)
