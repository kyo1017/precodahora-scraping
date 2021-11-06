import requests, time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

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

keyword = input('\nKeyword: ')
zipCode = input('\nZip Code: ')

payload = {
    'termo': keyword,
    'horas': 72,
    'latitude': -12.97111,
    'longitude': -38.51083,
    'raio': 15,
    'pagina': 1,
    'ordenar': 'preco.asc',
}

res = session.post('https://precodahora.ba.gov.br/produtos/', headers=headers, cookies=cookie, data=payload).json()

if res['codigo'] == 80:
    
    products = res['resultado']

    for i, product in enumerate(products):
        if i > 10:
            break
        name.append(product['produto']['descricao'])
        barCode.append(product['produto']['gtin'])
        price.append(product['produto']['precoBruto'])
        issue.append(product['produto']['data'])
        df = product['estabelecimento']['endLogradouro'] + ' ' + product['estabelecimento']['endNumero'] + ' ' + product['estabelecimento']['bairro'] + ' ' + product['estabelecimento']['cep'] + ', ' + product['estabelecimento']['municipio']
        address.append(df)

    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')
    chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    chromeOptions.add_argument('--log-level=3')
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions)
    browser.get('https://precodahora.ba.gov.br/')

    browser.find_element_by_id('fake-sbar').click()
    browser.find_element_by_id('top-sbar').send_keys(keyword)
    browser.find_element_by_class_name('btn-top-sbar').click()

    browser.find_element_by_css_selector('.location-box button').click()
    time.sleep(1)
    browser.find_element_by_id('add-address').click()
    time.sleep(1)
    browser.find_element_by_id('my-zip').send_keys(zipCode)
    browser.find_element_by_id('sel-cep').click()
    time.sleep(5)

    products = browser.find_elements_by_class_name('item-list')

    for i, product in enumerate(products):
        if i > 10:
            break
        data = product.find_elements_by_css_selector('.flex-item2 div')
        if 'Km' in data[5].text:
            distance.append(data[5].text)
        else:
            distance.append(data[6].text)

    browser.quit()

    dict = {'Product Name': name, 'Product Bar Code': barCode, 'Price': price, 'Issue Date': issue, 'Address': address, 'Approximate Distance': distance} 
    df = pd.DataFrame(dict)
    print("\n", df)
    df.to_csv(keyword+'.csv', encoding='utf-8-sig')

else:
    print(res['descricao'])