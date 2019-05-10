class Issue:

  def __init__(
    self,  
    url,
    github_id,
    label,
    state,
    title,
    body_raw,
    body_text_only,
    language,
    repo):
    self.url = url
    self.github_id = github_id
    self.label = label
    self.state = state
    self.title = title
    self.body_raw = body_raw
    self.body_text_only = body_text_only,
    self.language = language
    self.repo = repo
    