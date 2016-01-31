from app import app, db
from app.models import Match, MatchPlayer, Player
from config import debug, port, host

def initialize():
    db.connect()
    db.create_tables([Match, MatchPlayer, Player], safe=True)
    db.close()

if __name__ == '__main__':
    initialize()
    app.run(debug=debug, port=port, host=host)
