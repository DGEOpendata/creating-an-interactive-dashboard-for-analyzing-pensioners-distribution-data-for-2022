python
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the datasets
df_distribution = pd.read_excel('Distribution of Pensioners 2022.xlsx')
df_gender_distribution = pd.read_excel('Distribution of Pensioners per Gender 2022.xlsx')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Pensioners Distribution Dashboard"),
    dcc.Dropdown(
        id='gender-filter',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Male', 'value': 'Male'},
            {'label': 'Female', 'value': 'Female'}
        ],
        value='All',
        placeholder='Filter by Gender'
    ),
    dcc.Graph(id='pensioners-trend'),
    dcc.Graph(id='gender-distribution'),
])

# Callback to update graphs based on dropdown selection
@app.callback(
    [Output('pensioners-trend', 'figure'),
     Output('gender-distribution', 'figure')],
    [Input('gender-filter', 'value')]
)
def update_graphs(selected_gender):
    if selected_gender == 'All':
        filtered_df = df_distribution
    else:
        filtered_df = df_gender_distribution[df_gender_distribution['Gender'] == selected_gender]

    # Create a line chart for quarterly trends
    trend_fig = px.line(
        filtered_df,
        x='Quarter',
        y='Count',
        color='Type',
        title='Quarterly Pensioners Distribution'
    )

    # Create a pie chart for gender distribution
    gender_fig = px.pie(
        df_gender_distribution,
        names='Gender',
        values='Count',
        title='Gender Distribution of Pensioners'
    )

    return trend_fig, gender_fig

if __name__ == '__main__':
    app.run_server(debug=True)
