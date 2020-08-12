from libs.MySQLHandler import MySQLHandler
from flask import Flask, render_template, jsonify, request, redirect

app = Flask(__name__)
handler = MySQLHandler()

@app.route('/')
def homepage():
    notes = handler.get_all_notes()
    return render_template('index.html', value=notes)

@app.route('/api/addNote', methods=['POST'])
def addNote():
    try:
        note_title = request.form['title']
        note_body = request.form['body']
        handler.addNote(note_title, note_body)
        data = {'response': 'success', 'status_code': 200}
    except Exception as e:
        print(e)
        data = {'response': 'error', 'status_code': 400}

    #return jsonify(data) 
    return redirect('/')

@app.route('/api/remove/<id_note>', methods=['GET'])
def removeNote(id_note):
    try:
        handler.removeNote(id_note)
        data = {'response': 'success', 'status_code': 200}
    except Exception as e:
        print(e)
        data = {'response': 'error', 'status_code': 400}

    #return jsonify(data) 
    return redirect('/')

app.run('0.0.0.0', debug=True)