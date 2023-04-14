from flask import Flask, render_template, request, redirect
from data import data
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/admin')
def admin():
    return render_template('admin.html', data=data)

@app.route('/add_card', methods=['POST'])
def add_card():
    card = {}
    card['id'] = datetime.datetime.now()
    card['name'] = request.form['name']
    card['age'] = request.form['age']
    card['overall_rating'] = request.form['overall_rating']
    card['height'] = request.form['height']
    data.append(card)
    return redirect('/')

@app.route('/delete_card', methods=['POST'])
def delete_card():
    id = request.form['id']
    for card in data:
        print(str(id))
        if str(card['id']) == str(id):
            data.remove(card)
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)