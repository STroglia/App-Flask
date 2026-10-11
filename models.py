from datetime import datetime
from config import db, ma

class Player(db.Model):
    __tablename__ = "player"
    
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(30))
    number = db.Column(db.Integer)

class Team(db.Model):
    __tablename__ = "team"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    city = db.Column(db.String(50))
    
    players = db.relationship(
        "Player",
        cascade="all, delete, delete-orphan",
        backref="team",
    )

class PlayerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Player
        load_instance = True
        sqla_session = db.session
        include_fk = True

class TeamSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Team
        load_instance = True
        sqla_session = db.session
        
    players = ma.Nested(PlayerSchema, many=True)

team_schema = TeamSchema()
teams_schema = TeamSchema(many=True)
player_schema = PlayerSchema()
players_schema = PlayerSchema(many=True)