import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
import stock_pred
import dash_bootstrap_components as dbc

# my_variable = "AAPL"
# x_low,x_high,m_low,m_high,preds_low, preds_high, real_preds_high = stock_pred.get_preds_high_low(my_variable,365)
# points_for_plot = stock_pred.compute_points_df(real_preds_high=real_preds_high)
# fig1 = stock_pred.get_plots(x_high,m_low,preds_low,preds_high,points_for_plot)



app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([

 html.H1(children="Stock Buster", style={'textAlign':'center', 'color': '#8B008B','font-size':'80px'}),

   html.Label("Input Stock:   "),
   dcc.Input(
       id='my-id',
       placeholder="ex. AAPL",
       type='text',
       value='AAPL'),

   html.Div(id='my-div'),

   html.Br(),

   html.Label("Input Forecasting Window (Days):   "),
   dcc.Input(
       id='days-id',
       placeholder="ex. 365",
       type='number',
       value=365),

   html.Div(id='my-div2'),

   html.Br(),

   html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children=''),
   html.Br(),

   html.H2(id = 'graph-header' ,style={'textAlign':'center','font-size':'35px'}),


   html.Br(),

   dcc.Graph(id = 'fig'),

   html.Br(),
   html.Br(),
   html.Br(),

   html.Label("Input Number of Shares in Posession:   "),
   dcc.Input(
       id='Initial-Shares',
       placeholder="ex. 250",
       type='number',
       value=0),
    
    html.Br(),
    html.Br(),

    html.Label("Input Amount Paid Per Share in Posession:   "),
   dcc.Input(
       id='Price-Of-Share',
       placeholder="ex. 11.67",
       type='number',
       value=0),
    
    html.Br(),
    html.Br(),
    html.Br(),
    
    html.H2(id ='table-header' ,style={'textAlign':'center','font-size':'35px'}),

    html.Br(),
    html.Br(),

    dash_table.DataTable(
    id='table',editable=True),

    html.Br(),
    html.Br(),

    html.Button('Submit', id='submit-table', n_clicks=0),
    html.Div(id='container-button-basic1',
             children=''),

    html.H2(id='Pred-Message',style={'textAlign':'center','font-size':'30px'}, children=''),

    html.Div(id='current-stock-price',style={'display': 'none'})

])

@app.callback(
    Output(component_id='fig', component_property='figure'),
    Output(component_id = 'table', component_property = 'columns'),
    Output(component_id = 'table', component_property = 'data'),  
    Output(component_id='current-stock-price',component_property = 'children'), 
    Output(component_id='graph-header',component_property = 'children'), 
    Output(component_id='table-header',component_property = 'children'), 
    [Input('submit-val', 'n_clicks')],
    [State(component_id='my-id', component_property='value')],
    [State(component_id='days-id',component_property='value')]
)

def update_output_div(n,input_value,days):    
    x_low,x_high,m_low,m_high,preds_low, preds_high, real_preds_high = stock_pred.get_preds_high_low(input_value,days)
    points_for_plot = stock_pred.compute_points_df(real_preds_high=real_preds_high)
    fig1 = stock_pred.get_plots(x_high,m_low,preds_low,preds_high,points_for_plot)
    current=points_for_plot.iloc[-1][-2]    
    points_df_new = points_for_plot.drop(points_for_plot.tail(1).index)
    points_df_new["Number of Shares"] = [0 for i in range(len(points_df_new))]
    graph_string = 'Graph of Predicted High/Low Stock Prices for ' + input_value  
    table_string = 'Table of Suggest Buy/Hold/Sell Points for ' + input_value   
    return fig1, [{"name": i, "id": i} for i in points_df_new.columns], points_df_new.to_dict('records'), current, graph_string, table_string

@app.callback(
    Output(component_id='Pred-Message', component_property='children'),       
    [Input('submit-table', 'n_clicks')],
    [State(component_id = 'table', component_property = 'data')],
    [State(component_id='current-stock-price', component_property='children')],      
    [State(component_id='Initial-Shares', component_property='value')],
    [State(component_id='Price-Of-Share',component_property='value')]
)
def table_prediction(n,table_data, current_stock_price, initial_shares,price_of_shares):      
    predicted_profit = stock_pred.get_profit(initial_shares,price_of_shares,table_data, current_stock_price)    
    reco = "Given our recommendation and your shares allocation, you would make a net profit of " + str(predicted_profit) + "."
    return reco

if __name__ == '__main__':
    app.run_server(debug=True)













# import dash
# import dash_table
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.express as px
# import pandas as pd
# from dash.dependencies import Input, Output
# import stock_pred

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# x_low,x_high,m_low,m_high,preds_low, preds_high, real_preds_high = stock_pred.get_preds_high_low("AAPL",365)
# points_for_plot = stock_pred.compute_points_df(real_preds_high=real_preds_high)
# fig1 = stock_pred.get_plots(x_low,x_high,m_low,m_high,preds_low, preds_high)
# params = [
#     'Weight', 'Torque', 'Width', 'Height',
#     'Efficiency', 'Power', 'Displacement'
# ]

# # assume you have a "long-form" data frame
# # see https://plotly.com/python/px-arguments/ for more options
# app.layout = dash_table.DataTable(
#     id='table',
#     columns=[{"name": i, "id": i} for i in points_for_plot.columns],
#     data=points_for_plot.to_dict('records')
# )

# if __name__ == '__main__':
#     app.run_server(debug=True)









# app.layout = html.Div(children=[
#     html.H1(children='Financial Forecast'),

#     html.Div(children='''
#         A web application that predicts the future of stocks.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig1),

#     dash_table.DataTable(
#         id='table-editing-simple',
#         columns=(
#             [{'id': 'Model', 'name': 'Model'}] +
#             [{'id': p, 'name': p} for p in params]
#         ),
#         data=[
#             dict(Model=i, **{param: 0 for param in params})
#             for i in range(1, 5)
#         ],
#         editable=True
#     ),
#     dcc.Graph(id='table-editing-simple-output'),

#     html.Label('Text Input'),
#     dcc.Input(value='MTL', type='text')
#     ])

# @app.callback(
#     Output('table-editing-simple-output', 'figure'),
#     Input('table-editing-simple', 'data'),
#     Input('table-editing-simple', 'columns'))
# def display_output(rows, columns):
#      df = pd.DataFrame(rows, columns=[c['name'] for c in columns])

# if __name__ == '__main__':
#     app.run_server(debug=True)