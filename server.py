import math
from decimal import Decimal

from flask import Flask, request, jsonify
import collections
import uuid

app = Flask(__name__)

"""
Below are some global variables for the application.
receipts = a list that stores all the receipts for a session.
totalPoints = a dictionary that stores the ID and total points for each receipt.
"""

receipts = []
totalPoints = collections.defaultdict(int)

"""
Description: 
1) Accepts POST request with receipt as a JSON body.
2) Counts points according to rules specified.
3) Updates all global variables accordingly.

Returns:
1) JSON object that contains the ID for the receipt
2) Error message if the receipt is not valid
"""
@app.route('/receipts/process', methods=['POST'])
def process_receipts():
    try:
        receipt = request.get_json()
        if not receipt:
            return jsonify({"error": "Invalid receipt data provided."}), 400

        receipt_id = uuid.uuid4()
        points = 0

        # One point for every alphanumeric character in the retailer name
        points += sum(c.isalnum() for c in receipt['retailer'])

        total_price = Decimal(receipt['total'])

        # 50 points if the total is a round dollar amount with no cents.
        if total_price % 1 == 0:
            points += 50

        # 25 points if the total is a multiple of 0.25
        if total_price % Decimal("0.25") == 0:
            points += 25

        # 5 points for every two items on the receipt.
        items = receipt['items']
        points += (len(items) // 2) * 5

        # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer.
        # The result is the number of points earned.
        for item in items:
            trimmed_length = len(item['shortDescription'].strip())
            if trimmed_length % 3 == 0:
                points += math.ceil(float(item['price']) * 0.2)

        # 6 points if the day in the purchase date is odd.
        day = int(receipt['purchaseDate'].split('-')[2])
        if day % 2 == 1:
            points += 6

        # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        hour = int(receipt['purchaseTime'].split(":")[0])
        if 14 <= hour < 16:
            points += 10

        totalPoints[receipt_id] = points
        print(totalPoints)
        return jsonify({"id": receipt_id})

    except KeyError as e:
        missing_field = e.args[0]
        return jsonify({"error": f"Missing receipt field: {missing_field}"}), 400

    except:
        return 'Error occurred while processing the receipt !!'


"""
Description: accepts GET request to get total points for given receipt ID.
Returns: JSON object that contains the total points.
"""
@app.route('/receipts/<uuid:receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    return jsonify({"points": totalPoints.get(receipt_id)})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)