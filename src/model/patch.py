class Patch:

  def __init__(
    self,
    content,
    fileId):
    self.content = content
    self.fileId = fileId
    self.table = 'patches'
