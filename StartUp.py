from app import db, app
import requests
# Este archivo generará la BD local y realizará el primer POST para popular la BD:
app.app_context().push()
db.create_all()

# URL de load_data método para popular la BD en app.py
url = 'http://127.0.0.1:5000/load_data'

# Realizar la solicitud POST
response = requests.post(url)

# Verificar la respuesta del servidor
if response.status_code == 200:
    print("Solicitud POST exitosa")
else:
    print(f"Error en la solicitud POST: {response.status_code} - {response.text}")
