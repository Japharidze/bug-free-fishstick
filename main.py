import requests
import pandas as pd
from bs4 import BeautifulSoup as BS

def get_names(id: str):
    dt = {
        'c': 'search',
        'm': 'find_legal_persons',
        's_legal_person_idnumber': id
    }
    r = requests.post("https://enreg.reestri.gov.ge/main.php?m=new_index", data=dt)
    soup = BS(r.text.encode('ISO-8859-1'))
    name = soup.select_one('td ~ td ~ td ~ td').text.strip()
    unit = soup.select_one('td ~ td ~ td ~ td ~ td').text.strip()
    return name, unit

codes = pd.read_csv('media/data.csv')

result = pd.DataFrame(columns=['tax', 'name', 'unit'])

for _, row in codes.iterrows():
    tax = row['TaxCode']
    name, unit = get_names(tax)
    result = pd.concat([result, pd.Series({
        'tax': tax, 
        'name': name,
        'unit': unit
    }).to_frame().T])

result.to_csv('media/output.csv', index=False)