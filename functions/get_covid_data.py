import requests
import datetime
import csv

def get_data():
    
    '''
    It downloads a CSV file from a website, reads it, and returns the values of the variables I need
    
    Returns
    -------
        Date, Last_day_inf, In_hospitals, ActiveCovidCases, Tests
    
    '''
    
    url = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/zakladni-prehled.csv"
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode("utf-8")

        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        my_list = list(cr)
        
        numbers = my_list[1]
        
        Date = str(datetime.date.today())     
        Last_day_inf = numbers[8]
        In_hospitals = numbers[6]
        ActiveCovidCases = numbers[3]
        Tests = numbers[7]

        return Date, Last_day_inf, In_hospitals, ActiveCovidCases, Tests