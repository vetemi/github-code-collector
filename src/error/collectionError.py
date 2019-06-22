class CollectionError(Exception):

  def __init__(self, message, error, event, archiveDate):
    super().__init__(message)

    self.error = error
    self.event = event
    self.archiveDate = archiveDate
