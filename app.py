from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mikehall56!",
        database="cat_shelter"
    )
    return connection

@app.route("/")
def home():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cats")
    cats = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("home.html", cats=cats)

@app.route("/adopt/<int:cat_id>", methods=["GET", "POST"])
def adopt(cat_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM cats WHERE id = %s", (cat_id,))
    cat = cursor.fetchone()

    if request.method == "POST":
        applicant_name = request.form.get("applicant_name")
        email = request.form.get("email")
        housing_type = request.form.get("housing_type")
        other_pets = request.form.get("other_pets")
        message = request.form.get("message")

        print("FORM SUBMITTED")
        print(applicant_name, email, housing_type, other_pets, message)

        insert_cursor = connection.cursor()
        insert_cursor.execute(
            """
            INSERT INTO adoption_requests
            (cat_id, applicant_name, email, housing_type, other_pets, message)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (cat_id, applicant_name, email, housing_type, other_pets, message)
        )
        connection.commit()

        print("INSERTED INTO DATABASE")

        insert_cursor.close()
        cursor.close()
        connection.close()

        return redirect("/")

    cursor.close()
    connection.close()
    return render_template("adopt.html", cat=cat)

if __name__ == "__main__":
    app.run(debug=True)