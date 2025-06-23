"""
main.py
Run the CS‑340 Animal Rescue Dashboard.

Start with:
    python main.py
"""

import pandas as pd
from dash import Dash

from db_module import AnimalShelter
import ui_module


def launch_app(debug: bool = True) -> None:
    shelter = AnimalShelter()
    df_initial = pd.DataFrame.from_records(shelter.read())

    app = Dash(__name__)
    app.layout = ui_module.build_layout(df_initial)
    ui_module.register_callbacks(app, df_initial)

    app.run(debug=debug, host="127.0.0.1", port=8050)


if __name__ == "__main__":
    launch_app()