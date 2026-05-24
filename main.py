from logging import raiseExceptions

import httpx
import ssl
import pandas as pd

from httpx import HTTPError

# Low security context for CEPIK API
ssl_context = ssl.create_default_context()
ssl_context.set_ciphers('DEFAULT:@SECLEVEL=1')

PATH = "data/test_data/vehicles.csv"
URL = "https://api.cepik.gov.pl/pojazdy"
params_vehicles = {
    'wojewodztwo': '24',
    'data-od': '19250101',
    'data-do': '19260101',
    'pokaz-wszystkie-pola': 'false'
}



def vehicles_endpoint_fetch(url, params=None):
    car_list = []
    with httpx.Client(verify=ssl_context) as client:
        r = client.get(url, params=params)

        if r.status_code == 200:
            response_json = r.json().get('data')
            for item in response_json:
                ids = item.get('id')
                attribute = item.get('attributes')
                attribute = list(attribute.values())
                car_list.append([ids,attribute])
            new_list = [[item[0], *item[1]] for item in car_list]
            return new_list

        else:
            raise HTTPError(str(r.status_code))

def save_to_csv(data, path):
    df = pd.DataFrame(data)
    save_csv = df.to_csv(path, index=False)
    return save_csv


if __name__ == "__main__":
    cars = vehicles_endpoint_fetch(URL, params_vehicles)
    print(cars)
