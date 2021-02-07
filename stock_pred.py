import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
import yfinance
import plotly.graph_objects as go



def get_preds_high_low(stock_name, time_steps):
    data_source = data = yfinance.download(stock_name, period ="5y",  interval = "1d")
    data_source = data_source.dropna()
    data_source.reset_index(inplace= True)
    data_source_high = data_source[["Date","High"]]
    data_source_low = data_source[["Date","Low"]]
    data_source_low = data_source_low.rename(columns = {"Date":"ds","Low":"y"})
    data_source_high = data_source_high.rename(columns = {"Date":"ds","High":"y"})
    m_low = Prophet(daily_seasonality = True)    
    m_low.fit(data_source_low)
    future_low = m_low.make_future_dataframe(periods=time_steps)
    prediction_low = m_low.predict(future_low)
    m_high = Prophet(daily_seasonality = True) 
    m_high.fit(data_source_high)
    future_high = m_high.make_future_dataframe(periods=time_steps)
    prediction_high = m_high.predict(future_high)
    real_preds_high = prediction_high[-time_steps:]
    return data_source_low,data_source_high,m_low,m_high,prediction_low, prediction_high, real_preds_high

def get_plots(x_high,m_low,preds_low, preds_high, points_for_plot):
    colors = []
    for i in range(len(points_for_plot)):
      if points_for_plot.iloc[i]['Actions'] == "Buy":
          colors.append("green")
      elif points_for_plot.iloc[i]['Actions'] == "Sell":
          colors.append("red")
      else:
          colors.append('#8c564b')
    points_for_plot["Colors"] = colors
    fig1 = plot_plotly_v2(m_low,preds_low, xlabel='Date', ylabel='Stock Price')
    fig1 = fig1.add_scatter(x=preds_high['ds'], y=preds_high['yhat'],name='Predicted High',line=dict(color='orange'))
    fig1 = fig1.add_scatter(x = x_high["ds"], y = x_high["y"], name = 'Actual High', marker=dict(color="purple", size = 4),
      mode="markers" )
    for i in range(len(points_for_plot)):
      fig1 = fig1.add_scatter(x = [points_for_plot.iloc[i]['Date']], y = [points_for_plot.iloc[i]['Predicted High']], name = points_for_plot.iloc[i]['Actions'], marker=dict(color= points_for_plot.iloc[i]['Colors'], size = 10),
      mode="markers" )
    points_for_plot.drop(columns = ["Colors"], inplace = True)
    return fig1

def compute_points_df(real_preds_high):
    if (len(real_preds_high) >= 50):
        batch_min_max_size = int (0.3* len(real_preds_high))
        unique_window_size = int (0.1*len(real_preds_high))
    else:
        batch_min_max_size = 1
        unique_window_size = 1
    min_rows = []
    smallest_list = real_preds_high.nsmallest(batch_min_max_size,"yhat")
    min_rows = [smallest_list.iloc[0]]
    for index in range(len(smallest_list)):
        if index == 0:
            continue
        else:
          good_min_count = 0
          for row in min_rows:        
            if ((smallest_list.iloc[index]['ds'] - row['ds']).days < unique_window_size and (smallest_list.iloc[index]['ds'] - row['ds']).days > -unique_window_size):
                good_min_count +=1
          if (good_min_count == 0):
              min_rows.append(smallest_list.iloc[index])
    max_rows = []
    biggest_list = real_preds_high.nlargest(batch_min_max_size,"yhat")
    max_rows = [biggest_list.iloc[0]]
    for index in range(len(biggest_list)):
        if index == 0:
            continue
        else:
          good_min_count = 0
          for row in max_rows:        
            if ((biggest_list.iloc[index]['ds'] - row['ds']).days < unique_window_size and (biggest_list.iloc[index]['ds'] - row['ds']).days > -unique_window_size):
                good_min_count +=1
          if (good_min_count == 0):
              max_rows.append(biggest_list.iloc[index])
    
    points = [real_preds_high.iloc[0]] + min_rows + max_rows + [real_preds_high.iloc[-1]] 
    points_df = pd.DataFrame(points)
    points_df.drop_duplicates("ds", inplace=True)
    points_df = points_df[['ds','yhat']]
    points_df  = points_df.sort_values(by=['ds'])
    action_list = []
    for i in range(len(points_df)-1):
        if (points_df.iloc[i+1]['yhat']-points_df.iloc[i]['yhat'] < -0.1*points_df.iloc[0]['yhat']):
            action_list.append("Sell")
        elif (points_df.iloc[i+1]['yhat']-points_df.iloc[i]['yhat'] > 0.1*points_df.iloc[0]['yhat']):
            action_list.append("Buy")
        else:
            action_list.append("Hold")
    action_list.append("Null")
    points_df["Actions"] = action_list
    points_df.columns = ['Date','Predicted High', 'Actions']
    return points_df
    
def plot_plotly_v2(m, fcst, uncertainty=True, plot_cap=True, trend=False, changepoints=False,
                changepoints_threshold=0.01, xlabel='ds', ylabel='y', figsize=(900, 600)):
    
    prediction_color = '#0072B2'
    error_color = 'rgba(0, 114, 178, 0.2)'  # '#0072B2' with 0.2 opacity
    actual_color = 'black'
    cap_color = 'black'
    trend_color = '#B23B00'
    line_width = 2
    marker_size = 4

    data = []
    # Add actual
    data.append(go.Scatter(
        name='Actual Low',
        x=m.history['ds'],        
        y=m.history['y'],
        marker=dict(color=actual_color, size=marker_size),
        mode='markers'
    ))
    # Add lower bound
    if uncertainty and m.uncertainty_samples:
        data.append(go.Scatter(
            x=fcst['ds'],
            y=fcst['yhat_lower'],
            mode='lines',
            line=dict(width=0),
            hoverinfo='skip'
        ))
    # Add prediction
    data.append(go.Scatter(
        name='Predicted Low',
        x=fcst['ds'],
        y=fcst['yhat'],
        mode='lines',
        line=dict(color=prediction_color, width=line_width),
        fillcolor=error_color,
        fill='tonexty' if uncertainty and m.uncertainty_samples else 'none'
    ))
    # Add upper bound
    if uncertainty and m.uncertainty_samples:
        data.append(go.Scatter(
            x=fcst['ds'],
            y=fcst['yhat_upper'],
            mode='lines',
            line=dict(width=0),
            fillcolor=error_color,
            fill='tonexty',
            hoverinfo='skip'
        ))
    # Add caps
    if 'cap' in fcst and plot_cap:
        data.append(go.Scatter(
            name='Cap',
            x=fcst['ds'],
            y=fcst['cap'],
            mode='lines',
            line=dict(color=cap_color, dash='dash', width=line_width),
        ))
    if m.logistic_floor and 'floor' in fcst and plot_cap:
        data.append(go.Scatter(
            name='Floor',
            x=fcst['ds'],
            y=fcst['floor'],
            mode='lines',
            line=dict(color=cap_color, dash='dash', width=line_width),
        ))
    # Add trend
    if trend:
        data.append(go.Scatter(
            name='Trend',
            x=fcst['ds'],
            y=fcst['trend'],
            mode='lines',
            line=dict(color=trend_color, width=line_width),
        ))
    # Add changepoints
    if changepoints and len(m.changepoints) > 0:
        signif_changepoints = m.changepoints[
            np.abs(np.nanmean(m.params['delta'], axis=0)) >= changepoints_threshold
        ]
        data.append(go.Scatter(
            x=signif_changepoints,
            y=fcst.loc[fcst['ds'].isin(signif_changepoints), 'trend'],
            marker=dict(size=50, symbol='line-ns-open', color=trend_color,
                        line=dict(width=line_width)),
            mode='markers',
            hoverinfo='skip'
        ))

    layout = dict(
        showlegend=False,
        width=figsize[0],
        height=figsize[1],
        yaxis=dict(
            title=ylabel
        ),
        xaxis=dict(
            title=xlabel,
            type='date',
            rangeselector=dict(
                buttons=list([
                    dict(count=7,
                         label='1w',
                         step='day',
                         stepmode='backward'),
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(count=1,
                         label='1y',
                         step='year',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
        ),
    )
    fig = go.Figure(data=data, layout=layout)
    return fig

def get_profit(init_shares,init_price, table_data, current_stock_price):
    starting_money = init_shares*init_price
    difference_in_stocks = 0
    Amount_Bought = 0
    Amount_Sold = 0
    for row in table_data:
        if (row['Actions'] == "Buy"):
            difference_in_stocks += float(row['Number of Shares'])
            Amount_Bought += float(row['Number of Shares'])*float(row['Predicted High'])
        elif (row['Actions'] == "Sell"):
            difference_in_stocks -= float(row['Number of Shares'])
            Amount_Sold += float(row['Number of Shares'])*float(row['Predicted High'])
    current_shares = init_shares + difference_in_stocks    
    return (current_stock_price*(current_shares) -(Amount_Bought) + (Amount_Sold) - starting_money)

