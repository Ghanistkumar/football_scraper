from pymongo import MongoClient
from football_scraper.config.config import database

# Connect to MongoDB Database
client = MongoClient(
    host=database.host,
    port=database.port,
)
db = client[database.name]

# Database Tables
LeagueTable = db.football_league