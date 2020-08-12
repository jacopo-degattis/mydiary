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

    def get_all_notes(self):
        query = 'SELECT * FROM Note'
        status = self.execute(query)
        notes_list = []
        if self.results:
            for note in self.results:
                notes_list.append(
                    Note(note[0], note[1], note[2], note[3])
                )
        return notes_list

    def removeNote(self, id_note):
        query = f'DELETE FROM Note WHERE id_note={id_note}'
        return self.execute(query)

    def addNote(self, title, body):
        # AGGIUNGERE POI UTENTI, QUINDI AGGIUNGERE NEL DB ID_UTENTE --> CHIAVE ESTERNA
        query = f'INSERT INTO Note (title, body) VALUES ("{title}", "{body}")'
        return self.execute(query)


