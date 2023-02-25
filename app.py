import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import tkinter as tk


def get_news(ticker):
    # Bloomberg
    url1 = f'https://www.bloomberg.com/quote/{ticker}:US'
    response1 = requests.get(url1)
    soup1 = BeautifulSoup(response1.text, 'html.parser')
    article1 = soup1.find('h1', {'class': 'companyName__99a4824b'})
    title1 = article1.text.strip() if article1 else 'No news found.'
    link1 = url1 if article1 else ''
    
    # Yahoo Finance
    url2 = f'https://finance.yahoo.com/quote/{ticker}/news?p={ticker}'
    response2 = requests.get(url2)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    article2 = soup2.find('h3', {'class': 'Mb(5px)'})
    title2 = article2.text if article2 else 'No news found.'
    link2 = article2.a['href'] if article2 else ''
    
    # Reuters
    url3 = f'https://www.reuters.com/companies/{ticker}'
    response3 = requests.get(url3)
    soup3 = BeautifulSoup(response3.text, 'html.parser')
    article3 = soup3.find('div', {'class': 'ArticleHeader_headline__1W4uo'})
    title3 = article3.text if article3 else 'No news found.'
    link3 = url3 if article3 else ''
    
    return [(title1, link1), (title2, link2), (title3, link3)]


def plot_ticker(ticker):
    stock = yf.Ticker(ticker)
    history = stock.history(period="10y")
    history2 = stock.history(period="5y")
    history3 = stock.history(period="3y")
    
    plt.plot(history.index, history['Close'], label='10y')
    plt.plot(history2.index, history2['Close'], label='5y')
    plt.plot(history3.index, history3['Close'], label='3y')
    plt.legend()

    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.title(f"{ticker} Historical Prices")
    plt.show()    


def run_app():
    ticker = entry.get()
    news = get_news(ticker)
    news_text.delete('1.0', tk.END)
    for title, link in news:
        news_text.insert(tk.END, f'{title}\n{link}\n\n')
    plot_ticker(ticker)
2  
    
root = tk.Tk()
root.title("Financial News Aggregator")

# Set the window size
root.geometry('800x600')

# Create a frame for the input and button
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

label = tk.Label(input_frame, text="Enter a ticker symbol:")
label.pack(side='left')

entry = tk.Entry(input_frame, width=10, font=('Arial', 14))
entry.pack(side='left', padx=10)

button = tk.Button(input_frame, text="Search", command=run_app, font=('Arial', 14))
button.pack(side='left')

# Create a frame for the news text area
news_frame = tk.Frame(root)
news_frame.pack(pady=10)

news_label = tk.Label(news_frame, text="Recent financial news:", font=('Arial', 16))
news_label.pack()

news_text = tk.Text(news_frame, height=10, width=80, font=('Arial', 12))
news_text.pack(pady=10)

# Create a frame for the plot
plot_frame = tk.Frame(root)
plot_frame.pack(pady=10)

plot_label = tk.Label(plot_frame, text="Price history:", font=('Arial', 16))
plot_label.pack()

# Create a canvas for the plot
canvas = tk.Canvas(plot_frame, width=700, height=400)
canvas.pack()

# Create a scrollbar for the canvas
scrollbar = tk.Scrollbar(plot_frame, orient=tk.HORIZONTAL, command=canvas.xview)
scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

canvas.configure(xscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

# Create a frame inside the canvas to hold the plot
plot_canvas = tk.Frame(canvas)

canvas.create_window((0, 0), window=plot_canvas, anchor='nw')

root.mainloop()
