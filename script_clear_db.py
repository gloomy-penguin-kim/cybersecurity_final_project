import sqlite3

 
base_path = sys.argv[1] 
database = os.path.join(base_path, "database.db") 

if not os.path.exists(os.path.join(base_path, "database.db")):
    print("Database does not exist in " + base_path)
    sys.exit(1)
 

sqliteConnection = sqlite3.connect(database)
cursor = sqliteConnection.cursor()

cursor.execute("delete from attacks_option", {})
cursor.execute("delete from attacks_option_heading", {})
cursor.execute("delete from attacks_attack", {})
cursor.execute("delete from attacks_option", {})
cursor.execute("delete from attacks_target", {})
sqliteConnection.commit()