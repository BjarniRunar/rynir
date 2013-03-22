# Alþingisrýnirinn #

Þetta er kóði sem kemur vonandi til með að auðvelda fólki að fylgjast
með því hvernig kjörnir fulltrúar þeirra haga atkvæðum sínum á Alþingi.


## Að hakkast í kóðanum ##

Þú þarft `django` og `BeautifulSoup` 2.x og `chardet`.  Miðað er við
útgáfurnar sem hægt er að setja inn með `apt-get` á gamalli Debian
vél.

Svo þarf að gera svona:

    $ manage.py syncdb
    $ manage.py runserver

    # Í öðrum terminal
    $ curl http://localhost:8000/scraper/bootstrap

Vei!

