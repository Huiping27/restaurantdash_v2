import plotly.graph_objects as go
import pandas as pd
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output
import base64

# Define the author's name
author = "Li"

# Initialize the Dash app
app = dash.Dash()
server = app.server

# Read the necessary data
deliverando = pd.read_csv('SalesAnalyst_deliverando.csv', sep=';')
compe_1 = pd.read_excel('SalesAnalyst_Competition.xlsx', sheet_name='Month 1')
compe_2 = pd.read_excel('SalesAnalyst_Competition.xlsx', sheet_name='Month 2')
compe_merge = pd.concat([compe_1, compe_2], ignore_index=True)

# Calculate total amounts for Month 1 and Month 2 on Deliverando
active_restaurants_month1 = deliverando[deliverando['Month 1'] > 0]['name'].nunique()
active_restaurants_month2 = deliverando[deliverando['Month 2'] > 0]['name'].nunique()

# Calculate the difference and percentage change
difference_deliverando = active_restaurants_month2 - active_restaurants_month1
percentage_deliverando = (difference_deliverando / active_restaurants_month1) * 100

# Create a bar plot for total amounts and difference on Deliverando
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=['Month 1', 'Month 2'], y=[active_restaurants_month1, active_restaurants_month2], name='Total', width=0.3))
fig1.add_annotation(x='Month 2', y=active_restaurants_month2, text=f'Difference: +{difference_deliverando} ({percentage_deliverando:.2f}%)', showarrow=True, arrowhead=1, ax=0, ay=-40)
fig1.update_layout(
    title='Comparison of Month 1 and Month 2 on Deliverando',
    xaxis_title='Month',
    yaxis_title='Total Active Restaurants',
    barmode='group',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    yaxis=dict(range=[0, max(active_restaurants_month1, active_restaurants_month2) * 1.1])
)

# Calculate total amounts for Month 1 and Month 2 on Competitors
competition_restaurants_m1 = compe_merge[compe_merge['month'] == 1]['name'].nunique()
competition_restaurants_m2 = compe_merge[compe_merge['month'] == 2]['name'].nunique()

# Calculate the difference and percentage change
difference_competitors = competition_restaurants_m2 - competition_restaurants_m1
percentage_competitors = (difference_competitors / competition_restaurants_m1) * 100

# Create a bar plot for total amounts and difference on Competitors
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=['Month 1', 'Month 2'], y=[competition_restaurants_m1, competition_restaurants_m2], name='Total', width=0.4))
fig2.add_annotation(x='Month 2', y=competition_restaurants_m2, text=f'Difference: +{difference_competitors} ({percentage_competitors:.2f}%)', showarrow=True, arrowhead=1, ax=0, ay=-40)
fig2.update_layout(
    title='Comparison of Month 1 and Month 2 on Competitors',
    xaxis_title='Month',
    yaxis_title='Total Active Restaurants',
    barmode='group',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    yaxis=dict(range=[0, max(competition_restaurants_m1, competition_restaurants_m2) * 1.1])
)

# Calculate market share of Deliverando and Competitors
total_restaurants = deliverando['name'].nunique() + compe_merge['name'].nunique()
deliverando_market_share = deliverando['name'].nunique() / total_restaurants
competitors_market_share = compe_merge['name'].nunique() / total_restaurants

# Create a pie plot for market share
fig3 = go.Figure(data=[go.Pie(labels=['Deliverando', 'Competitors'], values=[deliverando_market_share, competitors_market_share])])
fig3.update_layout(title='Market Share Comparison: Deliverando vs Competitors', legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

# Calculate exclusive restaurants on competitors
competition_restaurants_total = 2932
exclusive_to_competitors = 2726
exclusive_ratio = exclusive_to_competitors / competition_restaurants_total
rest_market_ratio = 1 - exclusive_ratio

# Create a pie plot for exclusive vs non-exclusive competitors
fig4 = go.Figure(data=[go.Pie(labels=['Exclusive', 'Rest'], values=[exclusive_ratio, rest_market_ratio])])
fig4.update_layout(title='Exclusive vs Non-Exclusive Competitors', legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

# Calculate top 10 active restaurants on competitors
top_10_active_restaurants = compe_merge.groupby('name')['orders'].sum().nlargest(10)

# Create a bar plot for top 10 active restaurants on competitors
fig5 = go.Figure(data=[go.Bar(x=top_10_active_restaurants.index, y=top_10_active_restaurants.values)])
fig5.update_layout(title='Top 10 Restaurants on Competitors', xaxis_title='Restaurant Name', yaxis_title='Total Orders', height=600, width=1100)

# Define the layout of the app with all graphs
app.layout = html.Div(children=[
    html.H1(children='Deliverando and Competitors in Graz'),

    # First graph
    dcc.Graph(id='graph1', figure=fig1),

    # Second graph
    dcc.Graph(id='graph2', figure=fig2),

    # Third graph
    dcc.Graph(id='graph3', figure=fig3),

    # Fourth graph
    dcc.Graph(id='graph4', figure=fig4),

    # Fifth graph
    dcc.Graph(id='graph5', figure=fig5)
])

# Download functionality
@app.server.route("/download")
def download_csv():
    df = pd.DataFrame({'Deliverando_Month1': [active_restaurants_month1],
                       'Deliverando_Month2': [active_restaurants_month2],
                       'Difference_Deliverando': [difference_deliverando],
                       'Percentage_Change_Deliverando': [percentage_deliverando],
                       'Competitors_Month1': [competition_restaurants_m1],
                       'Competitors_Month2': [competition_restaurants_m2],
                       'Difference_Competitors': [difference_competitors],
                       'Percentage_Change_Competitors': [percentage_competitors],
                       'Deliverando_Market_Share': [deliverando_market_share],
                       'Competitors_Market_Share': [competitors_market_share],
                       'Exclusive_to_Competitors': [exclusive_to_competitors],
                       'Rest_Market_Ratio': [rest_market_ratio]})
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return html.Div([
        html.A('Download CSV Data', href=csv_string, download='data.csv')
    ])

# Run the app
if __name__ == '__main__':
    app.run_server(port=8057)

