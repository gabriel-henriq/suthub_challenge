import requests
import json
import csv
from http import HTTPStatus

"""_Author_: Gabriel Henrique
"""

"""_summary_
    Criar um CSV que possue duas colunas (nome_pet e contador).
    Identificar como acessar a informação do pet dos contratos-
    que tiverem pet e registrar/contabilizar cada nome de pet.
    
    URL: 
    Headers: "Content-Type": "application/json",  
    "api_key": ""
    Method: GET
"""

api_url = ""
headers = {'Content-Type': 'application/json', 'api_key': ''}


def main():
    try:
        response = fetch_content_to_dict(api_url, headers)
        pet_names = get_pet_names_from_response_dict(response)
        pet_names_count_list = {pet_name: pet_names.count(pet_name) for pet_name in pet_names}
        create_csv_file(pet_names_count_list)
    except Exception as e:
        print(f"Error: {e}")


def fetch_content_to_dict(url: str, headers: dict):
    response = requests.get(url, headers=headers)
    if response.status_code == HTTPStatus.OK:
        return json.loads(response.content)
    elif response.status_code == HTTPStatus.BAD_REQUEST:
        raise Exception(f"status_code: {response.status_code} Bad Request")
    elif response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        raise Exception(f"status_code: {response.status_code} Internal Server Error")
    else:
        raise Exception(f"Unknown error with code status: {response.status_code}")


def get_pet_names_from_response_dict(dict_response: dict):
    pet_names = []
    for policies in dict_response["response"]:
        for policy in policies["policies"]:
            for covered_goods in policy["covered_goods"]:
                if 'Nome' in covered_goods:
                    pet_names.append(covered_goods["Nome"])
    return pet_names


def create_csv_file(dict_response: dict):
    file_name = "data.csv"
    with open(file_name, "w", newline='') as csvFile:
        coluns = ['nome_pet', 'contador']
        writer = csv.DictWriter(csvFile, fieldnames=coluns)
        writer.writeheader()
        for nm, ct in dict_response.items():
            writer.writerow({'nome_pet': nm, 'contador': ct})
        print(f"File {file_name} has been created successfully!")


if __name__ == '__main__':
    main()
