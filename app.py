from dash import Dash,dcc,html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from pages import gapminder,avocado
from dash_bootstrap_templates import load_figure_template

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# This loads the "cyborg" themed figure template from dash-bootstrap-templates library,
# adds it to plotly.io and makes it the default figure template.
load_figure_template("slate")

app =Dash(
    __name__, 
    external_stylesheets=[dbc.themes.SLATE,dbc.icons.FONT_AWESOME]
)

server = app.server

app.title = "Data Analitycs"

sidebar = html.Div(
    [
        html.Div(
            [
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                html.Img(src=PLOTLY_LOGO, style={"width": "3rem"}),
                html.H2("Menú"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="fas fa-home me-2"), html.Span("Home")],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-line-chart me-2"),
                        html.Span("Avocados"),
                    ],
                    href="/avocados",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-globe me-2"),
                        html.Span("gapminder"),
                    ],
                    href="/gapminder",
                    active="exact",
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)

content = html.Div(id="page-content", className="content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# set the content according to the current pathname
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return avocado.layout
    elif pathname == "/avocados":
        return avocado.layout
    elif pathname == "/gapminder":
        return gapminder.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(debug=False)