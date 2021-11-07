import pdfplumber
import click
import json
import logging
import re
import requests

logging.basicConfig(level=logging.ERROR)

def normalisechars(text=''):
    text = re.sub('[\r\n]',' ',text)
    text = re.sub('"', '\\"', text)
    return text

def processtext(text=''):
    text = normalisechars(text)
    return text


@click.command()
@click.option("--inputfile",
                "-i",
                help="Specify input PDF file")
@click.option("--outfile",
                "-o",
                help="Specify output JSON file")
@click.option("--forcemode",
                "-f",
                required=False,
                help="Force mode - overwrite output file")
@click.option("--startpage",
                "-s",
                required=False,
                help="Start page",
                type=int)
@click.option("--numpages",
                "-n",
                required=False,
                help="Number of pages to process",
                type=int)
def convertpdftoidx(inputfile='', outfile='', forcemode=False, startpage=0, numpages=0):
    with pdfplumber.open(inputfile) as pdf:
        print(10)
        pagecounter = 0        
        if startpage is None:
            startpage = 1
        #if numpages is None:
        #    numpages = 1
        print(20)
        for p in pdf.pages:
            print(30)
            pagecounter+=1
            if pagecounter<startpage:
                continue
            
            if numpages is not None and pagecounter-startpage>numpages-1:
                break
            try:
                print(40)
                txt = processtext(p.extract_text())
                txt=txt.replace('"', '\"')
                doc=f'{{ "fields": [ {{ "name":"text", "value":"{txt}" }}, {{ "name":"source", "value":"{inputfile}" }}, {{ "name":"page", "value":"{pagecounter-1}"}} ] }}'
                print(f"sende doc {pagecounter-1}")
                ##print(doc)                
                r = requests.post("http://localhost:8090/v1/document", data=doc.encode('utf-8'), headers={'Content-type': 'application/json; charset=utf-8'})
                print(f"sended {r}")
                if r.status_code!=200:
                    print(f"error sending document {doc}")
                    print(r.text)
                    
                else:
                    print(f"200: {r.text}")
            except Exception as ex:
                pass

if __name__=="__main__":
    convertpdftoidx()
