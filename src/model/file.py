class File:

  def __init__(
    self,
    sha,
    url,
    name,
    extension,
    content
    patch,
    commit):
    self.sha = sha
    self.url = url
    self.name = name
    self.extension = extension
    self.content = content
    self.patch = patch
    self.commit = commit

