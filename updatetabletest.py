from flask_sqlalchemy import SQLAlchemy
from app import app, db, Country

# Crea una instancia de la aplicación Flask
app.app_context().push()

# Obtiene todos los registros de Country
countries = Country.query.all()

# Actualiza los registros estableciendo el campo capital en cadena vacía si es None
for country in countries:
    if country.capital is None:
        country.capital = ''

# Confirma los cambios en la base de datos
db.session.commit()
