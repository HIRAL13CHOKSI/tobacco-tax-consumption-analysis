import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table
import ruptures as rpt
from statsmodels.nonparametric.smoothers_lowess import lowess
from sklearn.cluster import KMeans

# ============================================================
# LOAD DATA
# ============================================================
import argparse
from pathlib import Path
from tobacco_data import load_data


def create_app(data_path):
    df = load_data(data_path)

    # Region mapping
    region_map = {
        "WA":"West","OR":"West","CA":"West","NV":"West","ID":"West","MT":"West",
        "WY":"West","UT":"West","CO":"West","AZ":"West","NM":"West","AK":"West","HI":"West",
        "ND":"Midwest","SD":"Midwest","NE":"Midwest","KS":"Midwest","MN":"Midwest",
        "IA":"Midwest","MO":"Midwest","WI":"Midwest","IL":"Midwest","IN":"Midwest","MI":"Midwest","OH":"Midwest",
        "OK":"South","TX":"South","AR":"South","LA":"South","KY":"South","TN":"South",
        "MS":"South","AL":"South","GA":"South","FL":"South","SC":"South","NC":"South",
        "VA":"South","WV":"South","MD":"South","DE":"South",
        "PA":"Northeast","NY":"Northeast","NJ":"Northeast","CT":"Northeast","RI":"Northeast",
        "MA":"Northeast","VT":"Northeast","NH":"Northeast","ME":"Northeast",
        "DC":"South"
    }
    df["Region"] = df["state"].map(region_map).fillna("Other")

    years = sorted(df["Year"].unique())
    states = sorted(df["state"].unique())

    # ============================================================
    # LOESS + CHANGEPOINT
    # ============================================================
    def loess_smooth(x, y, frac=0.25):
        sm = lowess(y, x, frac=frac)
        return sm[:,0], sm[:,1]

    def changepoints(series, n=3):
        model = rpt.Binseg(model="rbf").fit(series)
        pts = model.predict(n_bkps=n)
        return pts[:-1]

    national = df.groupby("Year", as_index=False)["Y"].mean()
    cp_idx = changepoints(national["Y"].values, n=3)

    # ============================================================
    # K-MEANS CLUSTERING
    # ============================================================
    cluster_data = df.groupby("state").agg({
        "state_tax_pct":"mean",
        "Y":"mean"
    }).reset_index()

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    cluster_data["cluster"] = kmeans.fit_predict(cluster_data[["state_tax_pct","Y"]]).astype(str)

    df = df.merge(cluster_data[["state","cluster"]], on="state")

    cluster_colors = {
        "0":"#00b4ff",
        "1":"#ff6bcb",
        "2":"#ffae00",
        "3":"#2ed573"
    }

    # ============================================================
    # CORRELATION MATRIX
    # ============================================================
    corr_cols = ["Y",
                 "state_tax_pct","federal_tax_pct","total_tax_pct",
                 "Avg Cost Per Pack","Gross Cigarette Tax Revenue"]

    corr = df[corr_cols].corr()

    # ============================================================
    # DARK MODE STYLING
    # ============================================================
    dark_bg = "#0e0e10"
    card_bg = "#1a1b1f"
    text_color = "white"
    neon_blue = "#00b4ff"
    neon_pink = "#ff4ecd"

    tab_style = {
        "backgroundColor": card_bg,
        "color": text_color,
        "padding": "10px",
        "fontWeight": "bold",
        "border": "none"
    }
    tab_selected = {
        "backgroundColor": neon_blue,
        "color": "black",
        "padding": "10px",
        "fontWeight": "bold",
        "border": "none"
    }

    # ============================================================
    # DASH APP
    # ============================================================
    app = Dash(__name__, suppress_callback_exceptions=True)

    content = html.Div(
        style={"backgroundColor": dark_bg, "color": text_color, "padding": "10px"},
        children=[
            html.H1(
                "Tobacco Tax & Cigarette Consumption Dashboard (1990–2019)",
                style={"textAlign":"center","color":neon_blue,"fontWeight":"bold"}
            ),
            html.H3(
                "By Hiral Choksi — UConn",
                style={"textAlign":"center","color":neon_pink,"marginBottom":"20px"}
            ),

            dcc.Tabs(
                id="tabs",
                value="tab1",
                children=[
                    dcc.Tab(label="Overview", value="tab1", style=tab_style, selected_style=tab_selected),
                    dcc.Tab(label="State Clusters", value="tab2", style=tab_style, selected_style=tab_selected),
                    dcc.Tab(label="Correlation", value="tab3", style=tab_style, selected_style=tab_selected),
                    dcc.Tab(label="Geographic Maps", value="tab4", style=tab_style, selected_style=tab_selected),
                    dcc.Tab(label="Elasticity", value="tab5", style=tab_style, selected_style=tab_selected),
                    dcc.Tab(label="Compare States", value="tab6", style=tab_style, selected_style=tab_selected),
                    dcc.Tab(label="Data Table", value="tab7", style=tab_style, selected_style=tab_selected),
                ],
            ),

            html.Div(id="tab_content", style={"padding":"20px"})
        ]
    )

    app.layout = html.Div([
        html.Label("Chart theme"),
        dcc.RadioItems(id="theme", options=["Light", "Dark"], value="Dark", inline=True),
        content,
    ])

    # ============================================================
    # TAB RENDERING
    # ============================================================
    @app.callback(
        Output("tab_content","children"),
        Input("tabs","value"),
        Input("theme", "value")
    )
    def render_tab(tab, theme="Dark"):
        template = "plotly_dark" if theme == "Dark" else "plotly_white"

        # ---------------- TAB 1: OVERVIEW ----------------
        if tab == "tab1":
            smooth_x, smooth_y = loess_smooth(national["Year"], national["Y"])

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=national["Year"], y=national["Y"],
                mode="lines+markers",
                name="Actual",
                line=dict(color=neon_blue)
            ))

            fig.add_trace(go.Scatter(
                x=smooth_x, y=smooth_y,
                mode="lines",
                name="LOESS Trend",
                line=dict(color=neon_pink, width=4)
            ))

            # policy markers
            for yr, col in zip([1998,2009,2019], ["red","orange","purple"]):
                fig.add_vline(x=yr, line_color=col, line_dash="dash")

            # change-points
            for i in cp_idx:
                year = int(national.iloc[i]["Year"])
                fig.add_vline(x=year, line_dash="dot", line_color="lime")

            fig.update_layout(
                template=template,
                title="National Trend with LOESS + Policy Events + changepoints"
            )

            return dcc.Graph(figure=fig)

        # ---------------- TAB 2: CLUSTERS ----------------
        if tab == "tab2":
            fig = px.scatter(
                cluster_data,
                x="state_tax_pct",
                y="Y",
                color="cluster",
                color_discrete_map=cluster_colors,
                hover_name="state",
                title="K-Means State Clusters : State Clusters based on Tax Share & Consumption"
            )
            fig.update_layout(template=template)
            return dcc.Graph(figure=fig)

        # ---------------- TAB 3: CORRELATION ----------------
        if tab == "tab3":
            fig = px.imshow(
                corr,
                text_auto=True,
                color_continuous_scale="RdBu_r",
                title="Correlation Heatmap"
            )
            fig.update_layout(template=template)
            return dcc.Graph(figure=fig)

        # ---------------- TAB 4: MAPS ----------------
        if tab == "tab4":
            fig = px.choropleth(
                df,
                locations="state",
                locationmode="USA-states",
                color="state_tax_pct",
                animation_frame="Year",
                scope="usa",
                color_continuous_scale="Turbo",
                title="Animated US Map: State Tax Burden Over Time"
            )
            fig.update_layout(template=template)
            return dcc.Graph(figure=fig)

        # ---------------- TAB 5: ELASTICITY ----------------
        if tab == "tab5":
            df_el = df.copy()
            df_el["tax_bin"] = pd.cut(df_el["state_tax_pct"], bins=20)

            g = df_el.groupby("tax_bin", as_index=False, observed=True).agg(
                x=("state_tax_pct","mean"),
                y=("Y","mean")
            )

            g = g.dropna(subset=["x", "y"])
            slope, intercept = np.polyfit(g["x"], g["y"], 1)
            line = slope*g["x"] + intercept

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=g["x"], y=g["y"], mode="markers", marker=dict(color=neon_blue), name="Data"))
            fig.add_trace(go.Scatter(x=g["x"], y=line, mode="lines", line=dict(color=neon_pink, width=4), name="Trend"))

            fig.update_layout(template=template, title="Tax Share vs Consumption (descriptive binned trend)", xaxis_title="State tax share (fraction of retail price)", yaxis_title="Pack sales per capita")
            return dcc.Graph(figure=fig)

        # ---------------- TAB 6: COMPARE STATES ----------------
        if tab == "tab6":
            return html.Div([
                html.Label("Select State 1", style={"color":"white"}),
                dcc.Dropdown(options=states, value="NY", id="s1"),

                html.Br(),

                html.Label("Select State 2", style={"color":"white"}),
                dcc.Dropdown(options=states, value="KY", id="s2"),

                html.Br(),

                dcc.Graph(id="compare_graph")
            ])

        # ---------------- TAB 7: DATA TABLE ----------------
        if tab == "tab7":
            return html.Div([
                html.H3("Dataset Overview", style={"color": neon_blue}),
                dash_table.DataTable(data=df.to_dict("records"), columns=[{"name": c, "id": c} for c in df.columns], page_size=15, sort_action="native", filter_action="native", style_table={"overflowX": "auto"}, style_cell={"color": "#111", "backgroundColor": "white"})
            ])

    # ============================================================
    # CALLBACK: STATE COMPARISON
    # ============================================================
    @app.callback(
        Output("compare_graph","figure"),
        Input("s1","value"),
        Input("s2","value"),
        Input("theme", "value")
    )
    def compare_states(a, b, theme="Dark"):
        template = "plotly_dark" if theme == "Dark" else "plotly_white"
        fig = go.Figure()

        d1 = df[df["state"] == a]
        d2 = df[df["state"] == b]

        fig.add_trace(go.Scatter(x=d1["Year"], y=d1["Y"], mode="lines", name=a, line=dict(width=4, color=neon_blue)))
        fig.add_trace(go.Scatter(x=d2["Year"], y=d2["Y"], mode="lines", name=b, line=dict(width=4, color=neon_pink)))

        fig.update_layout(template=template, title=f"{a} vs {b} — Consumption Trends (1990–2019)")
        return fig

    # Expose pure callbacks for focused tests without starting a server.
    app.render_tab = render_tab
    app.compare_states = compare_states
    return app


def main():
    parser = argparse.ArgumentParser(description="Tobacco tax and consumption dashboard")
    parser.add_argument("--data", type=Path, required=True, help="Path to the raw Tax Burden on Tobacco CSV")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8060)
    args = parser.parse_args()
    create_app(args.data).run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
