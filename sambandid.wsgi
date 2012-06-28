import os
import sys

os.environ['mode'] = 'production'

sys.path.insert(0, '/var/www/sambandid/repo/')

activate_this = '/var/www/sambandid/env/sambandid/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from sambandid import app as application
