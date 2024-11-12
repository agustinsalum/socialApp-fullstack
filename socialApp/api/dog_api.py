
import requests

def get_random_dog_image():
    base_url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(base_url)
    return response.json()