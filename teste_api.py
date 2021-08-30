import random
import string
from base64 import b64encode
from concurrent.futures import ThreadPoolExecutor

import requests

""" 
    Script de teste da API
    Este script irá realizar 20 chamadas simultaneamente para:
     - criar clientes com dados aleatorios
     - atualizar o nome dos clientes
     - adicionar alguns produtos favoritos
     - remover o clientes criados
    Para rodar este script nao é necessário nenhuma dependencia do projeto e basta executar:
    python teste_api.py 
"""

username = "admin"
password = "teste123"
endpoint_customer = "http://localhost:8000/app/customer/"
endpoint_favorite = "http://localhost:8000/app/customer/{customer_id}/favorite/"
number_tests = 20

def main():
    pool = ThreadPoolExecutor(max_workers=20)
    for c in pool.map(test_customer, range(number_tests)):
        print(f'Customer {c} finished')
    print('Program Finished.')

def test_customer(n):
    print(f'Iniciando teste #{n+1}')
    customer = create_customer()
    update_customer(customer)
    add_products(customer)
    view_favorites(customer)
    remove_customer(customer)
    return customer["id"]

def create_customer():
    headers = get_headers()
    data = {
        "name": ''.join(random.choice(string.ascii_lowercase) for _ in range(20)),
        "email": ''.join(random.choice(string.ascii_lowercase) for _ in range(5)) + '@' + 'teste.com',
    }
    response = requests.post(endpoint_customer, json=data, headers=headers, timeout=10)
    response.raise_for_status()
    result = response.json()
    print(f"Customer {result['id']} created.")
    return result


def update_customer(customer):
    headers = get_headers()
    data = {
        "id": customer['id'],
        "name": ''.join(random.choice(string.ascii_lowercase) for _ in range(20)),
        "email": ''.join(random.choice(string.ascii_lowercase) for _ in range(5)) + '@' + 'teste.com',
    }
    response = requests.put(endpoint_customer, json=data, headers=headers, timeout=10)
    response.raise_for_status()
    result = response.json()
    print(f"Customer {result['id']} modified.")
    return result


def add_products(customer):
    headers = get_headers()
    data = {
        "product": "79b1c283-00ef-6b22-1c8d-b0721999e2f0",
    }
    url = endpoint_favorite.replace("{customer_id}", customer["id"])
    response = requests.post(url, json=data, headers=headers, timeout=10)
    response.raise_for_status()
    result = response.json()
    print(f"Favorite Item {result['id']} created.")
    return result


def view_favorites(customer):
    headers = get_headers()
    url = endpoint_favorite.replace("{customer_id}", customer["id"])
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    result = response.json()
    for f in result["favorites"]:
        print(f"Favorite item from customer {customer['id']}: {f['id']}")
    return result


def remove_customer(customer):
    headers = get_headers()
    url = f"{endpoint_customer}{customer['id']}/"
    response = requests.delete(url, headers=headers, timeout=10)
    response.raise_for_status()
    print(f"Customer removed.")


def get_headers():
    user_pass = b64encode(f"{username}:{password}".encode()).decode("ascii")
    headers = {'Authorization': f"Basic {user_pass}"}
    return headers


if __name__ == "__main__":
    main()

