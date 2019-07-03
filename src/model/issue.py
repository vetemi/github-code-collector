class Issue:

  def __init__(
    self,  
    url,
    github_id,
    title,
    body,
    labeled,
    language,
    repoId):
    self.url = url
    self.github_id = github_id
    self.title = title
    self.body = body
    self.labeled = labeled
    self.language = language
    self.repoId = repoId
    self.table = 'issues'
