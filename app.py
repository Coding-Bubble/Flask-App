from flask import Flask, render_template, request, session, redirect, url_for
from os import urandom
from pymongo import MongoClient
from config import password


app = Flask(__name__)
app.secret_key = urandom(24)

client = MongoClient(f"mongodb+srv://flaskAdmin:{password}@cluster0.8ejth.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database('coding-bubble')
records = db.admin
resource_collection = db.resource_collection


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/admin', methods=['post', 'get'])
def admin():
    if "name" in session:
        return redirect(url_for('insert'))
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        credential = records.find_one({"name": name})
        if credential:
            correct_name = credential['name']
            correct_password = credential['password']

            if correct_password == password and correct_name == name:
                session['name'] = correct_name
                # print(session)
                return redirect(url_for('insert'))
            else:
                if "name" in session:
                    return redirect(url_for('insert'))
    return render_template("admin.html")


@app.route('/insert', methods=['post', 'get'])
def insert():
    if "name" in session:
        if request.method == "POST":
            title = request.form.get('tittle')
            category = request.form.get('category')
            description = request.form.get('description')
            url = request.form.get('url')
            resource_details = {"tittle": title, "category": category, "description": description, "url": url}
            resource_collection.insert_one(resource_details)
            return render_template('insert.html')
        return render_template('insert.html')
    return redirect(url_for('admin'))


@app.route('/resources')
def resources():
    data = resource_collection.find()
    return render_template("resources.html", data = data)


if __name__ == '__main__':
    app.run()
