from flask import abort, make_response, request
from config import db
from models import Team, teams_schema, team_schema

def read_all():
    teams = Team.query.order_by(Team.name).all()
    return teams_schema.dump(teams)

def read_one(name):
    team = Team.query.filter(db.func.lower(Team.name) == name.lower()).one_or_none()
    if team is not None:
        return team_schema.dump(team)
    else:
        abort(404, f"Equipo '{name}' no encontrado")

def create():
    data = request.get_json()
    name = data.get("name")
    existing_team = Team.query.filter(db.func.lower(Team.name) == name.lower()).one_or_none()

    if existing_team is None:
        new_team = Team(name=name, city=data.get("city"))
        db.session.add(new_team)
        db.session.commit()
        return team_schema.dump(new_team), 201
    else:
        abort(409, f"El equipo '{name}' ya existe")

def delete(name):
    team = Team.query.filter(db.func.lower(Team.name) == name.lower()).one_or_none()
    if team is not None:
        db.session.delete(team)
        db.session.commit()
        return make_response(f"Equipo '{name}' eliminado", 200)
    else:
        abort(404, f"Equipo '{name}' no encontrado")