class Issue:

  def __init__(
    self,  
    url,
    github_id,
    title,
    body,
    language,
    repo):
    self.url = url
    self.github_id = github_id
    self.title = title
    self.body = body
    self.language = language
    self.repo = repo
    