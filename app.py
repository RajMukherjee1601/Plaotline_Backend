from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "mongodb+srv://rajmukherjee1601:0dBZfnllyiAvmRtj@cluster0.grwr7ep.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client.get_database('Plotline')


def calculate_tax(price): #Tax calculation for product
    if price > 5000:
        return price * 0.18  # Tax PB
    elif 1000 < price <= 5000:
        return price * 0.12  # Tax PA
    else:
        return 200  # Tax PC

def calculate_service_tax(price):#Tax calculation for service
    if price > 8000:
        return price * 0.15  # Tax SB
    elif 1000 < price <= 8000:
        return price * 0.10  # Tax SA
    else:
        return 100  # Tax SC


@app.route('/signup', methods=['POST']) #Signup
def signup():
    collection = db['User_login'] #database name
    try:
        data = request.json
        if data:
            collection.insert_one(data)
            return jsonify({"message": "User added successfully"}), 201
        else:
            return jsonify({"message": "No data provided"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/product/insert', methods=['POST'])
def insert_product_data():#insert data for product
    collection = db['product']
    try:
        data = request.json
        if data:
            collection.insert_one(data)
            return jsonify({"message": "Data inserted successfully"}), 201
        else:
            return jsonify({"message": "No data provided"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/service/insert', methods=['POST'])# insert data for service
def insert_service_data():
    collection = db['Service']
    try:
        data = request.json
        if data:
            collection.insert_one(data)
            return jsonify({"message": "Data inserted successfully"}), 201
        else:
            return jsonify({"message": "No data provided"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/product/retrieve', methods=['GET']) #Retrive data for product
def retrieve_product_data():
    collection = db['product']
    try:
        users = collection.find({})
        result = []
        if users:
            for user in users:
                result.append({
                    "name": user["Name"],
                    "price": user["price"],
                })
            return {"users": result}
        else:
            return jsonify({"message": "No data found in database"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/service/retrieve', methods=['GET'])#retrive data for service
def retrieve_service_data():
    collection = db['Service']
    try:
        users = collection.find({})
        result = []
        if users:
            for user in users:
                result.append({
                    "name": user["Name"],
                    "price": user["price"],
                })
            return {"users": result}
        else:
            return jsonify({"message": "No data found in database"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/product/remove', methods=['POST']) #Remove data for product database
def remove_product_data():
    collection = db['product']
    users = collection.find({})
    user_name = []
    if users:
        for user in users:
            user_name.append(user["Name"])
    try:
        data = request.json
        print(data.get("Name"))
        print(user_name)
        if data.get("Name") in user_name:
            result = collection.delete_one({"Name": data.get("Name")})
            if result.deleted_count > 0:
                return jsonify({"message": "Data removed successfully"}), 200
            else:
                return jsonify({"message": "No matching data found"}), 404
        else:
            return jsonify({"message": "Missing 'name' field in request data"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/service/remove', methods=['POST'])#remove data for service database
def remove_service_data():
    collection = db['Service']
    users = collection.find({})
    user_name = []
    if users:
        for user in users:
            user_name.append(user["Name"])
    try:
        data = request.json
        print(data.get("Name"))
        print(user_name)
        if data.get("Name") in user_name:
            result = collection.delete_one({"Name": data.get("Name")})
            if result.deleted_count > 0:
                return jsonify({"message": "Data removed successfully"}), 200
            else:
                return jsonify({"message": "No matching data found"}), 404
        else:
            return jsonify({"message": "Missing 'name' field in request data"}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/product/clear', methods=['DELETE'])#remove data from product
def clear_product_data():
    collection = db['product']
    try:
        result = collection.delete_many({})
        return jsonify({"message": f"{result.deleted_count} documents deleted"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/service/clear', methods=['DELETE'])#remove data from service
def clear_service_data():
    collection = db['Service']
    try:
        result = collection.delete_many({})
        return jsonify({"message": f"{result.deleted_count} documents deleted"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/product/calculate_bill', methods=['GET'])#calculate bill for product
def calculate_product_bill():
    collection = db['product']
    try:
        products = collection.find({})
        total_bill = 0

        for product in products:
            price = product["price"]
            tax = calculate_tax(price)
            total_price = price + tax
            total_bill += total_price

        return jsonify({"total_bill": total_bill}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/service/calculate_bill', methods=['GET'])#calculate bill for service
def calculate_service_bill():
    collection = db['Service']
    try:
        products = collection.find({})
        total_bill = 0

        for product in products:
            price = product["price"]
            tax = calculate_service_tax(price)
            total_price = price + tax
            total_bill += total_price

        return jsonify({"total_bill": total_bill}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/product/confirm_order', methods=['POST'])# confirm order for product
def confirm_product_order():
    collection = db['product']
    try:
        data = request.json
        if data.get("value").lower() == "yes":
            response = calculate_product_bill()
            print(response[0])
            # clear_data()
            # return jsonify({"Your Order has been confirmed with the bill value of ": amount["total_bill"]}), 200
            return "Your Order is confirmed", 200
        else:
            return "Your Order is not confirmed", 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/service/confirm_order', methods=['POST']) #confirm order for service
def confirm_service_order():
    collection = db['service']
    try:
        data = request.json
        if data.get("value").lower() == "yes":
            response = calculate_service_bill()
            print(response[0])
            # clear_data()
            # return jsonify({"Your Order has been confirmed with the bill value of ": amount["total_bill"]}), 200
            return "Your Order is confirmed", 200
        else:
            return "Your Order is not confirmed", 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)