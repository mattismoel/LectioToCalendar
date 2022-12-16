# Getting into the main folder.
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.lectio import Lectio

lec = Lectio(lectioUsername, lectioPassword, schoolId)

print(lec.getSchools())