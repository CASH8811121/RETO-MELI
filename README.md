# RETO-MELI

#  Requisitos

Python, IDE (VSCODE), virtualenv, GIT.

https://git-scm.com/download/win
https://code.visualstudio.com/python
https://www.python.org/ftp/python/3.11.3/python-3.11.3-amd64.exe




# Inicializar

Se debe seguir los siguientes pasos para poder inicializar el entorno de pruebas: 

* **1-** Clonar el repositorio en IDE de preferencia VSCODE: 
`git clone https://github.com/CASH8811121/RETO-MELI.git`
* **2-** Asegurarse de instalar virtualenv en el IDE desde terminal: 
`pip install virtualenv`
* **3-** ejecutar este comando en powershell (como administrador) para permitir ejecucion remota de codigo desde el IDE: 
`Set-ExecutionPolicy RemoteSigned -Force`
* **4-** en el IDE creamos el enviroment virtual llamado env: 
`virtualenv -p python3 env`
* **5-** Iniciar el enviroment en el IDE: 
`.\env\Scripts\activate`  
Comprobar con pip list si esta instalado
* **4-** instalar los componentes necesarios para iniciar la API: 
`pip install -r requeriments.txt`
* **4-** Correr la API: 
`python .\app\app.py`
* **4-** Acceder a WEB localhost mediante URL: 
`http://127.0.0.1:5000`
