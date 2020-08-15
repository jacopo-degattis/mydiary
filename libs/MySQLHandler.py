import mysql.connector
from libs.config import config
from libs.Note import Note

class MySQLHandler(object):

    def __init__(self):
        self.host = config['host']
        self.user = config['user']
        self.password = config['password']
        self.database = config['database']
        self.results = None

        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            #buffered=True
        )

    def execute(self, query):
        msg = False
        try:
            cursor = self.db.cursor()
            cursor.execute(query)
            if 'SELECT' in query:
                results = cursor.fetchall()
                if results:
                    self.results = results
                else:
                    self.results = None
            if 'INSERT' in query or 'DELETE' in query:
                self.db.commit()
            msg = True
        except Exception as e:
            print(e)
            msg = False
        return msg

    def get_id_from_username(self, username):
        query = f'SELECT id_utente FROM User WHERE username="{username}"'
        self.execute(query)
        return self.results[0][0]

    def checkLogin(self, username, password):
        success = None
        query = f'SELECT * FROM User WHERE username="{username}" AND password="{password}"'
        self.execute(query)
        if self.results:
            success = self.get_id_from_username(username)
        else:
            success = None
        return success

    def addUser(self, first_name, last_name, email, username, password):
        query = f'''INSERT INTO User (first_name, last_name, email, username, password)
                    VALUES ("{first_name}","{last_name}","{email}","{username}","{password}")'''
        return self.execute(query)

    def get_username_from_id(self, id_utente):
        query = f'SELECT username FROM User WHERE id_utente={id_utente}'
        self.execute(query)
        return self.results[0][0]

    def get_notes_by_user_id(self, user_id):
        user_note_owner = self.get_username_from_id(user_id)
        query = f'SELECT * FROM Note WHERE id_utente={user_id}'
        self.execute(query)
        notes_list = []
        if self.results:
            for note in self.results:
                notes_list.append(
                    Note(note[0], note[1], note[2], user_note_owner, note[3], note[5])
                )
        return notes_list

    def get_all_notes(self):
        query = 'SELECT * FROM Note'
        status = self.execute(query)
        notes_list = []
        print(self.results)
        if self.results:
            for note in self.results:
                curr_note_user = self.get_username_from_id(note[4])
                notes_list.append(
                    Note(note[0], note[1], note[2], curr_note_user, note[3], note[5])
                )
        return notes_list

    def removeNote(self, id_note):
        query = f'DELETE FROM Note WHERE id_note={id_note}'
        return self.execute(query)

    def addNote(self, title, body, id_utente):
        # AGGIUNGERE POI UTENTI, QUINDI AGGIUNGERE NEL DB ID_UTENTE --> CHIAVE ESTERNA
        query = f'INSERT INTO Note (title, body, id_utente) VALUES ("{title}", "{body}", {id_utente})'
        return self.execute(query)


