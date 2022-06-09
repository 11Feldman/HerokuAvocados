from dash import dcc, html,callback
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.io as pio

template = 'plotly_dark'

df = px.data.gapminder()

dff = df[df.year.between(1952, 1982)]
dff = dff[dff.continent.isin(df.continent.unique()[1:])]
line_fig = px.line(
    dff, x="year", y="gdpPercap", color="continent", line_group="country",template=template
)

dff = dff[dff.year == 1982]
scatter_fig = px.scatter(
    dff, x="lifeExp", y="gdpPercap", size="pop", color="pop", size_max=60,template=template
).update_traces(marker_opacity=0.8)

avg_lifeExp = (dff["lifeExp"] * dff["pop"]).sum() / dff["pop"].sum()
map_fig = px.choropleth(
    dff,
    locations="iso_alpha",
    color="lifeExp",
    title="%.0f World Average Life Expectancy was %.1f years" % (1982, avg_lifeExp),
    template=template
)

hist_fig = px.histogram(dff, x="lifeExp", nbins=10, title="Life Expectancy",template=template)

graphs = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=line_fig,className="card"), className="card",lg=5),
                dbc.Col(dcc.Graph(figure=scatter_fig,className="card"), className="card",lg=5),
            ],
            # className="mt-4",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(figure=hist_fig,className="card"),className="card", lg=5),
                dbc.Col(dcc.Graph(figure=map_fig,className="card"),className="card", lg=5),
            ],
            # className="mt-4",
        ),
    ]
)

heading = html.H1("Dash Bootstrap Template Demo", className="bg-primary text-white p-2")

layout = dbc.Container(fluid=True, children=[heading, graphs])
