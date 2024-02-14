import oracledb
from dotenv import load_dotenv
import os

load_dotenv()

oracledb.init_oracle_client()
connection = oracledb.connect(  user=os.getenv("DB_USER"), 
                                password=os.getenv("DB_PASSWORD"), 
                                dsn=os.getenv("DB_DSN") )
cursor  = connection.cursor()

print("Database version: " + connection.version)
        
cursor.close()