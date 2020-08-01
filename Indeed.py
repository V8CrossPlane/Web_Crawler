import os
import winshell
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import lxml.html
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

job_name = []
company_name = []
salary = []
date = []
Location = []
info = []
expired =[]

chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--incognito')
driver = webdriver.Chrome(options=chrome_options)

pages = np.arange(0, 111, 10)
for page in pages:
    page = driver.get("https://vn.indeed.com/jobs?q=Công+Nhân&l=Hà+Nội&start=" + str(page))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find(id='resultsCol')

    elements = results.find_all('div', class_='clickcard')
    for elem in elements:
        
        company_elements = elem.find('span', class_='company')
        if company_elements is None:
            company_name.append('None')
        else:
            company_name.append(company_elements.text.strip())

        job_elements = elem.find('h2', class_='title').text.strip()
        job_name.append(job_elements)


        salary_elements = elem.find('span', class_='salaryText')
        if salary_elements is None:
            salary.append('None')
        else:
            salary.append(salary_elements.text)

        date_elements = elem.find('span', class_='date').text
        if date_elements is None:
            date.append('None')
        else:
            date.append(date_elements)

        location_elements = elem.find(class_='location accessible-contrast-color-location')
        if location_elements is None:
            Location.append('None')
        else:
            Location.append(location_elements.text)

        info_elements = elem.find('div', class_='summary').text
        if info_elements is None:
            info.append('None')
        else:
            info.append(info_elements)

    # hrefs_elements = driver.find_elements_by_css_selector('.turnstileLink')
    # for href in hrefs_elements:
    #     links = href.get_attribute('href')
    #     page2 = requests.get(links)
    #     soup = BeautifulSoup(page2.content, 'html.parser')
    #     doc = lxml.html.fromstring(page2.content)


    df = pd.DataFrame(
            {'Company': company_name, 'Job': job_name, 'Salary': salary, 'location': Location, 'Date': date, 'Info': info})
    df.to_excel(os.path.join(winshell.desktop(), "Indeed.xlsx"))

driver.close()