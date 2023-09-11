from flask import Flask, jsonify,request
import psycopg2
from database.database_connect import DatabaseConnect
from datetime import datetime,date



app = Flask(__name__)

db=DatabaseConnect()  # PostgreSQL database

@app.route('/data', methods=['GET'])
def get_data():
    try:
        data=db.executeQuery("SELECT * from PropertyDetails;")
        
        # Convert data to a list of dictionaries
        data_dict = [{'id': row[0], 'docno': row[1], 'doctype': row[2], 'Office': row[3], 'year': row[4], 'Buyername': row[5], 'Sellername': row[6], 'otherinfo': row[7], 'listno': row[8]} for row in data]

        return jsonify(data_dict)

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/namesearch', methods=['GET'])
def partial_text_search():
    query = request.args.get('query', '')
    results = []
    data=db.executeQuery("SELECT * from PropertyDetails;")
    
    data_dict = [{'id': row[0], 'docno': row[1], 'doctype': row[2], 'Office': row[3], 'year': row[4], 'Buyername': row[5], 'Sellername': row[6], 'otherinfo': row[7], 'listno': row[8]} for row in data]

    for item in data_dict:
        if query.lower() in item['Buyername'].lower() or query.lower() in item['Sellername'].lower():
            results.append(item)
    response = {"Status": "Success", "data": results, "Length": len(results)}

    if results:
        # Return a JSON response indicating success with the results and length
        return jsonify(response)
    else:
        # Return a JSON response indicating failure with an error message
        return jsonify({"status": "Fail", "message": "No matching data found.", "length": 0}), 404  
    
@app.route('/docnosearch', methods=['GET'])
def search_by_docno():
    docno = request.args.get('docno')

    results = []
    data=db.executeQuery("SELECT * from PropertyDetails;")
    data_dict = [{'id': row[0], 'docno': row[1], 'doctype': row[2], 'Office': row[3], 'year': row[4], 'Buyername': row[5], 'Sellername': row[6], 'otherinfo': row[7], 'listno': row[8]} for row in data]

    for item in data_dict:
        if str(item.get('docno')) == docno:
            results.append(item)

    if results:
        return jsonify({"Status": "Success", "results": results}), 200
    else:
        return jsonify({"Status": "Fail", "message": "No matching data found."}), 404

@app.route('/Yearsearch', methods=['GET'])
def search_by_year():
    data=db.executeQuery("SELECT * from PropertyDetails;")
    data_dict = [{'id': row[0], 'docno': row[1], 'doctype': row[2], 'Office': row[3], 'year': row[4], 'Buyername': row[5], 'Sellername': row[6], 'otherinfo': row[7], 'listno': row[8]} for row in data]

    year_param = request.args.get('year')

    try:
        year_param = int(year_param)  # Convert year parameter to an integer
    except ValueError:
        return jsonify({"status": "Fail", "message": "Invalid year parameter."}), 400

    results = []
    for item in data_dict:
        if isinstance(item.get('year'), date):  # Check if 'year' is a date object
            item_year = item.get('year').year
        else:
            try:
                item_year = datetime.strptime(item.get('year'), "%Y-%m-%d").year
            except ValueError:
                continue  # Skip records with invalid date formats

        if item_year == year_param:
            results.append(item)

    if results:
        return jsonify({"Status": "Success", "results": results,"Length":len(results)}), 200
    else:
        return jsonify({"Status": "Fail", "message": "No matching data found."}), 404

@app.route('/addresssearch', methods=['GET'])
def search_by_address():
    address_param = request.args.get('address')

    results = []
    data=db.executeQuery("SELECT * from PropertyDetails;")
    data_dict = [{'id': row[0], 'docno': row[1], 'doctype': row[2], 'Office': row[3], 'year': row[4], 'Buyername': row[5], 'Sellername': row[6], 'otherinfo': row[7], 'listno': row[8]} for row in data]

    for item in data_dict:
        other_info = item.get('otherinfo')
        if address_param.lower() in other_info.lower():
            results.append(item)

    if results:
        return jsonify({"Status": "Success", "results": results}), 200
    else:
        return jsonify({"Status": "Fail", "message": "No matching data found."}), 404

def runFlaskApp(debug=True):
    app.run(debug=True)
# if __name__ == '__main__':
#     app.run(debug=True)

