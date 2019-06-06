class Issue:

  def __init__(
    self,  
    url,
    github_id,
    title,
    message,
    language,
    repo):
    self.url = url
    self.github_id = github_id
    self.title = title
    self.message = message
    self.language = language
    self.repo = repo
    