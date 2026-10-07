from typing import Dict, Any, List


# Start here
def process(data: Dict[str, Any]) -> str:
    # return the 'name' field from the dictionary
    return data['name']    

def extract_product_names(products: List[Product]) -> List[str]:
    # iterate over products and return a list of each product's name
    return [product.name for product in products]