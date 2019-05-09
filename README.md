# Mi Band + reproduccion de pulso

**Nota:**La carpeta actual contiene la librería desarrollada por [Leo Soares](https://github.com/leojrfs/miband2) 
quién también ha escrito un artículo interesante sobre mi Band: [Mi Band 2, Part 1: Authentication](https://leojrfs.github.io/writing/miband2-part1-auth/).

Por otro lado incluye una modificacion desarrollada por [Ariane Fernandez] de dicha libreria, que añade un sistema de reproduccion de audio, que reproduce en tiempo real los latidos 
que son recogidos a traves de la pulsera. Las clases main.py y pulsos.py, asi como los audios contenidos no formaban parte de la libreria original. 
Por otro lado esta incluido el sistema de reconocimiento de emociones explicado en la `Nota2` que se ejecuta cada 15 minutos.

### Preparacion

En primer lugar se debe desconectar la Mi Band de la aplicación, si no queremos desvincular la pulsera de la aplicación debemos desconectarla de nuestro
bluetooth movil.

Para hacer uso del pulsometro instalaremos `Python 3` y la libreria `bluepy`:

apt-get install python3-pip libglib2.0-dev
pip3 install bluepy --user

En este caso uso `Python 3` ya que la librería que vamos a utilizar para el audio solo est disponible en esta version.

Para reproducir el sonido del corazon instalaremos la libreria `simpleaudio`:

pip install --upgrade pip setuptools

pip install simpleaudio

Para variantes de Linux debemos instalar

sudo apt-get install -y python3-dev libasound2-dev

Si nuestro Linux trabaja sobre `Python 2` y queremos usar `Python 3` introducimos en la terminal:

alias python='/usr/bin/python3'
sudo -H pip3 install --upgrade pip

Si la instalacion de simpleaudio nos ha dado problemas tras ejecutar el comando citado anteriormente ejecutaremos las siguientes lineas:

sudo -H pip3 install simpleaudio

**Nota2:**He añadido y modificado una libreria de (https://cloud.google.com/) para el reconocimiento facial de emociones. 
Ya que se deben detectar emociones de neonatales, he creado un modelo personalizado con la herramienta beta AUTOML Vision 
de la API (https://cloud.google.com/vision/). Este modelo cuenta con dos emociones, llanto y binestar. 
De momento es para la detección de una emocion a través de una imagen, cuya ruta se especifica, pero haré una actualización
para cambiar dicho funcionamiento.

Para hacer uso de la libreria debemos asegurarnos de que estamos usando `Python 3`:

python --version

Si nuestra version es inferior a la 3.0 podemos introducir el comando de `alias` citado anteriormente.

Es necesario tener la siguiente libreria para `Python 3` en su version 0.1.2:

pip install google-cloud-automl

Es conveniente tener un setup adecuado para Python:

sudo apt update
sudo apt install python python-dev python3 python3-dev

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py

$ pip --version
pip 9.0.1 from /usr/local/lib/python3.5/dist-packages (python 3.5)

pip install --upgrade virtualenv

cd your-project
virtualenv --python python3 env

virtualenv --python "c:\python36\python.exe" env

Para ejecutar emocion.py es necesario rellenar tal como se indica en el tutorial de (https://cloud.google.com/vision/):

    project_id = 'PROJECT_ID_HERE'
    compute_region = 'COMPUTE_REGION_HERE'
    model_id = 'MODEL_ID_HERE'
    file_path = '/local/path/to/file'
    score_threshold = 'float from 0.0 to 0.5'

Hay que recordar introducir las credenciales

sudo -i
export GOOGLE_APPLICATION_CREDENTIALS=filename.json

Respecto a la aplicación web de Heroku, para usar la piCamera hay que usar el siguiente comando

sudo modprobe bcm2835-v4l2
    













