import requests
from bs4 import BeautifulSoup
from datetime import datetime # Current date time in local system
import string
import pandas as pd


company_name = 'BankOfAmerica'
urll = 'https://careers.bankofamerica.com'

def extract():
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}
    url = 'https://careers.bankofamerica.com/en-us/job-search?ref=search&search=getAllJobs&start=0&rows=2000'
    r = requests.get(url,headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div',class_ = 'job-search-tile')
    for item in divs:
        title = item.find('a').text.strip()
        job_name = item.find('a', class_='job-search-tile__url t-track-search-select-position').text.strip()
        jobs_name = item.find('a', class_='job-search-tile__url t-track-search-select-position')
        req_id = jobs_name['href'][18:26]
        href = jobs_name['href']
        now_date = datetime.date(datetime.now())
        items = item.find('div', class_ = 'job-search-tile__detail').text.translate({ord(c): None for c in string.whitespace}).replace('Posted','')
        job_date = items[0:10]
        job_location = items[10:]
        job_link = urll+href
        job = {
            'comapnyName': company_name,
            'ReqId': req_id,
            'jobTitle': job_name,
            'location': job_location,
            'postingDate': job_date,
            'url': job_link,
            'extrationDate': now_date
        }
        joblist.append(job)
    return

joblist= []

c = extract()
transform(c)
print(len(joblist))


df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('BankOfAmerica.csv')
