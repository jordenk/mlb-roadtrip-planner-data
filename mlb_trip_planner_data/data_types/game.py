class Game:
    def __init__(self, home_team, away_team, stadium_lat_long, timestamp):
        self.home_team = home_team
        self.away_team = away_team
        self.stadium_lat_long = stadium_lat_long_map[home_team]
        self.timestamp = timestamp

stadium_lat_long_map = {}