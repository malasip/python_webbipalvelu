# Tuodaan flask kirjastosta Flask pääluokka, joka implementoi WSGI applikaation
from flask import Flask

# Luodaan instanssi Flask luokasta ja annetaan sille nimeksi ajettavan scriptin nimi __name__ muuttujasta.
# Valitaan __name__ jotta flask löytää templatet ja muut käytettävät tiedostot oikeasta paikasta.
app = Flask(__name__)

# Luodaan reitti josta applikaatio vastaa GET kyselyihin
@app.route('/')
# Määritellään funktio joka hoitaa kyselyyn vastaamisen. Funktion nimi tulee olla kuvaava
def index():
    # Määritellään jotain liirumlaarumia sivun sisällöksi ja palautetaan se (flask appi renderöi)
    content = 'Hello, world!'
    return content

# Varmistetaan että development serveriä ei ajeta jos scripti on importattu toiseen.
if __name__ == '__main__':
    # Ajetaan flask appi. Host parametrillä määritellään missä osoitteessa applikaatio kuuntelee tulevia kutsuja.
    # Debug true moodilla appi latautuu uudelleen jos koodiin tulee muutoksia.
    app.run(host='0.0.0.0', debug=True)