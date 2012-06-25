import os

activate_this = '/var/www/sambandid/env/sambandid/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))


import sys
sys.path.insert(0, '/var/www/sambandid/repo/')

from sambandid import app as application