import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Style for tiles
tile_style = {
    'background-color': '#f0f0f0',
    'border-radius': '10px',
    'padding': '5px',
    'margin': '5px',
    'text-align': 'center',
    'display': 'inline-block',
    'width': '80%'
}

# Load data
df = pd.read_csv('20240805_pricedata.csv')

# Data preprocessing
df['Verkauf in'] = pd.to_datetime(df['Verkauf in'])
df['Quarter'] = df['Verkauf in'].dt.to_period('Q')

colors = ['#F97A1F', '#C91D42', '#1DC9A4', '#141F52', '#B3B3B3']
category_order = sorted(df['Kategorie'].apply(str).unique())

# Creating Line Chart for Categories
category_grouped = df.groupby(['Kategorie', 'Quarter']).agg({'Verkaufspreis': 'median'}).reset_index()
category_grouped.sort_values('Quarter', inplace=True)
last_five_quarters = category_grouped['Quarter'].unique()[-5:]
category_grouped = category_grouped[category_grouped['Quarter'].isin(last_five_quarters)]

category_line_chart_figure = go.Figure()

for i, category in enumerate(category_order):
    category_data = category_grouped[category_grouped['Kategorie'] == category]
    category_line_chart_figure.add_trace(go.Scatter(
        x=category_data['Quarter'].astype(str),
        y=category_data['Verkaufspreis'],
        mode='lines+markers',
        name=category,
        line=dict(color=colors[i % len(colors)])
    ))

category_line_chart_figure.update_layout(
    xaxis_title='Quartal',
    yaxis_title='Medianpreis (in Tsd)',
    legend=dict(
        orientation='h',
        x=0.5,
        y=-0.3,
        xanchor='center',
        yanchor='top'
    ),
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(family='Roboto Condensed', size=14),
    yaxis=dict(
        tickvals=list(range(0, 100001, 10000)),
        ticktext=[str(int(value / 1000)) for value in range(0, 100001, 10000)]
    )
)

# Creating Stacked Bar Chart for Category Sales Count
quarterly_sales_count = df[df['Quarter'].isin(last_five_quarters)].groupby(['Quarter', 'Kategorie']).size().reset_index(name='Anzahl Verkäufe')
quarterly_totals_count = quarterly_sales_count.groupby('Quarter')['Anzahl Verkäufe'].sum().reset_index()
merged_data_count = pd.merge(quarterly_sales_count, quarterly_totals_count, on='Quarter', suffixes=('', '_total'))
merged_data_count['Percentage'] = (merged_data_count['Anzahl Verkäufe'] / merged_data_count['Anzahl Verkäufe_total']) * 100

stacked_bar_chart_figure = go.Figure()

for i, category in enumerate(category_order):
    category_data = merged_data_count[merged_data_count['Kategorie'] == category]
    stacked_bar_chart_figure.add_trace(go.Bar(
        name=category,
        x=category_data['Quarter'].astype(str),
        y=category_data['Percentage'],
        text=category_data['Percentage'].apply(lambda x: f'{x:.0f}%'),
        textposition='inside',
        marker_color=colors[i % len(colors)]
    ))

stacked_bar_chart_figure.update_layout(
    barmode='stack',
    xaxis=dict(title='Quartal', type='category'),
    yaxis=dict(title='Prozentualer Anteil (%)', tickformat=',d'),
    legend=dict(orientation='h', x=0.5, y=-0.3, xanchor='center', yanchor='top'),
    legend_title_text='Fahrzeugkategorie',
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(family='Roboto Condensed', size=14)
)

# Creating Line Chart for Vehicle Age Categories
age_cat_grouped = df.groupby(['fahrzeugalter_cat', 'Quarter']).agg({'Verkaufspreis': 'median'}).reset_index()
age_cat_grouped.sort_values('Quarter', inplace=True)
age_cat_grouped = age_cat_grouped[age_cat_grouped['Quarter'].isin(last_five_quarters)]
age_order = ["Bis 2 Jahre", "2 - 4 Jahre", "4 - 6 Jahre", "6 - 10 Jahre", "Über 10 Jahre"]

vehicle_age_line_chart_figure = go.Figure()

for i, age_cat in enumerate(age_order):
    age_data = age_cat_grouped[age_cat_grouped['fahrzeugalter_cat'] == age_cat]
    vehicle_age_line_chart_figure.add_trace(go.Scatter(
        x=age_data['Quarter'].astype(str),
        y=age_data['Verkaufspreis'],
        mode='lines+markers',
        name=age_cat,
        line=dict(color=colors[i % len(colors)])
    ))

vehicle_age_line_chart_figure.update_layout(
    xaxis_title='Quartal',
    yaxis_title='Medianpreis (in Tsd)',
    legend=dict(orientation='h', x=0.5, y=-0.3, xanchor='center', yanchor='top'),
    margin=dict(l=20, r=20, t=20, b=70),
    font=dict(family='Roboto Condensed', size=14)
)

# Creating Stacked Bar Chart for Vehicle Age Sales Count
age_cat_sales_count = df[df['Quarter'].isin(last_five_quarters)].groupby(['Quarter', 'fahrzeugalter_cat']).size().reset_index(name='Anzahl Verkäufe')
quarterly_totals_count = age_cat_sales_count.groupby('Quarter')['Anzahl Verkäufe'].sum().reset_index()
merged_data_age_count = pd.merge(age_cat_sales_count, quarterly_totals_count, on='Quarter', suffixes=('', '_total'))
merged_data_age_count['Percentage'] = (merged_data_age_count['Anzahl Verkäufe'] / merged_data_age_count['Anzahl Verkäufe_total']) * 100

vehicle_age_stacked_bar_figure = go.Figure()

for i, age_cat in enumerate(age_order):
    age_cat_data = merged_data_age_count[merged_data_age_count['fahrzeugalter_cat'] == age_cat]
    vehicle_age_stacked_bar_figure.add_trace(go.Bar(
        name=age_cat,
        x=age_cat_data['Quarter'].astype(str),
        y=age_cat_data['Percentage'],
        text=age_cat_data['Percentage'].apply(lambda x: f'{x:.0f}%'),
        textposition='inside',
        marker_color=colors[i % len(colors)]
    ))

vehicle_age_stacked_bar_figure.update_layout(
    barmode='stack',
    xaxis=dict(title='Quartal', type='category'),
    yaxis=dict(title='Prozentualer Anteil (%)', tickformat=',d'),
    legend=dict(orientation='h', x=0.5, y=-0.3, xanchor='center', yanchor='top', title='Fahrzeugalter Kategorie'),
    margin=dict(l=20, r=20, t=20, b=20),
    font=dict(family='Roboto Condensed', size=14)
)

# Creating the Dash app
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Link(rel='stylesheet', href='https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap'),
    html.Div([
        html.Img(src='assets/Header_PriceAnalyzer.jpg'),
        html.Div([
            html.Div([
                html.H2("Kerndaten auf einem Blick:", style={'textAlign': 'left', 'margin-top': '20px'})
            ], style={'width': '70%', 'display': 'inline-block'}),
        ], style={'display': 'flex', 'width': '100%'}),
        html.Div([
            html.Div('Tile 1', id='tile-1', style=tile_style),
            html.Div('Tile 2', id='tile-2', style=tile_style),
            html.Div('Tile 3', id='tile-3', style=tile_style),
            html.Div('Tile 4', id='tile-4', style=tile_style)
        ], style={'display': 'flex', 'justify-content': 'space-around', 'width': '100%'}),
        html.Div([
            html.Div([
                html.H3('Fahrzeugtyp', style={'textAlign': 'center'}),
                dcc.Dropdown(
                    id='category-dropdown',
                    options=[{'label': k, 'value': k} for k in df['Kategorie'].dropna().unique()] + [{'label': 'Total', 'value': 'Total'}],
                    value='Total',
                    style={'width': '100%', 'margin-right': '10px'}
                )
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'}),
            html.Div([
                html.H3('Alter des Fahrzeugs', style={'textAlign': 'center'}),
                dcc.Dropdown(
                    id='age-cat-dropdown',
                    options=[{'label': k, 'value': k} for k in df['fahrzeugalter_cat'].unique()] + [{'label': 'Total', 'value': 'Total'}],
                    value='Total',
                    style={'width': '100%', 'margin-right': '10px'}
                )
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px'})
        ], style={'display': 'flex', 'width': '100%'}),
        html.Div([
            html.Div([
                html.H2("Preisentwicklung seit Q4/2022", style={'textAlign': 'center'}),
                dcc.Graph(id='price-graph'),
            ], style={'width': '60%', 'display': 'inline-block'}),
            html.Div([
                html.Div([
                    html.Div([
                        html.Img(src='assets/OlegRubinov_Kommentar.jpg', style={'width': '100%', 'border-radius': '50%'})  # Ensure this path is correct
                    ], style={'width': '25%', 'display': 'inline-block', 'padding': '5px'}),
                    html.Div([
                        html.H4("Oleg Rubinov", style={'margin': '0', 'color': '#b22122', 'fontSize': '24px'}),
                        html.P("Co-Gründer & Geschäftsführer caravanmarkt24.de", style={'color': 'black', 'margin': '0'})
                    ], style={'width': '75%', 'display': 'inline-block', 'padding': '5px'})
                ], style={'display': 'flex', 'alignItems': 'center'}),
                html.P("""Einmal mehr unterstreicht das aktuell positive Marktgeschehen die Resilienz und Stärke des Gebrauchtwagensegments. Die Nachfrage nach gebrauchten Reisemobilen befindet sich auf Rekordniveau, die Preise bleiben stabil, das Angebot insbesondere in den Altersklassen ab 2021 und älter recht überschaubar. Händler können die Gunst der Stunde nutzen und durch den selektiven Zukauf von gepflegten Gebrauchtwagen Umsätze und Erträge steigern und neue Kundengruppen erschließen.""",
                style={'backgroundColor': '#f0f0f0', 'borderRadius': '10px', 'padding': '30px', 'fontSize': '18px', 'lineHeight': '1.5'})
            ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top', 'margin': '10px'})
        ], style={'display': 'flex', 'width': '100%'}),
        html.Div(id='data-alert', style={'textAlign': 'left', 'marginTop': 20, 'marginBottom': 20}),
        html.Div(style={'height': '20px'}),
        html.Img(src='assets/Fahrzeugkategorie_Block.jpg'),
        html.Div([
            html.Div([
                dcc.Graph(id='category_line_chart', figure=category_line_chart_figure),
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(id='stacked_bar_chart', figure=stacked_bar_chart_figure),
            ], style={'width': '50%', 'display': 'inline-block'}),
        ], style={'display': 'flex', 'width': '100%', 'margin-top': '20px'}),
        html.Div(style={'height': '20px'}),
        html.Img(src='assets/Fahrzeugalter_Block.jpg'),
        html.Div([
            html.Div([
                dcc.Graph(id='vehicle_age_line_chart', figure=vehicle_age_line_chart_figure),
            ], style={'width': '50%', 'display': 'inline-block'}),
            html.Div([
                dcc.Graph(id='vehicle_age_stacked_bar', figure=vehicle_age_stacked_bar_figure),
            ], style={'width': '50%', 'display': 'inline-block'}),
        ], style={'display': 'flex', 'width': '100%', 'margin-top': '20px'}),
        html.A(html.Img(src='assets/Feedback_PriceAnalyzer.png'), href='https://forms.office.com/Pages/ResponsePage.aspx?id=lIkX3lPYBk6rI3GE28OEZn_hulrk9ZNKrDbnahImCUpUMU40MlhFQU1EMFRSQ0xDNUlGNTlRQ1RNWC4u', target='_blank'),
    ], style={'fontFamily': 'Roboto Condensed', 'maxWidth': '1000px', 'margin': '0 auto'})
])

@app.callback(
    [Output('tile-1', 'children'), Output('tile-2', 'children'), Output('tile-3', 'children'), Output('tile-4', 'children')],
    [Input('category-dropdown', 'value'), Input('age-cat-dropdown', 'value')]
)
def update_tiles(selected_category, selected_age_cat):
    filtered_data = df.copy()
    if selected_category != 'Total':
        filtered_data = filtered_data[filtered_data['Kategorie'] == selected_category]
    if selected_age_cat != 'Total':
        filtered_data = filtered_data[filtered_data['fahrzeugalter_cat'] == selected_age_cat]

    q2_2024_data = filtered_data[filtered_data['Quarter'] == '2024Q2']
    median_price_2024 = round(q2_2024_data['Verkaufspreis'].median())
    q2_2023_data = filtered_data[filtered_data['Quarter'] == '2023Q2']
    median_price_2023 = q2_2023_data['Verkaufspreis'].median()
    percentage_diff_2023 = ((median_price_2024 - median_price_2023) / median_price_2023) * 100 if median_price_2023 else None
    current_quarter_period = pd.Period('2024Q2', freq='Q')
    previous_quarter_period = current_quarter_period - 1
    previous_quarter = previous_quarter_period.strftime('Q%q/%Y')
    previous_q_data = filtered_data[filtered_data['Quarter'] == previous_quarter_period]
    median_price_previous = previous_q_data['Verkaufspreis'].median()
    percentage_diff_previous = ((median_price_2024 - median_price_previous) / median_price_previous) * 100 if median_price_previous else None
    median_wunschpreis_2024 = q2_2024_data['Wunschpreis'].median()
    percentage_diff_wunschpreis = ((median_price_2024 - median_wunschpreis_2024) / median_wunschpreis_2024) * 100 if median_wunschpreis_2024 else None

    number_style = {'font-size': '20px', 'font-weight': 'bold'}
    tile_1_content = html.Div([
        html.Div(html.Strong("Händlereinkaufspreis"), style={'margin-bottom': '5px'}),
        html.Div("(Q2/2024):", style={'margin-bottom': '10px'}),
        html.Div(f"{median_price_2024:,.0f} €" if median_price_2024 else 'Data not available', style=number_style)
    ])
    tile_2_content = html.Div([
        html.Div(html.Strong("Trend (Vorjahr)"), style={'margin-bottom': '5px'}),
        html.Div("(vs. Q2/2023):", style={'margin-bottom': '10px'}),
        html.Div([
            html.Span(f"{percentage_diff_2023:.2f}%", style={'color': '#ff0000' if percentage_diff_2023 < 0 else '#008000'}),
            html.Span(f" ({median_price_2023:,.0f} €)" if median_price_2023 else ' (Data not available)', style={'color': '#888', 'font-size': '80%', 'font-weight': 'normal'})
        ], style=number_style) if percentage_diff_2023 is not None else 'Data not available'
    ])
    tile_3_content = html.Div([
        html.Div(html.Strong("Trend (letztes Quartal)"), style={'margin-bottom': '5px'}),
        html.Div(f"(vs. {previous_quarter}):", style={'margin-bottom': '10px'}),
        html.Div(html.Span(f"{percentage_diff_previous:.2f}%", style={'color': '#ff0000' if percentage_diff_previous < 0 else '#008000'}) if percentage_diff_previous is not None else 'Data not available', style=number_style)
    ])
    tile_4_content = html.Div([
        html.Div(html.Strong("Verhandlungsspielraum"), style={'margin-bottom': '5px', 'padding':'0'}),
        html.Div("(Angebots- zu Einkaufspreis):", style={'margin-bottom': '10px', 'font-size': '90%'}),
        html.Div(html.Span(f"{percentage_diff_wunschpreis:.2f}%", style={'color': '#ff0000' if percentage_diff_wunschpreis < 0 else '#008000'}) if percentage_diff_wunschpreis is not None else 'Data not available', style=number_style)
    ])

    return tile_1_content, tile_2_content, tile_3_content, tile_4_content

@app.callback(
    Output('price-graph', 'figure'),
    [Input('category-dropdown', 'value'), Input('age-cat-dropdown', 'value')]
)
def update_graph(selected_category, selected_age_cat):
    filtered_data = df.copy()
    if selected_category != 'Total':
        filtered_data = filtered_data[filtered_data['Kategorie'] == selected_category]
    if selected_age_cat != 'Total':
        filtered_data = filtered_data[filtered_data['fahrzeugalter_cat'] == selected_age_cat]

    filtered_quarterly = filtered_data.groupby('Quarter').agg({'Verkaufspreis': 'median'}).reset_index()
    last_5_quarters = filtered_quarterly['Quarter'].unique()[-5:]
    filtered_quarterly = filtered_quarterly[filtered_quarterly['Quarter'].isin(last_5_quarters)]
    filtered_quarterly['Verkaufspreis'] = filtered_quarterly['Verkaufspreis'] / 1000

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_quarterly['Quarter'].astype(str), y=filtered_quarterly['Verkaufspreis'],
                             mode='lines+markers', line=dict(color='#b22122', width=4), name='Medianpreis'))

    min_price = filtered_quarterly['Verkaufspreis'].min() - 10
    max_price = filtered_quarterly['Verkaufspreis'].max() + 10

    fig.update_layout(
        yaxis=dict(title='Medianpreis (in Tsd. €)', range=[min_price, max_price]),
        xaxis_title='Quartal',
        margin=dict(l=20, r=20, t=10, b=20),
        legend=dict(x=0.01, y=0.99, bordercolor="Black", borderwidth=2, orientation="h"),
        font=dict(family='Roboto Condensed', size=14)
    )

    return fig

@app.callback(
    Output('data-alert', 'children'),
    [Input('category-dropdown', 'value'), Input('age-cat-dropdown', 'value')]
)
def update_data_alert(selected_category, selected_age_cat):
    filtered_data = df.copy()
    if selected_category != 'Total':
        filtered_data = filtered_data[filtered_data['Kategorie'] == selected_category]
    if selected_age_cat != 'Total':
        filtered_data = filtered_data[filtered_data['fahrzeugalter_cat'] == selected_age_cat]

    q2_2024_data = filtered_data[filtered_data['Quarter'] == '2024Q2']

    if len(q2_2024_data) < 10:
        return html.Div('Hinweis: Für das letzte Quartal liegen uns zu wenige Daten vor. Bitte wählen Sie weniger Parameter.', 
                        style={'color': 'red', 'fontWeight': 'bold', 'fontSize': '17px', 'display': 'left', 'alignItems': 'left', 'justifyContent': 'left', 'height': '100%'})
    return ''

if __name__ == '__main__':
    app.run_server(debug=True)
