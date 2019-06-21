from tensorflow.keras.models import load_model
from keras.backend import clear_session
import tensorflow
import dill

clear_session()

class BugDetector:

  def __init__(self, configService):

    with open(configService.config['issuedetection']['title-preprocessor'], 'rb') as f:
      self.titlePreproc = dill.load(f)

    with open(configService.config['issuedetection']['body-preprocessor'], 'rb') as f:
      self.bodyPreproc = dill.load(f)
    
    self.threshold = float(configService.config['issuedetection']['threshold'])

  def isBug(self, issue):
    if not issue['body'] or not issue['title']:
      return False   

      self.model = load_model(configService.config['issuedetection']['model'])
      self.vecTitle = self.titlePreproc.transform([issue['title']])
      self.vecBody = self.bodyPreproc.transform([issue['body']])
      probs = self.model.predict(x=[self.vecBody, self.vecTitle]).tolist()[0]
      return probs[0] >= self.threshold

