
import pandas as pd
import requests
from bs4 import BeautifulSoup
from Lawyer import Lawyer

baseUrl = "https://www.avocatsdemartinique.com"
uri = "/le-barreau/annuaire-des-avocats/"

finalUrl = baseUrl + uri

response = requests.get(finalUrl)
soup = BeautifulSoup(response.text, 'lxml')
lawyer_cards = soup.findAll('div', class_='cn-entry')


def get_lawyer(lawyer_card):
    try:

        first_name = lawyer_card.find('span', class_='given-name').text
        last_name = lawyer_card.find('span', class_='family-name').text
        email = lawyer_card.find('span', class_='email-address').text
        address = lawyer_card.find('span', class_='adr cn-address').text

        return Lawyer(first_name, last_name, email, address)
    except AttributeError:
        return None


def format_lawyers(lawyers_array):
    lawyers_data = []
    for lawyer in lawyers_array:
        if lawyer:
            lawyer_dict = {
                'Prénom': lawyer.get_name(),
                'Nom': lawyer.get_last_name(),
                'Email': lawyer.get_email(),
                'Adresse': lawyer.get_address(),
            }
            lawyers_data.append(lawyer_dict)

    return lawyers_data


def main():
    lawyers = []
    for lawyer_card in lawyer_cards:
        lawyer = get_lawyer(lawyer_card)
        if lawyer:
            lawyers.append(lawyer)

    lawyers_data = format_lawyers(lawyers)

    df = pd.DataFrame(lawyers_data)
    df.to_csv('andy.csv', index=False)

    print("Liste des avocats récupérés :", len(lawyers))

if __name__ == "__main__":
    main()
