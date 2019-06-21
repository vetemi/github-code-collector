class File:

  def __init__(
    self,
    github_id,
    url,
    name,
    extension,
    content,
    hash,
    commitId):
    self.github_id = github_id
    self.url = url
    self.name = name
    self.extension = extension
    self.content = content
    self.hash = hash
    self.commitId = commitId
    self.table = 'files'

