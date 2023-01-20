from flask import Flask, render_template, request, url_for, redirect
import sqlite3
from random import randint

app = Flask(__name__)


@app.route('/')
def index():
    
    con = sqlite3.connect('names.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM People')
    persons = cur.fetchall()
    con.close()
    return render_template('index.html', persons=persons)


@app.route('/submit_name', methods=['POST', 'GET'])
def submit_name():

    try:
        con = sqlite3.connect('names.db')
        cur = con.cursor()
        name = request.form.get("name")
        age = request.form.get("age")

        id = randint(0, 9999999999999)
        try: 
            cur.execute('INSERT INTO People VALUES (?, ?, ?)', (name, age, id))
            con.commit()
            con.close()
            return redirect('/')

        except:
            return redirect('/')

    except:
        return render_template('failure.html')

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete_person(id):

    try:
        con = sqlite3.connect('names.db')
        cur = con.cursor()
        cur.execute('DELETE FROM People WHERE id = ?', (id,))
        con.commit()
        con.close()
        return redirect('/')

    except:
        return "Error deleting person brah"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update_person(id):


    if request.method == 'POST':

        new_name = request.form.get("name")
        new_age = request.form.get("age")

        try:
            con = sqlite3.connect('names.db')
            cur = con.cursor()
            cur.execute('UPDATE People SET Name = ? WHERE id = ?', (new_name, id))
            cur.execute('UPDATE People SET Age = ? WHERE id = ?', (new_age, id))

            con.commit()
            con.close()
            return redirect('/')
        
        except:
            return "Error updating peerson bruh"

    else:
        con = sqlite3.connect('names.db')
        cur = con.cursor()
        cur.execute('SELECT * FROM People WHERE id = ?', (id,))
        person = cur.fetchall()
        con.close()
        return render_template('update.html', id=id, old_name=person[0][0], old_age=person[0][1])


if __name__ == '__main__':
    app.run(debug=True)