
class Note(object):

    def __init__(self, id_note, title, body, author, timestamp):
        self.id_note = id_note
        self.title = title
        self.body = body
        self.author = author
        self.timestamp = timestamp

    def get_id_note(self):
        return self.id_note

    def get_title(self):
        return self.title

    def get_body(self):
        return self.body

    def get_author(self):
        return self.author

    def get_timestamp(self):
        return self.timestamp