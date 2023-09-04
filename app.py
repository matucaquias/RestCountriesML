from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


# Declaración de la tabla en la BD:
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


# API completa después de fillear la BD:
@app.route('/country')
def get_countries():
    countries = Country.query.all()
    output = []
    for country in countries:
        country_data = {'country': country.country, 'capital': country.capital, 'population': country.population}

        output.append(country_data)
    return {"countries": output}

# Método para popular la BD desde la API REST de RestCountries:
@app.route('/load_data', methods=['POST'])
def load_data():
    # Obtener datos de la API de países
    response = requests.get('https://restcountries.com/v3.1/all')
    countries_data = response.json()

    # Limpiar la tabla 'Country' en la base de datos
    db.session.query(Country).delete()

    # Guardar los datos en la base de datos
    for country_info in countries_data:
        # Chequeo en caso de que el formato no coincida con el general de las capitales:
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

# Query para devolver capital, % de población y próximo país en cuanto a % poblacional:
@app.route('/country_info', methods=['GET'])
def country_info():
    country_name = request.args.get('country')

    # Buscar información del país en la base de datos
    country = Country.query.filter_by(country=country_name).first()

    if country:
        # Calcular el porcentaje de población mundial
        total_population = db.session.query(func.sum(Country.population)).scalar()
        percentage = (country.population / total_population) * 100

        # Encontrar el próximo país
        next_country = Country.query.filter(Country.population < country.population).order_by(
            Country.population.desc()).first()

        response = {
            'capital': country.capital,
            'porcentaje_mundial': str(percentage) + '%',
            'proximo_pais': next_country.country if next_country else None
        }

        return jsonify(response)
    else:
        return jsonify({'message': 'País no encontrado'}), 404


if __name__ == '__main__':
    app.run()
