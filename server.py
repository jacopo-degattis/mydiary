import secrets
import hashlib
from libs.MySQLHandler import MySQLHandler
from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)
handler = MySQLHandler()

app.secret_key = secrets.token_bytes()

@app.route('/')
def homepage():
    #notes = handler.get_all_notes()
    # return render_template('index.html', value=notes[::-1])
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('logged')
    session.pop('curr_id')
    return redirect('/')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/notesList', methods=['GET'])
def notesList():
    #notes = handler.get_all_notes() # Visualizzare solo le note associate all'utente
    notes = handler.get_notes_by_user_id(session['curr_id'])
    return render_template('notesList.html', value=notes[::-1])

@app.route('/api/newUser', methods=['POST'])
def newUser():
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()

        handler.addUser(first_name, last_name, email, username, password)
        data = {'response': 'success', 'status_code': 200}
        return redirect('/login')
    except Exception as e:
        print(e)
        data = {'response': 'error', 'status_code': 400}
        return redirect('/signup') # Aggiungere segnalazione dell'errore all'utente se possibile

    # Caso che non si dovrebbe mai verificare
    return redirect('/')

@app.route('/api/login', methods=['POST'])
def userLogin():
    try:
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()

        login = handler.checkLogin(username, password)
        if login:
            session['logged'] = True 
            session['curr_id'] = login
            session['curr_username'] = username
            return redirect('/') # Aggiungere login corretto con la sessione
        else:
            session['logged'] = False
            print('Login errato')
    except Exception as e:
        print(e)
        return redirect('/login')

    return ''


@app.route('/api/addNote', methods=['POST'])
def addNote():
    try:
        note_title = request.form['title']
        note_body = request.form['body']
        handler.addNote(note_title, note_body, session['curr_id'])
        data = {'response': 'success', 'status_code': 200}
    except Exception as e:
        print(e)
        data = {'response': 'error', 'status_code': 400}

    # return jsonify(data) 
    # return redirect('/')
    return render_template('index.html', value=data['status_code'])

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