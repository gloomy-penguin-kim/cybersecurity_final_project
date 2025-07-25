For a Cybersecurity Bootcamp Project. For educational purposes only.

![alt text](https://github.com/gloomy-penguin-kim/cybersecurity_final_project/blob/master/metasploit%201.png) "Metasploit 1 screenshot")
 
![alt text](https://github.com/gloomy-penguin-kim/cybersecurity_final_project/blob/master/metasploit%202.png) "Metasploit 2 screenshot")
 
![alt text](https://github.com/gloomy-penguin-kim/cybersecurity_final_project/blob/master/metasploit.png) "Metasploit 3 screenshot")
 
![alt text](https://github.com/gloomy-penguin-kim/cybersecurity_final_project/blob/master/metasploit%204.png) "Metasploit 4 screenshot")


How to run: 
- download the project
- works with Metasploit v6.4.55-dev-
   - I'll tell you why, if you look at the info for an expoloit, the default taget has the value of => to its side.  this does not exist in all versions.  Please updae script_sqlite3.py to change that.
- sqlite3 database-exploit-schema.db < database-exploit-schema.sql  (this has some of my old django tables in it that I do not use in the code, will edit, only attacks_tables are used) 
- the column "session_required" requires a database query which I will post at a later time or upon request 
- (pip install here for python)
- source .venv/bin/activate
- to build and parse out the database from msfconsole.  I would post the db somewhere but it is too large for github.  Ask me and we can figure something out if this doesn't work out for you. The database can literally run all night.  Turn off the STDOUT to make it faster.  I just let it run and parse, though.  The database IS NORMALIZED.  It just has a lot of things.  
   - python3 script_payloads.py - look at file for arguments, all may not be in use, I can clean this up later 
   - python3 script_sqlite3.py  - look at file for arguments, all may not be in use, I can clean this up later
- python3 main.py for the fastapi to run. should be found at 0.0.0.0:8084/app

- to mess with the React front end see my other repo at: https://github.com/gloomy-penguin-kim/cybersecurity_final_frontend but the built dist files are in the /app folder to use as-is 
