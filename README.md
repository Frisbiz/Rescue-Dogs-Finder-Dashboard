# 🐾 CS‑340 Animal Rescue Dashboard

This project is a web-based dashboard for an animal rescue organization, originally developed for the SNHU CS‑340 Advanced Programming Concepts course and enhanced as part of the CS 499 Capstone. It allows users to explore animal shelter data using interactive filters, maps, and visualizations. The application is built using **Python**, **Dash**, **MongoDB**, and **Plotly**.

---

## 📌 Features

- Filter animals by rescue type (Water, Mountain, Disaster)
- Optional breed dropdown filter
- Interactive data table with sorting and filtering
- Pie chart of breed distribution
- Location map using `dash-leaflet`
- CSV export of filtered table data
- Reset All button for easy clearing of filters
- Modular code structure for UI, DB, and App logic

---

## 📂 Project Structure

```bash
.
├── main.py                # Launches the dashboard
├── db_module.py          # MongoDB access layer
├── ui_module.py          # Layout and callbacks
├── assets/
│   └── Grazioso Salvare Logo.png
│   └── aac_shelter_outcomes.csv   # Required dataset
└── README.md             # This file
