import requests
import pandas as pd

keyword = input('\nKeyword: ')

headers = {
    'Cookie': 'session=eyJjc3JmX3Rva2VuIjoiYjU3MjY0NjJiMTIyNDRhMGQyMTM0ZGQzZWZmZjk3NmE0N2VhODAzYiJ9.YYS90g.sukA-o3wSb7Z7UDnu-vGMlSH8s4; token=7druNGgoRl4vv-CuRZCbY0-uEQLOHYHpbFcSxiMatVn0xFq51992W0fUTAaEoA4rfOH15Q0elMSRDUEUqRDFRDvop84',
    'X-CSRFToken': 'ImI1NzI2NDYyYjEyMjQ0YTBkMjEzNGRkM2VmZmY5NzZhNDdlYTgwM2Ii.YYS98Q.cc3irB4uWUfaWZyOWocCiLGqkGU',
    'X-Requested-With': 'XMLHttpRequest'
}

payload = {
    'termo': keyword,
    'horas': 72,
    'latitude': -12.97111,
    'longitude': -38.51083,
    'raio': 15,
    'pagina': 1,
    'ordenar': 'preco.asc',
}

res = requests.post('https://precodahora.ba.gov.br/produtos/', headers=headers, data=payload).json()

if res['codigo'] == 80:

    products = res['resultado']

    name = []
    barCode = []
    price = []
    issue = []
    address = []
    distance = []

    for i, product in enumerate(products):

        if i > 10:
            break

        name.append(product['produto']['descricao'])
        barCode.append(product['produto']['gtin'])
        price.append(product['produto']['precoBruto'])
        issue.append(product['produto']['data'])
        address.append(product['estabelecimento']['endLogradouro'])
        distance.append(product['estabelecimento']['distancia'])

    dict = {'Product Name': name, 'Product Bar Code': barCode, 'Price': price, 'Issue Date': issue, 'Address': address, 'Approximate Distance': distance} 

    df = pd.DataFrame(dict)

    print("\n", df)

    df.to_csv(keyword+'.csv', encoding='utf-8-sig')

else:
    print("\nNo Result")