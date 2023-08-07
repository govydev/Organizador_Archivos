# INSTALACION DE PAQUETES
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <paquete>
# ELIMINAR PAQUETES
pip uninstall -y <paquete>, <paquete>
# DEPLOY
python setup.py build
pyinstaller --onefile --windowed --add-data "icons;." .\proceso_definitivo.py

# ENTORNOS VIRTUALES
## CREACION DE ENTORNO
python -m venv tutorial-env
## CREACION DE LISTA DE PAQUETES
python -m pip freeze > requirements.txt

## INSTALACION DE LISTA DE PAQUETES
python -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt


# Agregar from babel.numbers import * al archivo calendar_.py del paquete tkalendar
from babel.numbers import *