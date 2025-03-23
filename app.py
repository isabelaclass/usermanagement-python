from  flask import Flask, request, jsonify
import mysql.connector

NOT_FOUND = 404
BAD_REQUEST = 400

app = Flask(__name__)

# Database connection
def build_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="localhost",
        database="users"
    )

# Generic function to exeute queries
def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    connection = build_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)

    result = None

    if fetch_one:
        result = cursor.fetchone()
    elif fetch_all:
        result = cursor.fetchall()
    elif commit:
        connection.commit()
    
    cursor.close()
    connection.close()

    return result

# Validate if required fields are present
def validate_data(data):
    required_fields = ["name", "lastname", "age"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message":f"Field '{field}' is required"}), BAD_REQUEST

# Validate if user id exists in database
def get_user_by_id(user_id):
    user = execute_query("SELECT * FROM users WHERE id = %s", (user_id,), fetch_one=True)
    if not user:
        return jsonify({"message":"User not found"}), NOT_FOUND
    return user

# Route GET to search for an user by the id 
@app.route("/user", methods=["GET"])
def get_user():
    user_id = int(request.args.get("id"))
    if not user_id:
        return jsonify({"message":"Please provide a user ID"}), BAD_REQUEST

    user = get_user_by_id(user_id)

    return jsonify(user)

# Route to insert a new user into database
@app.route("/user", methods=["POST"])
def insert_user():
    data = request.json;
    validation_error = validate_data(data)

    if validation_error:
        return validation_error

    query = "INSERT INTO users (name, lastname, age) VALUE (%s, %s, %s)"
    params = (data["name"], data["lastname"], data["age"])
    execute_query(query, params, commit=True)

    return jsonify({"message": "User created successfully"}), 201

# Route to update an user by the ID
@app.route("/user", methods=["PUT"])
def update_user():
    user_id = request.args.get("id")
    if not user_id:
        return jsonify({"message": "Please provide an user ID"}), BAD_REQUEST
    
    user = get_user_by_id(user_id)

    if isinstance(user, tuple):
        return user
    
    data = request.json
    update_fields = ",".join(f"{key} = %s" for key in data.keys())
    query = f"UPDATE users SET {update_fields} WHERE id = %s"
    params = tuple(data.values()) + (user_id,)

    execute_query(query, params, commit=True)
    return jsonify({"message": "User updated successfully"}), 200

# Route to delete an user by the ID
@app.route("/user", methods=["DELETE"])
def delete_user():
    user_id = int(request.args.get("id"))
    if not user_id:
        return jsonify({"message": "Please provide an user ID"}), BAD_REQUEST
    
    user = get_user_by_id(user_id)
    if isinstance(user, tuple):
        return user

    execute_query("DELETE FROM users WHERE id = %s", (user_id,), commit=True)
    return jsonify({"message":"User deleted successfully"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
