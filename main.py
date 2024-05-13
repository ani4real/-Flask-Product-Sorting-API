from flask import Flask, jsonify
import requests
import os
import json

app = Flask(__name__)

@app.route('/sample_data', methods=['GET'])
def get_data():                                     #don't need to call this function as Flask already calls the function
    try:
        response = requests.get('https://dummyjson.com/products')
        data = response.json()

        if response.status_code == 200:
            print("success!")
            sorted_data = sort_data(data)
            create_json_files(sorted_data)
            return jsonify(sorted_data), 200
        else:
            return jsonify({'error': 'Failed to fetch data'}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def sort_data(data):
    sorted_data = {"Products": {}}

    sorted_products = sorted(data["products"], key=lambda x: (x["category"], x["brand"], -x["price"]))    # sorting based on price in decreasing order

    for product in sorted_products:
        category = product["category"]
        brand = product["brand"]

        if category not in sorted_data["Products"]:
            sorted_data["Products"][category] = {}

        if brand not in sorted_data["Products"][category]:
            sorted_data["Products"][category][brand] = []

        sorted_data["Products"][category][brand].append(product)

    return sorted_data


def create_json_files(sorted_data): 
    for category, brands in sorted_data["Products"].items():
        for brand, products in brands.items():
            brand_directory = os.path.join('output', brand)
            if not os.path.exists(brand_directory):
                os.makedirs(brand_directory)
            
            filename = os.path.join(brand_directory, f"{brand}.json")
            with open(filename, 'w') as f:
                json.dump(products, f)
        
if __name__ == '__main__':
    app.run(port=5000, debug=True)


