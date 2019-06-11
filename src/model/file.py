class File:

  def __init__(
    self,
    sha,
    url,
    name,
    extension,
    content,
    patch,
    commitId):
    self.sha = sha
    self.url = url
    self.name = name
    self.extension = extension
    self.content = content
    self.patch = patch
    self.commitId = commitId
    self.table = 'files'

