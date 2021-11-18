from main import db

class Keyboard(db.Model):
    __tablename__ = "keyboards"
    keyboard_id = db.Column(db.Integer, primary_key=True)
    keyboard_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), default="No Description Provded")
    cost = db.Column(db.Integer, nullable=False, server_default="0")

    def __init__(self, keyboard_name):
        self.keyboard_name = keyboard_name

    @property
    def serialize(self):
        return {
            "keyboard_id": self.keyboard_id,
            "keyboard_name": self.keyboard_name
        }