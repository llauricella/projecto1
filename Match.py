class Match:
    def __init__(self, id, number, home_team_id, home_team_name, home_team_code,
                 away_team_id, away_team_name, away_team_code, date, group):
        self.id = id
        self.number = number
        self.home_team_id = home_team_id
        self.home_team_name = home_team_name
        self.home_team_code = home_team_code
        self.away_team_id = away_team_id
        self.away_team_name = away_team_name
        self.away_team_code = away_team_code
        self.date = date
        self.group = group

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number,
            "home_team_id": self.home_team_id,
            "home_team_name": self.home_team_name,
            "home_team_code": self.home_team_code,
            "away_team_id": self.away_team_id,
            "away_team_name": self.away_team_name,
            "away_team_code": self.away_team_code,
            "date": self.date,
            "group": self.group
        }