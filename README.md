# StockBuster
## Simplifying Stocks: Offering you suggestions on when to buy, sell, or hold and letting you know potential profit!
We have website currently running on: http://stockbuster.tech/ 
Deployed on Google Cloud Compute with domain name from Domain.com
### Inspiration
The inspiration for this project came from the fact that the stock market is becoming an increasingly big part of everyone's lives. With trading apps like Robinhood making buying and selling stock that much more accessible to individuals, we wanted to create an app that could help people see trends in various stocks in the market and even suggest when they should buy, sell, or hold. 

### What it does
Stock Buster allows you to input any stock and the number of days into the future that you want predictions. Given these inputs, a graph is generated where you can see the predicted high and low prices of that stock for the number of days given as well as suggested points where you should buy, sell, or hold the stock. A table is also generated giving specific dates and stock prices on the days that you should buy/hold/sell. The user is then given the opportunity to input how many shares of that stock they already own and at what price they bought that stock. They are also able to edit the last column of the table generated to edit the number of shares they would like to buy/sell. Based on these inputs, an estimated net profit that the user would gain from taking the model's recommendation is generated.

### How we built it
We began by determining where we wanted our stock data to come from and since we wanted to be able to predict for any stock in the world, we decided to use the yahoo finance API and used Facebook prophet to fit a time series forecasting model to the data.  We used the past 5 years worth of the daily high and low stock prices to predict however many days desired into the future.
Using Dash on Python we created a front-end application that could take "stock name" and "number of days of desired predictions" as inputs so the model is trained on that specific stock. Using Plotly with Dash we were able to create an interactive plot as well as a dynamic table of future stock prices and suggested buy/hold/sell dates. To determine optimal buy/sell/hold points, we found the local minimums and maximums in our predictions and suggested buying, selling, and holding based on increases/decreases over 10%. We also came up with the algorithm to calculate the net profit generated from the trading decisions.

### Challenges we ran into
One challenge we encountered was preprocessing Yahoo Finance stock data into usable data to input into the Facebook prophet model. Another challenge was triggering the training of the model in the back-end using inputs from the front-end.

### Accomplishments that we're proud of
Contrary to other machine learning models that are expensive to train and are trained exclusively on specific stock data sets, we created an app that utilizes a model that can train on demand using any stock's data. This allows for real time analysis on a plethora of stocks.

### What we learned
We learned how to create interactive plots with Plotly, use Facebook prophet model to create an ARIMA time series model, scrape date using Yahoo Finance API, create application using Dash and Flask on Python.

### What's next for Stock Buster
In the future we hope to expand Stock Buster to be able to track the future of multiple stocks at once and understand the profit you would can by making optimal suggested buys and sells. This would enable individuals to make more informed trading decisions and see how their entire stock portfolio is contributing to their financial success.

### Instalation
Run these following commands:
Download and Install Anaconda
pip install dash
pip install pandas
pip install matplotlib
conda install -c conda-forge fbprophet
pip install yfinance
pip install dash-bootstrap-components

### Usage
python Hacklytics_Dash.py
