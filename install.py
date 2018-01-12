import rethinkdb as r

from models.Profile import Profile
from tools.SettingsManager import SettingsManager

settings = SettingsManager().loadSettings()

print("----------")
print("Installing DB")
r.db_create(settings['db']['name']).run(r.connect(settings['db']['host'], settings['db']['port']))
print("The DB " + settings['db']['name'] + " now exists.")
print("----------")
print("\n")
print("----------")
print("Installing Profile")
profile = Profile()
profile.createTable()
print("The table now exists")
print("----------")
