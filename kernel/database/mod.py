import pymongo
from config import data

cfg = data['database']

# src = (f"{cfg['protocol']}://{cfg['user']}:{cfg['password']}@{cfg['host']}/?retryWrites=true&w=majority"
#        f"&appName=Aurora-Echo")

src = "mongodb://127.0.0.1:27017/?retryWrites=true&w=majority&appName=Aurora-Echo"


client = pymongo.MongoClient(src)
db = client['aurora-echo']
