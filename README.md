CS‑340 Animal Rescue Dashboard – Setup Guide
1. Prerequisites
• Docker Desktop installed and running
• Python 3.9 or newer
• aac_shelter_outcomes.csv (included)
2. Start MongoDB Container
Run in PowerShell:
docker run -d --name mongo_local -p 27018:27017 mongo:6
3. Import the Dataset
docker cp aac_shelter_outcomes.csv mongo_local:/aac.csv
docker exec mongo_local mongoimport --db AAC --collection animals --drop --type csv --file /aac.csv --headerline
4. Install Python Packages
pip install dash==2.15.0 dash-leaflet pandas plotly pymongo
5. Run the Dashboard
python main.py
Open http://127.0.0.1:8050
Notes
- The app reads data only (no writes).
- Mongo URI is hard‑coded to localhost:27018 in db_module.py.
- Change the port mapping and URI if 27018 is unavailable.
