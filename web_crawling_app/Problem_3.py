from flask import Flask, request, render_template
from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'Hello, week 15'

#--------------- TODO---------------- #
@app.route("/publication",methods=['GET'])
def publication():
   
    try:    
        year = request.args
        year = int(year["year"])

        if(year < 2000 or year > 2021):
            return render_template('publication.html', reportname=['PLEASE ENTER VALID YEAR'])
        
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
        
        
        return render_template('publication.html',reportname=reportname)

    except:
        return render_template('publication.html')
        

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)