from flask import Flask , render_template
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

req = Request('https://www.investing.com/indices/nasdaq-composite', headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Hello, week 15'


@app.route("/finance", methods=['GET'])
def finance():
    bsObject = BeautifulSoup(html, from_encoding="utf-8")
    instPrice = bsObject.find('div',{"class":"instrument-price_instrument-price__3uw25 flex items-end flex-wrap font-bold"})
    nasdaq = instPrice.find('span',{"class":"text-2xl"}).text
    return render_template('finance.html', nasdaq=nasdaq)


if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)