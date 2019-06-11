class Commit:

  def __init__(
    self,
    url,
    github_id,
    message,
    language,
    issueId):
    self.url = url
    self.github_id = github_id
    self.message = message
    self.language = language
    self.issueId = issueId
    self.table = 'commits'
