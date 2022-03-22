from flask import Flask, request, render_template
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

app = Flask(__name__)

# You can create a new template or add a function.
# The contents of index.html should always be maintained.
# The style of the html tag is not reflected in the score.

#--------------- TODO---------------- #
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#--------------- TODO---------------- #
@app.route("/finance",methods=['GET'])
def finance():    
    url = "https://www.investing.com/indices/nasdaq-composite"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bsObject = BeautifulSoup(html, from_encoding="utf-8")
    instPrice = bsObject.find('div',{"class":"instrument-price_instrument-price__3uw25 flex items-end flex-wrap font-bold"})
    nasdaq = instPrice.find('span',{"class":"text-2xl"}).text
    return render_template('finance2.html', nasdaq=nasdaq)

#--------------- TODO---------------- #
@app.route("/covid",methods=['GET'])
def covid():    
    url = "https://covid19.who.int/table"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    bsObject = BeautifulSoup(html, from_encoding="utf-8", features="html.parser")  
    countries = bsObject.select(
        '#gatsby-focus-wrapper > div > div.sc-AxjAm.sc-fzpmMD.buBEYf > div > div.sc-AxjAm.sc-pIjat.rFwNh > div > div > div.tbody > div > div'
    )
    names=[]
    totals=[]
    deaths=[]
    for i in range(3,8):
        name = countries[0].select(
            f'div:nth-child({i}) > div.column_name.td > div > span'
        )
        
        total = bsObject.select(
            f'#gatsby-focus-wrapper > div > div.sc-AxjAm.sc-fzpmMD.buBEYf > div > div.sc-AxjAm.sc-pIjat.rFwNh > div > div > div.tbody > div > div > div:nth-child({i}) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)'
        )
        
        death = countries[0].select(
            f'div:nth-child({i}) > div.column_Cumulative_Deaths.td > div'
        )
     
        names.append(name[0].text)
        totals.append(total[0].text)
        deaths.append(death[0].text)
    
    return render_template('covid2.html',names=names, totals=totals, deaths=deaths)

#--------------- TODO---------------- #
@app.route("/publication",methods=['GET'])
def publication():
    url = "http://monet.skku.edu/?page_id=3550"
    
    try:    
        year = request.args
        year = int(year["year"])

        if(year < 2000 or year > 2021):
            return render_template('publication2.html', reportname=['PLEASE ENTER VALID YEAR'])
        
        req = Request('http://monet.skku.edu/?page_id=3550', headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()
        soup = BeautifulSoup(html,from_encoding='utf-8')
        page = soup.select_one(
            '#after_submenu > div > div > div > div'
        )
        reports=page.select(
            'section.avia_codeblock_section + div'
        )
        
        report = reports[0].select(
            'article > div > header > h2'
        )
        
        report = reports[2021-year].find_all('h2',{'class':'post-title'})
        reportname=[]
        for i in report:
            reportname.insert(0,i.text)
            
            
        getDiv = soup.select(
            '#after_submenu > div > div > div > div > div:nth-child(4)'
        )
        
        
        return render_template('publication2.html',reportname=reportname)

    except:
        return render_template('publication2.html')
        
        

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)