
def get_http_cat_image(status_code):
    base_url = f"https://http.cat/{status_code}.jpg"
    return {'url': base_url}