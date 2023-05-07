# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#Launch site list for dropdown
launch_site_list = list(spacex_df['Launch Site'].unique())
launch_site_opt={'All Sites':'ALL'}
for i in launch_site_list:
    launch_site_opt[i]=i

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div([
                                    # Create an division for adding dropdown helper text for choosing launch site

                                    html.Div(
                                        [
                                        html.H2('Select Launch Site:', style={'margin-right': '1em','font-size': '22px'})
                                        ]
                                    ),
                                    dcc.Dropdown(id='site-dropdown',
                                                    options=[{'label': 'All Sites', 'value': 'ALL'}]+
                                                            [{'label': i, 'value': i} for i in launch_site_list],
                                                    value='ALL',
                                                    placeholder="Select a Launch site here",
                                                    searchable=True,
                                                    style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}),
                                        
                                    ], style={'display':'flex'}),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # # TASK 3: Add a slider to select payload range

                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0:'0',10000:'10000'},
                                                value=[spacex_df["Payload Mass (kg)"].min(),spacex_df["Payload Mass (kg)"].max()]),

                                # # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                # 
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))


def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
    if entered_site == 'ALL':
        fig_pie = px.pie(spacex_df, values='class', 
                    names='Launch Site', 
                    title='Total Success Launches by all sites')
        return fig_pie
    else:
        # return the outcomes piechart for a selected site
        fig_pie = px.pie(filtered_df, values='class',
                    names='class',
                    title="Total Success Launches for site {}".format(entered_site))
        return fig_pie

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
 
def get_scatter(entered_site, payload):
    scatter_df_all = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]
    scatter_df_site = spacex_df[spacex_df['Launch Site']==entered_site][spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]
    if entered_site == 'ALL':
        fig_scatter = px.scatter(scatter_df_all,
                                 x="Payload Mass (kg)",
                                 y='class',
                                 color="Booster Version Category",
                         title="Correlation between Payload and Booster version for all sites")
        return fig_scatter
    else:
        # return the outcomes piechart for a selected site
        fig_scatter = px.scatter(scatter_df_site,x="Payload Mass (kg)",y='class',color="Booster Version Category",
                         title="Correlation between Payload and Booster version for {}".format(entered_site))
        return fig_scatter
    
# def get_scatter_graph(site)
# Run the app
if __name__ == '__main__':
    app.run_server()
