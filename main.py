import os
import telebot
import yfinance as yf

API_KEY = '1879593700:AAFGOM5iBq3gc8hE39QhlKGHenI3HzXA__4'
bot = telebot.TeleBot(API_KEY) # create bot object / instance of the TeleBot class

@bot.message_handler(commands=['greet'])
def greet(message):
  bot.reply_to(message, "Hey, hows it going?")

@bot.message_handler(commands=['hello'])
def hello(message):
  bot.send_message(message.chat.id, "MINIONS!")

@bot.message_handler(commands=['wsb'])
def get_stocks(message):
  stocks = ['CLOV', 'GME', 'AMC']
  stock_data = []
  columns = ['Stock']
  i = 0
  for stock in stocks:
    stock_data.append([stock])
    data = yf.download(tickers=stock, period="2d", interval="1d")
    data = data.reset_index()
    for index, row in data.iterrows():
      if i == 0:
        format_date = row['Date'].strftime('%d/%m')
        columns.append(format_date)
      price = round(row['Close'], 2)
      stock_data[i].append(price)
    i += 1
  response = f"{columns[0] : <10}{columns[1]: ^10}{columns[2]: >10}\n"
  for row in stock_data:
    response += f"{row[0]: <10}{row[1]: ^10}{row[2]: >10}\n"
  response += "\nStock Data"
  print(response)
  bot.send_message(message.chat.id, response)
    
  
def stock_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "price":
    return False
  else:
    return True

@bot.message_handler(func=stock_request)
def send_price(message):
  request = message.text.split()[1]
  data = yf.download(tickers=request, period="5m", interval="1m")
  if data.size > 0:
    data = data.reset_index()
    data['format_date'] = data['Datetime'].dt.strftime('%d/%m %I:%M %p')
    data.set_index('format_date', inplace=True)
    print(data.to_string())
    bot.send_message(message.chat.id, data['Close'].to_string(header=False))
  else:
    bot.send_message(message.chat.id, "No data")

bot.polling()

