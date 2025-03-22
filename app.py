from  flask import Flask, request, jsonify
import mysql.connector

NOT_FOUND = 404

app = Flask(__name__)

def build_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="localhost",
        database="users"
    )

def data_db_sql_select(sql):
    connection = build_connection()
    
    cursor = connection.cursor()
    cursor.execute(sql)

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result

def data_sql_insert(sql):
    connection = build_connection()

    cursor = connection.cursor()
    cursor.execute(sql)

    cursor.close
    connection.close()

def data_db_sql_update(sql):
    connection = build_connection()

    cursor = connection.cursor()
    cursor.execute(sql)

    connection.commit()

    cursor.close()
    connection.close()

def data_delete_sql(sql):
    connection = build_connection()

    cursor = connection.cursor()
    cursor.execute(sql)

    connection.commit()

    cursor.close()
    connection.close()

def build_update_sql(request, id):
    first_part_update = "UPDATE users SET "
    last_part_update = " WHERE id = " + id

    mean_words= []
    data = request.get_json()

    for key in data.keys():
        value = data[key]
        mean_words.append(f"{key}=\"{value}\"")

    mean_part_update_sql = ",".join(mean_words)
    return first_part_update + mean_part_update_sql + last_part_update

def build_insert_sql(request):
    first_part_insert = "INSERT INTO users "
    last_part_insert = " VALUES " 

    mean_words= []
    data = request.get_json()

    for key in data.keys():
        value = data[key]
        mean_words.append(f"{key}=\"{value}\"")

    mean_part_update_sql = ",".join(mean_words)
    return first_part_insert + mean_part_update_sql + last_part_insert


def get_id_user(id):

    if id == None:
        return jsonify({"message":"Inform your id if exists"}), NOT_FOUND
    
    user = data_db_sql_select("SELECT * FROM users WHERE id = " + id)

    if user == None:
        return jsonify({"message":"This user does not exist"}), NOT_FOUND

def validate_data(data):
    required_fields = ["name", "lastname", "age"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message":"Field {field} is required"})
    
@app.route("/user", methods=["GET"])
def get_user():
    id = request.args.get("id")

    if id == None:
        return jsonify({"message":"Inform your id if exists"}), NOT_FOUND

    user = data_db_sql_select("SELECT * FROM users WHERE id = " + id)

    if user == None:
        return jsonify({"message":"This user does not exist"}), NOT_FOUND

    return jsonify(user)

@app.route("/user", methods=["POST"])
def insert_user():
    data = request.json;
    validate_data(data)



    return jsonify({"message": "The user was created"})

@app.route("/user", methods=["PUT"])
def update_user():
    id = request.args.get("id")

    get_id_user(id)

    update_sql = build_update_sql(request, id)
    data_db_sql_update(update_sql)

    return jsonify({"message": "update was done successfully"})

@app.route("/user", methods=["DELETE"])
def delete_user():
    id = request.args.get("id")

    get_id_user(id)

    data_delete_sql("DELETE FROM users WHERE id = " + id)
    return jsonify({"message":"User deleted"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
