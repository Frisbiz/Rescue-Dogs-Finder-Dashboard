# 🐾 Animal Rescue Dashboard
This project is a web-based dashboard for an animal rescue organization, originally developed for the SNHU CS‑340 Advanced Programming Concepts course and enhanced as part of the CS 499 Capstone. It allows users to explore animal shelter data using interactive filters, maps, and visualizations. The application is built using Python, Dash, MongoDB, and Plotly.
## 📌 Features
- Filter animals by rescue type (Water, Mountain, Disaster)
- Optional breed dropdown filter
- Interactive data table with sorting and filtering
- Pie chart of breed distribution
- Location map using `dash-leaflet`
- CSV export of filtered table data
- Reset All button for easy clearing of filters
- Modular code structure for UI, DB, and App logic
## 📂 Project Structure
```
.
├── main.py                # Launches the dashboard
├── db_module.py          # MongoDB access layer
├── ui_module.py          # Layout and callbacks
├── assets/
│   └── Grazioso Salvare Logo.png
│   └── aac_shelter_outcomes.csv   # Required dataset
└── README.md             # This file
```
## 🧰 Prerequisites
- ✅ Docker Desktop installed and running
- ✅ Python 3.9 or newer
- ✅ pip (Python package installer)
## ⚙️ Setup Guide
### 1. Clone the Repo
```bash
git clone https://github.com/Frisbiz/animal-rescue-dashboard.git
cd animal-rescue-dashboard
```
### 2. Start MongoDB in Docker
```bash
docker run -d --name mongo_local -p 27018:27017 mongo:6
```
### 3. Import the Dataset
```bash
docker cp assets/aac_shelter_outcomes.csv mongo_local:/aac.csv
docker exec mongo_local mongoimport --db AAC --collection animals --drop --type csv --file /aac.csv --headerline
```
### 4. Install Python Packages
```bash
pip install dash==2.15.0 dash-leaflet pandas plotly pymongo
```
### 5. Run the Application
```bash
python main.py
```
> ⚠️ Make sure the file path to `aac_shelter_outcomes.csv` is correct and the container is running.
## 🔒 Notes
- The app only reads from MongoDB. No documents are modified or written.
- The MongoDB URI is hardcoded to `localhost:27018` in `db_module.py`.
- If port 27018 is unavailable, change the port mapping in Docker and update the URI accordingly.
- Tested on Windows with PowerShell. On Mac/Linux, commands may require adjustment.
## 🧠 Technologies Used
- **Dash 2.15.0 – Web framework for Python**
- **dash-leaflet – Interactive map integration**
- **MongoDB – NoSQL database used with Docker**
- **Pandas & Plotly – Data manipulation and visualizations**
- **Docker – Local containerized database environment**
## 📈 Enhancement Summary
- Software Design – Modular structure with separate files for UI, DB, and main logic, plus a Reset All button.
- Algorithms and Data Structures – Dynamic breed filter populated from unique values in the database.
- Database Handling – CSV export, environment-driven connection config, and startup checks for MongoDB.
## 🤝 Contributing
This project was built as a capstone artifact. For future improvements or suggestions:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request
## 🧑‍💻 Author
**Faris Malik**
GitHub: [@Frisbiz](https://github.com/Frisbiz)
