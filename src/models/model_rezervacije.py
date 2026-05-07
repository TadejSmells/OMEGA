import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import db
from datetime import date
from models.models import Rezervacija, Stranka, Frizer, Salon, Storitev