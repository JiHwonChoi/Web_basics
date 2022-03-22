from flask import Flask,  render_template
from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
req = Request('https://covid19.who.int/table', headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req).read()




@app.route('/', methods=['GET'])
def index():
    return 'Hello, week 15'

#--------------- TODO---------------- #
@app.route("/covid",methods=['GET'])
def covid():
    bsObject = BeautifulSoup(html, from_encoding="utf-8", features="html.parser")  
    countries = bsObject.select(
        '#gatsby-focus-wrapper > div > div.sc-AxjAm.sc-fzpmMD.buBEYf > div > div.sc-AxjAm.sc-pIjat.rFwNh > div > div > div.tbody > div > div'
    )
    names=[]
    totals=[]
    deaths=[]
    print(countries)
    # for i in range(3,8):
    #     name = countries[0].select(
    #         f'div:nth-child({i}) > div.column_name.td > div > span'
    #     )
        
    #     total = bsObject.select(
    #         f'#gatsby-focus-wrapper > div > div.sc-AxjAm.sc-fzpmMD.buBEYf > div > div.sc-AxjAm.sc-pIjat.rFwNh > div > div > div.tbody > div > div > div:nth-child({i}) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)'
    #     )
        
    #     death = countries[0].select(
    #         f'div:nth-child({i}) > div.column_Cumulative_Deaths.td > div'
    #     )
     
    #     names.append(name[0].text)
    #     totals.append(total[0].text)
    #     deaths.append(death[0].text)
    
    return render_template('covid.html',names=names, totals=totals, deaths=deaths)
      

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)