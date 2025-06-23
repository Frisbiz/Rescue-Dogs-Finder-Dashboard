"""
ui_module.py
Builds the Dash UI and callbacks.
"""

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table, Input, Output, State, ctx
import dash_leaflet as dl
from dash import dcc as dash_dcc  # for Download
from db_module import AnimalShelter

shelter = AnimalShelter()


def build_layout(df: pd.DataFrame) -> html.Div:
    # second enhancement: dynamic breed dropdown
    breed_opts = sorted(set(df["breed"]))
    breed_options = [{"label": b, "value": b} for b in breed_opts]

    return html.Div(
        [
            html.Center(html.B(html.H1("SNHU CS‑340 Dashboard – Faris Malik"))),

            html.A(
                html.Img(src="assets/Grazioso Salvare Logo.png",
                         style={"height": "100px"}),
                href="https://www.snhu.edu",
                target="_blank",
            ),

            html.Hr(),

            dcc.RadioItems(
                id="rescue-filter",
                options=[
                    {"label": "Water Rescue", "value": "Water Rescue"},
                    {"label": "Mountain Rescue", "value": "Mountain Rescue"},
                    {"label": "Disaster Rescue", "value": "Disaster Rescue"},
                    {"label": "Reset", "value": "Reset"},
                ],
                labelStyle={"display": "inline-block", "marginRight": "10px"},
                style={"display": "flex", "flexWrap": "wrap",
                       "justifyContent": "flex-start"},
            ),

            # second enhancement: breed dropdown
            dcc.Dropdown(
                id="breed-select",
                options=breed_options,
                placeholder="(optional) filter by breed",
                style={"width": "300px", "marginTop": "10px"},
            ),

            html.Br(),

            dash_table.DataTable(
                id="datatable-id",
                columns=[{"name": c, "id": c} for c in df.columns],
                data=df.to_dict("records"),
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                row_selectable="single",
                selected_rows=[],
                page_action="native",
                page_size=10,
            ),

            html.Br(),

            html.Div(
                [
                    html.Div([dcc.Graph(id="pie-chart")],
                             style={"width": "48%", "display": "inline-block"}),
                    html.Div([html.Div(id="map-id")],
                             style={"width": "48%", "display": "inline-block",
                                    "paddingLeft": "20px"}),
                ],
                style={"display": "flex", "justifyContent": "space-between"},
            ),

            html.Br(),
            html.Button("Reset All", id="reset-all", n_clicks=0),

            # second enhancement: CSV export
            html.Button("Export CSV", id="export-btn", n_clicks=0,
                        style={"marginLeft": "20px"}),
            dash_dcc.Download(id="download-csv"),

            html.Hr(),
            html.Div("Unique ID: Faris Malik", style={"marginTop": "20px"}),
        ]
    )


def register_callbacks(app: Dash, _df_start: pd.DataFrame) -> None:
    # combine rescue filter + breed filter
    @app.callback(Output("datatable-id", "data"),
                  Input("rescue-filter", "value"),
                  Input("breed-select", "value"))
    def filter_data(rescue_type, breed_value):
        if rescue_type == "Water Rescue":
            query = {
                "breed": {"$in": ["Labrador Retriever Mix",
                                  "Chesapeake Bay Retriever",
                                  "Newfoundland"]},
                "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156},
                "sex_upon_outcome": {"$regex": "Intact Female"},
            }
        elif rescue_type == "Mountain Rescue":
            query = {
                "breed": {"$in": ["German Shepherd", "Alaskan Malamute",
                                  "Old English Sheepdog", "Siberian Husky",
                                  "Rottweiler"]},
                "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156},
                "sex_upon_outcome": {"$regex": "Intact Male"},
            }
        elif rescue_type == "Disaster Rescue":
            query = {
                "breed": {"$in": ["Doberman Pinscher", "German Shepherd",
                                  "Golden Retriever", "Bloodhound",
                                  "Rottweiler"]},
                "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300},
                "sex_upon_outcome": {"$regex": "Intact Male"},
            }
        else:
            query = {}

        records = shelter.read(query)
        df_temp = pd.DataFrame(records)

        # second enhancement: optional breed filter
        if breed_value:
            df_temp = df_temp[df_temp["breed"] == breed_value]

        return df_temp.to_dict("records")

    @app.callback(Output("pie-chart", "figure"),
                  Input("datatable-id", "data"))
    def update_pie_chart(data):
        if not data:
            return {}
        df_local = pd.DataFrame(data)
        return px.pie(df_local, names="breed", title="Breed Distribution")

    @app.callback(Output("map-id", "children"),
                  Input("datatable-id", "derived_virtual_data"),
                  Input("datatable-id", "derived_virtual_selected_rows"))
    def update_map(view_data, selected):
        if not view_data:
            return [html.P("No data available.")]
        dff = pd.DataFrame(view_data)
        row = selected[0] if selected else 0
        center_lat, center_lon = 30.75, -97.48
        if row < len(dff) and \
           "location_lat" in dff.columns and "location_long" in dff.columns:
            center_lat = dff.at[row, "location_lat"]
            center_lon = dff.at[row, "location_long"]
        breed = dff.at[row, "breed"] if "breed" in dff.columns else "Unknown"
        name = dff.at[row, "name"] if "name" in dff.columns else "Unknown"
        return [
            dl.Map(
                style={"width": "100%", "height": "500px"},
                center=[center_lat, center_lon],
                zoom=10,
                children=[
                    dl.TileLayer(id="base-layer"),
                    dl.Marker(
                        position=[center_lat, center_lon],
                        children=[
                            dl.Tooltip(breed),
                            dl.Popup([html.H1("Animal Name"), html.P(name)]),
                        ],
                    ),
                ],
            )
        ]

    @app.callback(Output("rescue-filter", "value"),
                  Output("breed-select", "value"),
                  Output("datatable-id", "selected_rows"),
                  Input("reset-all", "n_clicks"),
                  prevent_initial_call=True)
    def reset_all(_clicks):
        return "Reset", None, []

    # second enhancement: CSV export callback
    @app.callback(Output("download-csv", "data"),
                  Input("export-btn", "n_clicks"),
                  State("datatable-id", "data"),
                  prevent_initial_call=True)
    def export_csv(_clicks, table_data):
        df_export = pd.DataFrame(table_data)
        return dash_dcc.send_data_frame(df_export.to_csv,
                                        "filtered_animals.csv",
                                        index=False)
