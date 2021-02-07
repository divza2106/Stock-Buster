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



app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP])


app.layout = html.Div([

 html.H1(children="Stock Buster", style={'textAlign':'center', 'color': '#8B008B','font-size':'80px'}),

   html.Label("    Input Stock:   ",style = {'font-size': '20px'}),
   dcc.Input(
       id='my-id',
       placeholder="ex. AAPL",
       type='text',
       value='AAPL',
       style = {"font-size":"18px"},
       size = '30'),

   html.Div(id='my-div'),

   html.Br(),

   html.Label("    Input Forecasting Window (Days):   ", style = {'font-size': '20px'}),
   dcc.Input(
       id='days-id',
       placeholder="ex. 365",
       type='number',
       value=365,
       style = {"font-size":"18px"},
       size = '30'),

   html.Div(id='my-div2'),

   html.Br(),

   html.Button('Submit', id='submit-val', n_clicks=0, style = {'width':'150px','height':'50px','font-size':'20px'}),
    html.Div(id='container-button-basic',
             children=''),

    html.Br(),
    html.Br(),
    html.Br(),

   dbc.Progress('', value=75, style={"height": "30px"},striped=True,animated=True, id='progress-bar'),
   html.Br(),

   html.H2(id = 'graph-header' ,style={'textAlign':'center','font-size':'35px'}),


   html.Br(),
   html.Br(),

   dcc.Graph(id = 'fig', style={
            'height': 500,
            'width': 900,
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto",
            }),

   html.Br(),
   html.Br(),
   html.Br(),
   html.Br(),
   html.Br(),
   html.Br(),
   html.Br(),
   html.Br(),
   html.Br(),
   html.Br(),

   html.Label("   Input Number of Shares in Posession:   ", style = {'font-size': '20px'}),
   dcc.Input(
       id='Initial-Shares',
       placeholder="ex. 250",
       type='number',
       value=0,
       style = {"font-size":"18px"},
       size = '30'
       ),
    
    html.Br(),
    html.Br(),

    html.Label("   Input Amount Paid Per Share in Posession:   ", style = {'font-size': '20px'}),
   dcc.Input(
       id='Price-Of-Share',
       placeholder="ex. 11.67",
       type='number',
       value=0,
       style = {"font-size":"18px"},
       size = '30'),
    
    html.Br(),
    html.Br(),
    html.Br(),
    
    html.H2(id ='table-header' ,style={'textAlign':'center','font-size':'35px'}),

    html.Br(),
    html.Br(),

    dash_table.DataTable(
    id='table',editable=True, style_cell={
        'whiteSpace': 'normal',
        'height': '45px',
    },style_data = {'font-size':'20px'},style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'font-size':'20px'
    }),

    html.Br(),
    html.Br(),

    html.Button('Submit', id='submit-table', n_clicks=0,  style = {'width':'150px','height':'50px','font-size':'20px'}),
    html.Div(id='container-button-basic1',
             children=''),

    html.H2(id='Pred-Message',style={'textAlign':'center','font-size':'30px'}, children=''),

    html.Div(id='current-stock-price',style={'display': 'none'}),
    dcc.Interval(
            id='interval-component',
            interval=1000, # in milliseconds
            n_intervals=0
        )

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
    f = open("progress.txt", "w")
    f.write("processing")
    f.close()
    x_low,x_high,m_low,m_high,preds_low, preds_high, real_preds_high = stock_pred.get_preds_high_low(input_value,days)
    points_for_plot = stock_pred.compute_points_df(real_preds_high=real_preds_high)
    fig1 = stock_pred.get_plots(x_high,m_low,preds_low,preds_high,points_for_plot)
    current=points_for_plot.iloc[-1][-2]    
    points_df_new = points_for_plot.drop(points_for_plot.tail(1).index)
    points_df_new["Number of Shares"] = [0 for i in range(len(points_df_new))]
    graph_string = 'Graph of Predicted High/Low Stock Prices for ' + input_value  
    table_string = 'Table of Suggest Buy/Hold/Sell Points for ' + input_value   
    f = open("progress.txt", "w")
    f.write("done")
    f.close()
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


@app.callback(
    Output(component_id='progress-bar', component_property='style'),    
     Input('interval-component', 'n_intervals')    
)
def change_progress(n):      
    f = open("progress.txt", "r")
    x = f.read()
    f.close()
    if x=='processing':
        return {"height": "30px"}
    else:
       return {"height": "30px","visibility":"hidden"}


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080)













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