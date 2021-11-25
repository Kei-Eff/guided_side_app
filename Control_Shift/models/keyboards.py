from main import db

ownerships = db.Table(
    'ownerships',
    db.Column('user_id', db.Integer, db.ForeignKey('flasklogin-users.id'), primary_key=True),
    db.Column('keyboard_id', db.Integer, db.ForeignKey('keyboards.keyboard_id'), primary_key=True)
)


class Keyboard(db.Model):
    __tablename__ = "keyboards"
    keyboard_id = db.Column(db.Integer, primary_key=True)
    keyboard_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), default="No Description Provided")
    cost = db.Column(db.Integer, nullable=False, server_default="0")

    creator_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'))

    def __init__(self, keyboard_name):
        self.keyboard_name = keyboard_name

    owners = db.relationship(
        'User',
        secondary=ownerships,
        backref=db.backref('owned_keyboards')
    )

    @property
    def image_filename(self):
        return f"keyboard_images/{self.keyboard_id}.png"