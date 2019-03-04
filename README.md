# Sistema de interacción y monitorización a través de distribución Raspberry 

**Nota:**La carpeta actual contiene el desarrollo de un sencillo sistema de incubación que cuenta con monitorización en Graphana y envío de alertas en tiempo real a través de esta herramienta. Por otro lado, implementa un sistema de interacción automático el cual reproduce sonidos en base al estudio de emociones y sonidos captados.

# Mi Band2 + reproducción de pulso

**Nota:**El fichero miband2.py contiene la librería desarrollada por [Leo Soares](https://github.com/leojrfs/miband2) 
quién también ha escrito un artículo interesante sobre mi Band: [Mi Band 2, Part 1: Authentication](https://leojrfs.github.io/writing/miband2-part1-auth/).
Por otro lado incluye una modificación desarrollada por mi de dicha librería, que añade un sistema de reproduccion de audio, que reproduce en tiempo real los latidos que son recogidos a traves de la pulsera. 
Las clases main.py y pulsos.py, asi como los audios contenidos permiten integrar parte de la funcionalidad de esa reproducción. Por otro lado, esta incluido un sistema de reconocimiento de emociones explicado en la `Nota2` que se ejecuta cada 2 minutos, que activa o desactiva un sonido dependiendo de la emoción.

### Preparación

En primer lugar se debe desconectar la Mi Band de la aplicación, si no queremos desvincular la pulsera de la aplicación debemos desconectarla de nuestro
bluetooth movil.

Para hacer uso del pulsometro instalaremos `Python 3` y la libreria `bluepy`:

apt-get install python3-pip libglib2.0-dev
pip3 install bluepy --user

En este caso uso `Python 3` ya que la librería que vamos a utilizar para el audio solo est disponible en esta version.

Para reproducir el sonido del corazón instalaremos la librería `simpleaudio`:

pip install --upgrade pip setuptools

pip install simpleaudio

Para variantes de Linux debemos instalar

sudo apt-get install -y python3-dev libasound2-dev

Si nuestro Linux trabaja sobre `Python 2` y queremos usar `Python 3` introducimos en la terminal:

alias python='/usr/bin/python3'
sudo -H pip3 install --upgrade pip

Si la instalación de simpleaudio nos ha dado problemas tras ejecutar el comando citado anteriormente ejecutaremos las siguientes lineas:

sudo -H pip3 install simpleaudio

# Detección de emociones

**Nota2:**He añadido y modificado una librería de (https://cloud.google.com/) para el reconocimiento facial de emociones. 
Ya que se deben detectar emociones de neonatales, he creado un modelo personalizado con la herramienta beta AUTOML Vision 
de la API (https://cloud.google.com/vision/). Este modelo cuenta con dos emociones, llanto y binestar. 
La detección de una emoción se realiza a través de una imagen cuya ruta se especifica, dicha imagen es obtenida en tiempo real a través de la cámara de raspberry pi (picam).

### Preparación

Para hacer uso de la librería debemos asegurarnos de que estamos usando `Python 3`:

python --version

Si nuestra versión es inferior a la 3.0 podemos introducir el comando de `alias` citado anteriormente.

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

su
export GOOGLE_APPLICATION_CREDENTIALS=filename.json

# Influxdb y Graphana

**Nota3:**Para utilizar la visualización de datos en Graphana, introduzco los datos recogidos en la base de datos Influxdb.Para ello será necesarió instalar ambas herramientas.

### Preparación

Para añadir Influxdb se puede crear un nuevo repositorio, después hay que instalar la clave pública y por último instalar influxdb:

    echo "deb https://miRepositorio.com bionic stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
    sudo curl -sL https://miRepositorio.com/influxdb.key | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install influxdb -y
    sudo systemctl start influxd
    sudo systemctl enable influxd
    
Para añadir Grphana hay que seguir los pasos de instalación de Influxdb realizando alguna modificación:

    echo "deb https://packagecloud.io/grafana/stable/debian/ stretch main" | sudo tee /etc/apt/sources.list.d/grafana.list
    curl https://packagecloud.io/gpg.key | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install grafana
    sudo systemctl start grafana-server
    sudo systemctl enable grafana-server
    













