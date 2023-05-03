from flask import Flask, render_template, request, redirect
from data import data
from commands import red, blue
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

@app.route('/join_button', methods=['POST'])
def join_button():
    id = request.form['id']
    for card in data:
        if str(card['id']) == str(id):
            if request.form['command'] == 'Blue':
                flag = False
                for blue_item in blue:
                    if str(blue_item['id']) == str(id):
                        blue.remove(blue_item)
                for red_item in red:
                    print(red_item)
                    if str(red_item['id']) == str(id):
                        red.remove(red_item)
                        flag = True
                if len(red) == 0 or len(blue) == 0 and flag:
                    blue.append(card)
            elif request.form['command'] == 'Red':
                flag = False
                for red_item in red:
                    if str(red_item['id']) == str(id):
                        red.remove(red_item)
                for blue_item in blue:
                    if str(blue_item['id']) == str(id):
                        blue.remove(blue_item)
                        flag = True
                if len(blue) == 0 or len(red) == 0 and flag:
                    red.append(card)

    print(red)
    print(blue)
    return redirect('/')

@app.route('/game')
def game():
    return render_template('game.html', red=red, blue=blue)

if __name__ == '__main__':
    app.run(debug=True)
