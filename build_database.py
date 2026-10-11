import os
from config import app, db
from models import Team, Player

if os.path.exists("football.db"):
    os.remove("football.db")

with app.app_context():
    db.create_all()

    teams_data = [
        {
            "name": "Boca Juniors",
            "city": "Buenos Aires",
            "players": [
                {"name": "Edinson Cavani", "position": "Delantero", "number": 10},
                {"name": "Kevin Zenón", "position": "Mediocampista", "number": 22},
            ],
        },
        {
            "name": "River Plate",
            "city": "Buenos Aires",
            "players": [
                {"name": "Franco Armani", "position": "Arquero", "number": 1},
                {"name": "Miguel Borja", "position": "Delantero", "number": 9},
            ],
        },
    ]

    for t_data in teams_data:
        team = Team(name=t_data["name"], city=t_data["city"])
        for p_data in t_data["players"]:
            team.players.append(
                Player(name=p_data["name"], position=p_data["position"], number=p_data["number"])
            )
        db.session.add(team)

    db.session.commit()

print("¡Base de datos de fútbol creada con éxito!")