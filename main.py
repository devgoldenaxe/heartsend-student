from flask import Flask, request, jsonify
from rec_system import module  # Importing the actual module function

app = Flask(__name__)

@app.route("/")
def hello_world():
    School_id = request.args.get('School_id')  
    user_id = request.args.get('profile_id')
    version = request.args.get('version', 'test')

    print(f"DEBUG: School_id = {School_id}, user_id = {user_id}")

    if School_id is None:
        return "ERROR: School_id is missing!", 400  # Return an error response instead of crashing

    result = module(School_id, user_id , version) 
    # print(result) # Call the imported module function
    return jsonify({
        "result": result
    })  # Ensure module() returns a valid response

if __name__ == "__main__":
    app.run(debug=True)
