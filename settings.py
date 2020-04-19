from playhouse.sqlite_ext import *
import pandas as pd
# Database file/configuration

DATABASE = 'inventory.db'
db = SqliteDatabase(DATABASE)

df = pd.read_sql("SELECT * FROM Product;", db)
# source product file
SOURCE = 'inventory.csv'

# Backup files

BACKUP_JSON = df.to_json('backups/backup.json', orient='records', lines=True)
BACKUP_CSV = df.to_csv('backups/backup.csv', sep='\t', index=False)
BACKUP_DB = df.to_sql('backups/backup.db', db, index_label=False, if_exists='replace')
#BACKUP_ALL = BACKUP_JSON BACKUP_CSV










