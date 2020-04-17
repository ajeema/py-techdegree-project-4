from playhouse.sqlite_ext import *
# Database file/configuration

DATABASE = 'inventory.db'
db = SqliteExtDatabase(DATABASE, pragmas={'journal_mode': 'wal'})

# source product file
SOURCE = 'inventory.csv'

# Backup files
BACKUP_DB = 'backups/backup.db'
BACKUP_JSON = 'backups/backup.json'
CSV_NAME = 'backups/backup.csv'








