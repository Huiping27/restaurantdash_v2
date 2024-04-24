import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine
import dash
from dash import html, dcc
import openpyxl as px


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

# Calculate total amounts for Month 1 and Month 2
competition_restaurants = 2932

# Identify restaurants exclusive to competitors
exclusive_to_competitors = 2726

# Create a bar plot
fig4 = go.Figure()

# Add bars for total amounts
fig4.add_trace(go.Bar(x=['Exclusive to Competitors','Total'], y=[ exclusive_to_competitors,competition_restaurants], name='Total', width=0.4))
# Update layout
fig4.update_layout(
    title='Exclusive Restaurants Only On Competitors',
    xaxis_title='Category',
    yaxis_title='Total Active Restaurants',
    barmode='group',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    yaxis=dict(range=[0, max(exclusive_to_competitors, competition_restaurants) * 1.1])  # Adjust y-axis range
)

# Calculate total amounts for Month 1 and Month 2
competition_restaurants = 2932

# Identify restaurants exclusive to competitors
exclusive_to_competitors = 2726

# Calculate the exclusive ratio
exclusive_ratio = exclusive_to_competitors / competition_restaurants 
# Calculate the market share of competitors
rest_market_ratio = 1 - exclusive_ratio

# Create a pie plot
fig5 = go.Figure(data=[go.Pie(labels=['Exclusive', 'Rest'], values=[exclusive_ratio, rest_market_ratio])])

# Update layout
fig5.update_layout(title='Exclusive On Competitos VS No Exclusive Competitors', legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

#groupby name and calcualte orders
restaurant_activity = compe_merge.groupby('name')['orders'].sum()
# Sort the restaurants based on the total orders in descending order
sorted_restaurants = restaurant_activity.sort_values(ascending=False)

# Get the top 10 active restaurants
top_10_active_restaurants = sorted_restaurants.head(10)

# Create a bar plot
fig6 = go.Figure()
fig6.add_trace(go.Bar(x=top_10_active_restaurants.index, y=top_10_active_restaurants.values))

# Update layout
fig6.update_layout(
    title='Top 10 Restaurants On Competitors',
    xaxis_title='Category',
    yaxis_title='Total Orders',
    barmode='group',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    yaxis=dict(range=[0, max(top_10_active_restaurants.values) * 1.5]),  # Adjust y-axis range
    height=600,  # Set the height of the figure
    width=1100    # Set the width of the figure
)

#groupby name and calcualte orders
restaurant_orders = compe_merge.groupby('name')['orders'].sum()

# Sort the restaurants based on the total orders in descending order and extract the top 10
top_10_restaurants = restaurant_orders.sort_values(ascending=False).head(10)

# Filter the top 10 restaurants to include only those present in the deliverando DataFrame
top_10_in_deliverando = top_10_restaurants[top_10_restaurants.index.isin(deliverando['name'])]
# Sort the restaurants based on the total orders in descending order and extract the top 10
top_10_restaurants = restaurant_orders.sort_values(ascending=False).head(10)

# Filter the top 10 restaurants to include only those present in the deliverando DataFrame
top_10_in_deliverando = top_10_restaurants[top_10_restaurants.index.isin(deliverando['name'])]


# Groupby name and calculate orders
restaurant_orders = compe_merge.groupby('name')['orders'].sum()
# Create a bar plot
fig7 = go.Figure()
fig7.add_trace(go.Bar(
    x=top_10_in_deliverando.index,  # x-axis: restaurant names
    y=top_10_in_deliverando.values,  # y-axis: total orders
))

# Update layout
fig7.update_layout(
    title='Top 10 Restaurants On Competitors Also On Delivery',
    xaxis_title='Restaurant Name',
    yaxis_title='Total Orders',
    height=600, 
    width=1100    
)

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
    dcc.Graph(id='graph5', figure=fig5),

    # Sixth graph
    dcc.Graph(id='graph6', figure=fig6),

    # Seventh graph
    dcc.Graph(id='graph7', figure=fig7)
])

# Run the app
if __name__ == '__main__':
    app.run_server(port=8057)
