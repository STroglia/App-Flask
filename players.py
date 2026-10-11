from flask import abort, make_response, request
from config import db
from models import Player, Team, player_schema, players_schema

def read_all():
    players = Player.query.all()
    return players_schema.dump(players)

def read_one(player_id):
    player = Player.query.filter(Player.id == player_id).one_or_none()
    if player is not None:
        return player_schema.dump(player)
    else:
        abort(404, f"Jugador con id {player_id} no encontrado")

def create(team_id):
    team = Team.query.filter(Team.id == team_id).one_or_none()
    if team is None:
        abort(404, f"Equipo con id {team_id} no encontrado")

    data = request.get_json()
    new_player = Player(
        name=data.get("name"),
        position=data.get("position"),
        number=data.get("number"),
        team_id=team_id
    )
    db.session.add(new_player)
    db.session.commit()
    return player_schema.dump(new_player), 201

def update(player_id):
    player = Player.query.filter(Player.id == player_id).one_or_none()
    if player is None:
        abort(404, f"Jugador con id {player_id} no encontrado")

    data = request.get_json()
    
    new_team_id = data.get("team_id")
    if new_team_id is not None and new_team_id != player.team_id:
        team_exists = Team.query.filter(Team.id == new_team_id).one_or_none()
        if team_exists is None:
            abort(404, f"El equipo destino con id {new_team_id} no existe")
        player.team_id = new_team_id

    player.name = data.get("name", player.name)
    player.position = data.get("position", player.position)
    player.number = data.get("number", player.number)

    db.session.commit()
    return player_schema.dump(player), 200

def delete(player_id):
    player = Player.query.filter(Player.id == player_id).one_or_none()
    if player is not None:
        db.session.delete(player)
        db.session.commit()
        return make_response(f"Jugador eliminado", 200)
    else:
        abort(404, f"Jugador no encontrado")