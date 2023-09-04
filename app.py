from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    capital = db.Column(db.String(250), default='')
    population = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.country} - {self.capital} - {self.population}"


@app.route('/')
def index():
    return 'Hello!'


@app.route('/country')
def get_countries():
    return {"countries": "countries data"}


@app.route('/load_data', methods=['POST'])
def load_data():
    # Obtener datos de la API de países
    response = requests.get('https://restcountries.com/v3.1/all')
    countries_data = response.json()

    # Limpiar la tabla 'Country' en la base de datos
    db.session.query(Country).delete()

    # Guardar los datos en la base de datos
    for country_info in countries_data:
        try:
            capitals = country_info['capital']
            if isinstance(capitals, list):
                capital = ', '.join(capitals)
            else:
                capital = capitals
        except KeyError:
            capital = ''
        country = Country(
            country=country_info['name']['common'],
            capital=capital,
            population=country_info['population']
        )
        db.session.add(country)

    # Confirmar los cambios en la base de datos
    db.session.commit()

    return {"message": "Data loaded successfully"}

if __name__ == '__main__':
    app.run()