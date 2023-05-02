import requests

url = "https://mercados.ambito.com/dolar/informal/variacion"

def get_ambito_values():
    try:
        return requests.get(url)
    except:
        response = requests.Response()
        response.status_code = 500
        return response
