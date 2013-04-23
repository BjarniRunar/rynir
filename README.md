# Alþingisrýnirinn #

Þetta er kóði sem kemur vonandi til með að auðvelda fólki að fylgjast
með því hvernig kjörnir fulltrúar þeirra haga atkvæðum sínum á Alþingi.


## Að hakkast í kóðanum ##

Þú þarft `django` og `BeautifulSoup` 2.x og `chardet`.  Miðað er við
útgáfurnar sem hægt er að setja inn með `apt-get` á gamalli Debian
vél.

Fyrst þarf að búa til skrá sem heitir `rynir/local_settings.py`, en
það er ágætis sýnishorn að finna í `rynir/local_settings.py-example`.

Svo þarf að gera svona:

    $ manage.py syncdb
    $ manage.py runserver

    # Í öðrum terminal
    $ curl http://localhost:8000/scraper/bootstrap/testing

Ef þú vilt að græjan lesi allt sem gerðist á síðasta kjörtímabili, í
staðinn fyrir að lesa bara inn síðustu fundina skiparðu svona í staðinn:

    $ curl http://localhost:8000/scraper/bootstrap

Vei!

