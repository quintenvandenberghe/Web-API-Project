import requests
from io import BytesIO
from PIL import Image

BASE_URL = "https://dog.ceo/api"

def fetch_all_breeds():
    response = requests.get(f"{BASE_URL}/breeds/list/all")
    response.raise_for_status()
    return response.json()["message"]

def fetch_breed_images(breed, count):
    url = f"{BASE_URL}/breed/{breed}/images/random/{count}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["message"]

def fetch_sub_breed_images(breed, sub_breed, count):
    url = f"{BASE_URL}/breed/{breed}/{sub_breed}/images/random/{count}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["message"]

def show_image_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        img.show()
    except Exception as e:
        print(f"Fout bij tonen van afbeelding: {e}")

def main():
    print("Wat wil je doen?")
    print("1. Toon random foto's van een ras")
    print("2. Toon random foto's van een subras")
    print("3. Toon random foto's van een willekeurig ras")
    while True:
        keuze = input("Maak een keuze (1/2/3): ").strip()
        if keuze in ("1", "2", "3"):
            break
        print("Ongeldige keuze. Probeer opnieuw.")
    breeds = fetch_all_breeds()
    breed_list = list(breeds.keys())
    if keuze == "1":
        while True:
            for idx, breed in enumerate(breed_list, 1):
                print(f"{idx}. {breed}")
            try:
                breed_idx = int(input("Voer het nummer van het ras in: ")) - 1
                breed = breed_list[breed_idx]
                print(f"Je koos: {breed}")
                break
            except (ValueError, IndexError):
                print("Ongeldige keuze ras. Probeer opnieuw.")
        while True:
            try:
                count = int(input("Hoeveel random foto's wil je zien? "))
                if count < 1:
                    print("Aantal moet minimaal 1 zijn. Probeer opnieuw."); continue
                print(f"Je koos voor {count} foto('s).")
                break
            except ValueError:
                print("Ongeldig aantal. Probeer opnieuw.")
        images = fetch_breed_images(breed, count)
        for url in images:
            show_image_from_url(url)
    elif keuze == "2":
        while True:
            for idx, breed in enumerate(breed_list, 1):
                print(f"{idx}. {breed}")
            try:
                breed_idx = int(input("Voer het nummer van het ras in: ")) - 1
                breed = breed_list[breed_idx]
                if not breeds[breed]:
                    print("Dit ras heeft geen subrassen. Kies een ander ras."); continue
                print(f"Je koos: {breed}")
                break
            except (ValueError, IndexError):
                print("Ongeldige keuze ras. Probeer opnieuw.")
        while True:
            for idx, sub in enumerate(breeds[breed], 1):
                print(f"{idx}. {sub}")
            try:
                sub_idx = int(input("Voer het nummer van het subras in: ")) - 1
                sub_breed = breeds[breed][sub_idx]
                print(f"Je koos subras: {sub_breed}")
                break
            except (ValueError, IndexError):
                print("Ongeldige keuze subras. Probeer opnieuw.")
        while True:
            try:
                count = int(input("Hoeveel random foto's wil je zien? "))
                if count < 1:
                    print("Aantal moet minimaal 1 zijn. Probeer opnieuw."); continue
                print(f"Je koos voor {count} foto('s).")
                break
            except ValueError:
                print("Ongeldig aantal. Probeer opnieuw.")
        images = fetch_sub_breed_images(breed, sub_breed, count)
        for url in images:
            show_image_from_url(url)
    elif keuze == "3":
        import random
        breed = random.choice(breed_list)
        print(f"Willekeurig gekozen ras: {breed}")
        while True:
            try:
                count = int(input("Hoeveel random foto's wil je zien? "))
                if count < 1:
                    print("Aantal moet minimaal 1 zijn. Probeer opnieuw."); continue
                print(f"Je koos voor {count} foto('s).")
                break
            except ValueError:
                print("Ongeldig aantal. Probeer opnieuw.")
        images = fetch_breed_images(breed, count)
        for url in images:
            show_image_from_url(url)

if __name__ == "__main__":
    main()
