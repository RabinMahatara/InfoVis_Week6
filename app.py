from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px

# Initialize the Dash app
app = Dash(__name__)

# Load the EM-DAT disaster data
emdat_url = 'https://raw.githubusercontent.com/RabinMahatara/Group-Research-Proposal/1c317906599be80326c1f75eb6777816a4ec9454/public_emdat_2024-11-07.xlsx'
emdat_data = pd.read_excel(emdat_url)

# Function to create choropleth map
def create_choropleth(data, disaster_type, color_scale, title):
    # Filter data for the specific disaster type
    disaster_data = data[data['Disaster Type'] == disaster_type]
    # Group by ISO country codes and count events
    regional_data = disaster_data.groupby('ISO').size().reset_index(name='Event Count')
    # Create the choropleth map
    fig = px.choropleth(
        regional_data,
        locations="ISO",  # Use the 'ISO' column for country codes
        color="Event Count",
        color_continuous_scale=color_scale,
        title=title,
        locationmode="ISO-3"  # Ensure ISO-3 codes are used
    )
    return fig

# Create visualizations
fig_drought = create_choropleth(emdat_data, 'Drought', "Blues", "Regional Distribution of Droughts")
fig_flood = create_choropleth(emdat_data, 'Flood', "Reds", "Regional Distribution of Floods")

# Define the layout of the app
app.layout = html.Div([
    html.H1("Disaster Distribution Visualizations", style={'textAlign': 'center'}),
    html.Div([
        html.H2("Droughts", style={'textAlign': 'center'}),
        dcc.Graph(figure=fig_drought)
    ]),
    html.Div([
        html.H2("Floods", style={'textAlign': 'center'}),
        dcc.Graph(figure=fig_flood)
    ])
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
