
import requests
from bs4 import BeautifulSoup

from .generate_synthetic_prices import generate_synthetic_data


def fetch_odop_data():


    url = "https://pmfme.cftri.res.in/odop/odopdata.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    product_names = parse_product_names(soup)
    
    product_prices = generate_synthetic_data(product_names)
    
    return product_names, product_prices

def parse_product_names(soup):
    product_names = []
    table = soup.find("table")  # Find the first table (you may need to refine this)
    rows = table.find_all("tr")
    
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 0:
            product_names.append(cols[0].text.strip())  # Assuming the first column has the product name
            
    return product_names
