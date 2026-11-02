Requisitos
Setup de un ambiente virtual de python virtual con pydgraph instalado
# Si no tienes pip instalado
sudo apt update
sudo apt install python3-pip

# Instalar y activar el virtual env (Linux/MacOS)
python3 -m pip install virtualenv
python3 -m venv ./venv
source ./venv/bin/activate

# Instalar y activar el virtual env (Windows)
python3 -m pip install virtualenv
python3 -m venv ./venv
.\venv\Scripts\Activate.ps1

# Instalar los requerimientos de python al project
python3 -m pip install -r requirements.txt
Para cargar los datos

# Asegurate de tener una instancia de dgraph corriendo i.e.:
docker run --name dgraph -d -p 8080:8080 -p 9080:9080 dgraph/standalone

# Opcional tener una instancia de ratel para visualizar los datos
docker run --name ratel -d -p 8000:8000 dgraph/ratel:latest

# Correr pydgraph.py i.e.:
python3 pydgraph_student.py
