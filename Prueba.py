import requests
response = requests.get('https://restcountries.com/v3.1/all')
# Test de devolución de common names y capitales:
common_names = str
capital = str
i = 0

while i < int(len(response.json())):
    common_names = response.json()[i]
    capital = response.json()[i]
    print(common_names['name']['common'])
    # Capitales da error ya que Antartida, por ejemplo, no tiene capital
    print(capital['capital'])
    i = i + 1
########################################