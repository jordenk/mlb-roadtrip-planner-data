class Team:
  def __init__(self, urlName):
    self.urlName = urlName
    self.url = f"https://www.mlb.com/{urlName}/fans/downloadable-schedule"
