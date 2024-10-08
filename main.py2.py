from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


# Initialize the Flask application and Marshmallow
app = Flask(__name__)
ma = Marshmallow(app)

# Database connection function
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Change to your host
            user='your_username',  # Change to your MySQL username
            password='your_password',  # Change to your MySQL password
            database='fitness_center'  # Change to your database name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

db_connection = create_connection()

# Members Table Schema
class Member(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'name', 'age', 'email')

# WorkoutSessions Table Schema
class WorkoutSession(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ('id', 'member_id', 'date', 'activity', 'duration')

# Task 2: CRUD Operations for Members

@app.route('/members', methods=['POST'])
def add_member():
    name = request.json['name']
    age = request.json['age']
    email = request.json['email']
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO Members (name, age, email) VALUES (%s, %s, %s)", (name, age, email))
    db_connection.commit()
    return jsonify({'message': 'Member added successfully!'}), 201

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM Members WHERE id = %s", (id,))
    member = cursor.fetchone()
    if member:
        return jsonify(Member().dump(member)), 200
    return jsonify({'message': 'Member not found!'}), 404

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    name = request.json.get('name')
    age = request.json.get('age')
    email = request.json.get('email')
    cursor = db_connection.cursor()
    cursor.execute("UPDATE Members SET name = %s, age = %s, email = %s WHERE id = %s", (name, age, email, id))
    db_connection.commit()
    return jsonify({'message': 'Member updated successfully!'}), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM Members WHERE id = %s", (id,))
    db_connection.commit()
    return jsonify({'message': 'Member deleted successfully!'}), 200

# Task 3: Managing Workout Sessions

@app.route('/workouts', methods=['POST'])
def add_workout():
    member_id = request.json['member_id']
    date = request.json['date']
    activity = request.json['activity']
    duration = request.json['duration']
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO WorkoutSessions (member_id, date, activity, duration) VALUES (%s, %s, %s, %s)",
                   (member_id, date, activity, duration))
    db_connection.commit()
    return jsonify({'message': 'Workout session added successfully!'}), 201

@app.route('/workouts/<int:member_id>', methods=['GET'])
def get_workouts(member_id):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM WorkoutSessions WHERE member_id = %s", (member_id,))
    workouts = cursor.fetchall()
    return jsonify([WorkoutSession().dump(workout) for workout in workouts]), 200

# Main block to run the application
if __name__ == '__main__':
    app.run(debug=True)
