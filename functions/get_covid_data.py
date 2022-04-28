import requests
import datetime
import csv

def get_data():
    
    url = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/zakladni-prehled.csv"
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode("utf-8")

        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        my_list = list(cr)
        
        text = my_list[0]
        numbers = my_list[1]
        
        datum = str(datetime.date.today())     
        nakazeni_vcera = numbers[8]
        hospitalizovani = numbers[6]
        aktivni_covid = numbers[3]
        testy = numbers[7]

        return datum, nakazeni_vcera, hospitalizovani, aktivni_covid, testy