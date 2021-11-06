import requests
import pandas as pd
from bs4 import BeautifulSoup

keyword = input('\nKeyword: ')
zipCode = input('\nZip Code: ')

name = []
barCode = []
price = []
issue = []
address = []
distance = []

session = requests.Session()
r = session.get('https://precodahora.ba.gov.br/produtos/')

cookie = session.cookies.get_dict()

soup = BeautifulSoup(r.text, features='lxml')
csrf_token = soup.select_one('meta[id="validate"]')['data-id']

headers = {
    'X-CSRFToken': csrf_token,
    'X-Requested-With': 'XMLHttpRequest'
}

locPayload = {
    'cep': zipCode
}

try:

    locRes = session.post('https://precodahora.ba.gov.br/geolocation/', headers=headers, cookies=cookie, data=locPayload).json()

    if locRes['codigo'] == 80:

        lat = locRes['lat']
        lon = locRes['lon']

        proPayload = {
            'termo': keyword,
            'horas': 72,
            'latitude': lat,
            'longitude': lon,
            'raio': 15,
            'pagina': 1,
            'ordenar': 'preco.asc',
        }

        proRes = session.post('https://precodahora.ba.gov.br/produtos/', headers=headers, cookies=cookie, data=proPayload).json()

        if proRes['codigo'] == 80:
            
            products = proRes['resultado']

            for i, product in enumerate(products):
                if i > 10:
                    break
                name.append(product['produto']['descricao'])
                barCode.append(product['produto']['gtin'])
                price.append(product['produto']['precoBruto'])
                issue.append(product['produto']['data'])
                address.append(product['estabelecimento']['endLogradouro'] + ' ' + product['estabelecimento']['endNumero'] + ' ' + product['estabelecimento']['bairro'] + ' ' + product['estabelecimento']['cep'] + ', ' + product['estabelecimento']['municipio'])
                distance.append(product['estabelecimento']['distancia'])

            dict = {'Product Name': name, 'Product Bar Code': barCode, 'Price': price, 'Issue Date': issue, 'Address': address, 'Approximate Distance': distance} 
            df = pd.DataFrame(dict)
            print("\n", df)
            df.to_csv(keyword+'.csv', encoding='utf-8-sig')

        else:
            print(proRes['descricao'])
    else:
        print(locRes['descricao'])

except:
    print('\nPlease enter your zip code correctly (*****-***)')