import os
from dotenv import load_dotenv
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 3


class DefaultConfig(Config):
    MAIN_PAGE='main.consent'
    SKIP_VALID=False
    EXPLAIN_TYPE=None
    PROLIFIC_STUDY_ID='687f5e181bae365fd931e999' # test
    PROLIFIC_COMPLETION_CODE='C10EXTDI' #test
    #PROLIFIC_STUDY_ID='687a244efed49cdf9e6592ff' # Final study ID
    #PROLIFIC_COMPLETION_CODE='CRQYIPFI'# Final completion code

class DebugConfig(Config):
    MAIN_PAGE='main.consent'
    SKIP_VALID=True
    EXPLAIN_TYPE=None
    #EXPLAIN_TYPE='explain_interactive'
    # choose amongts 'explain_baseline', 'explain_visual',
    # 'explain_textual', 'explain_quantitative', 'explain_interactive', 'explain_contextual'
    PROLIFIC_STUDY_ID='687f5e181bae365fd931e999' # test
    PROLIFIC_COMPLETION_CODE='C10EXTDI' #test
    #PROLIFIC_STUDY_ID='687a244efed49cdf9e6592ff' # Final study ID
    #PROLIFIC_COMPLETION_CODE='CRQYIPFI'# Final completion code

configs = {
  'default'  : DefaultConfig,
  'debug'  : DebugConfig,
}
