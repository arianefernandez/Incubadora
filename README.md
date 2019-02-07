# Mi Band + reproduccion de pulso

**Nota:**La carpeta actual contiene la librería desarrollada por [Leo Soares](https://github.com/leojrfs/miband2).
Él también ha escrito un artículo interesante sobre mi Band: [Mi Band 2, Part 1: Authentication](https://leojrfs.github.io/writing/miband2-part1-auth/).

Por otro lado incluye una modificacion desarrollada por [Ariane Fernandez] de dicha libreria, que añade un sistema de reproduccion de audio, que reproduce en tiempo real los latidos 
que son recogidos a traves de la pulsera. Las clases main.py y pulsos.py, asi como los audios contenidos no formaban parte de la libreria original. 

### Preparacion

En primer lugar se debe desconectar la Mi Band de la aplicación, si no queremos desvincular la pulsera de la aplicación debemos desconectarla de nuestro
bluetooth movil.

Para hacer uso del pulsometro instalaremos `Python 3` y la libreria `bluepy`:

pip install bluepy --user

En este caso uso `Python 3` ya que la librería que vamos a utilizar para el audio solo est disponible en esta version.

Para reproducir el sonido del corazon instalaremos la libreria `simpleaudio`:

pip install --upgrade pip setuptools

pip install simpleaudio

Para variantes de Linux debemos instalar

sudo apt-get install -y python3-dev libasound2-dev

Si nuestro Linux trabaja sobre `Python 2` y queremos usar `Python 3` introducimos en la terminal:

alias python='/usr/bin/python3'
sudo -H pip3 install
--upgrade pip

Si la instalacion de simpleaudio nos ha dado problemas tras ejecutar el comando citado anteriormente ejecutaremos las siguientes lineas:

sudo -H pip3 install
simpleaudio
