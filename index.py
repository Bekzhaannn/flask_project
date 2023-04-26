from flask import Flask, render_template, request, redirect
from data import data
import datetime
import os

app = Flask(__name__)

def get_data():
    with open('data.py', 'r', encoding="utf-8") as f:
        data = f.read()
    return data

def write_data(data):
    with open('data.py', 'w', encoding="utf-8") as f:
        f.write(data)

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/admin')
def admin():
    return render_template('admin.html', data=data)

@app.route('/add_card', methods=['POST'])
def add_card():
    card = {}
    card['id'] = str(datetime.datetime.now())[-6:-1]
    card['name'] = request.form['name']
    card['age'] = request.form['age']
    card['overall_rating'] = request.form['overall_rating']
    card['height'] = request.form['height']
    image = request.files['image']
    filename = f"{card['id']}.jpg"
    file_path = os.path.join("static", "photo", filename).replace("\\", "/")
    image.save(file_path)

    data.append(card)
    write_data(f"data = {data}")
    return redirect('/admin')

@app.route('/delete_card', methods=['POST'])
def delete_card():
    id = request.form['id']
    for card in data:
        print(str(id))
        if str(card['id']) == str(id):
            data.remove(card)
    return redirect('/admin')

#игра - на отдельном роуте

@app.route('/game')
def game():
    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)
