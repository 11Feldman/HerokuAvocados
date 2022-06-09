from dash import dcc,html,callback
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
import plotly.io as pio


data = pd.read_csv("avocado.csv")
data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m")
data.sort_values("Date", inplace=True)

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in np.sort(data.region.unique())
                            ],
                            value="Albany",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": avocado_type, "value": avocado_type}
                                for avocado_type in data.type.unique()
                            ],
                            value="organic",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.Date.min().date(),
                            max_date_allowed=data.Date.max().date(),
                            start_date=data.Date.min().date(),
                            end_date=data.Date.max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                            dcc.Loading([
                                dcc.Graph(
                                    id="price-chart", 
                                    config={"displayModeBar": False},
                                    className="card")
                                ],
                                type='cube'
                            )
                    ],
                    className="card",
                ),
                html.Div(
                    children=[
                        dcc.Loading([
                            dcc.Graph(
                                id="volume-chart", 
                                config={"displayModeBar": False},
                                className="card")
                            ],
                            type='cube'
                        )
                    ],
                    className="card",
                ),
                html.Div(
                    children=dcc.Loading([dcc.Graph(id="graph-iris",className='card')], type='cube'),
                    className='card'
                )
            ],
            className="wrapper",
        ),
    ]
)


@callback(
    [
        Output("price-chart", "figure"), 
        Output("volume-chart", "figure"),
        Output("graph-iris",'figure')
    ],
    [
        Input("region-filter", "value"),
        Input("type-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date"),
    ],
)
def update_charts(region, avocado_type, start_date, end_date):
    mask = (
        (data.region == region)
        & (data.type == avocado_type)
        & (data.Date >= start_date)
        & (data.Date <= end_date)
    )
    filtered_data = data.loc[mask, :]


    def graficoLineas(data_frame,x,y,colorLine='white',title=None,template='plotly_dark',tickprefix=None):
        fig = px.line(
            data_frame=data_frame,
            x=x,
            y=y,
            template=template
        )
        
        fig['data'][0]['line']['color']=colorLine

        fig.update_layout(
            title_text = title,
            title_x=0.05,
            title_xanchor='left'
        )

        fig.update_xaxes(
            fixedrange=True,
        )

        fig.update_yaxes(
            tickprefix=tickprefix,
            fixedrange=True,
        )

        return fig


    price_chart_figure=graficoLineas(
        data_frame=filtered_data,
        x='Date',
        y='AveragePrice',
        colorLine='white',
        title='Average Price of Avocados',
        tickprefix='$'
    )

    volume_chart_figure=graficoLineas(
        data_frame=filtered_data,
        x='Date',
        y='Total Volume',
        colorLine='red',
        title='Avocados Sold',
        tickprefix='$'
    )

    template = 'plotly_dark'

    df = px.data.iris()  # iris is a pandas DataFrame
    figIris = px.scatter(df, x="sepal_width", y="sepal_length",template=template)

    return price_chart_figure, volume_chart_figure, figIris