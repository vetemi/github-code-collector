class Commit:

  def __init__(
    self,
    url,
    github_id,
    body,
    language,
    issue):
    self.url = url
    self.github_id = github_id
    self.body = body
    self.language = language
    self.issue = issue
