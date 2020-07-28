
from requests import get
from bs4 import BeautifulSoup
from telegram.ext import Updater, MessageHandler, Filters
import logging
import os
TOKEN = os.environ.get("TOKEN")
PORT = os.environ.get("PORT",5000)
def getStatus(no):
  print(no)
  if not no.isdigit():
    return ["Please enter numbers only", "😕😕😕😕😕😕😕😕😕😕😕😕😕😕😕😕😕"]
  if not len(no) == 15:
    return ["Application number should have 15 digits","😕😕😕"]
  url1 = "https://edistrict.up.gov.in/edistrict/showStatushome.aspx?application_no="+no
  url2 = "https://edistrict.up.gov.in/edistrict/showAppDetails.aspx?xzatx="+no
  res1 = get(url1).text
  res2 = get(url2).text
  soup1 = BeautifulSoup(res1)
  soup2 = BeautifulSoup(res2)
  status = soup1.select("#status")
  if len(status) == 0 :
    return ["Application not found","🤔🤔🙄🤔🙄😳"]
  status = status[0].getText()
  rows = soup1.select("tr")
  res1 = status + "\n" 
  for i in range(5,9):
    row = rows[i]
    data = row.findAll("td")
    res1+=data[0].getText()
    res1+=" : "
    res1+=data[1].getText()
    res1+="\n"
  res2  = soup2.find("strong").getText()
  res2+="\n"
  rows = soup2.findAll("tr")
  for i in range(8,len(rows)):
     data = rows[i].findAll("td")
     for j in data:
       res2+=j.getText()
       res2+="->"
     res2+="\n"
  res = [res1,res2]
  return res

def status(update,context):
  context.bot.send_message(update.message.chat_id,getStatus(update.message.text)[0])
  context.bot.send_message(update.message.chat_id,getStatus(update.message.text)[1])
def main():
  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
  updater = Updater(TOKEN,use_context = True)
  dispatcher = updater.dispatcher

  handler = MessageHandler(Filters.text,status)
  dispatcher.add_handler(handler)
  updater.bot.setWebhook("https://application-tracker-bot.herokuapp.com/"+TOKEN)
  updater.start_webhook(listen = "0.0.0.0", port = int(PORT), url_path = TOKEN)
if __name__ == '__main__':
  main()
