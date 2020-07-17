import os
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import six
import lxml.html
import winshell


picture = []
name = []
desired = []
wishes = []
location = []
place_work = []
salary = []
introduce =[]
birthday = []
gender =[]
expired = []
experience = []
introduce = []


pages = np.arange(1, 11, 1)
for page in pages:
    page = requests.get("https://tuyencongnhan.vn/tim-ho-so?&page=" + str(page))

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='result-search-job')
    #print(results.prettify())
    jobs = results.find_all('div', class_='mng-company')
    for job in jobs:
        hrefs = job.find_all('a', class_='btn btn-apply-s m-width-100', href=True)
        for links in hrefs:
            a = links['href']
            page = requests.get("https://tuyencongnhan.vn" + a)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id='view-profile')
            
            TopCard = results.find_all('div', class_='masthead')
            for job_elem in TopCard:
                name_elem = job_elem.find('h1', class_='mar-0').text.strip()
                name.append(name_elem)
                
                des_elem = job_elem.find('h2', class_='mar-0 mb-15').text.strip()
                desired.append(des_elem)

                gender_elem = job_elem.find('div', class_='field').text.replace("Giới tính", "").strip()
                gender.append(gender_elem)

                location_elem = job_elem.find('div', class_='field').find_next_sibling("div").text.replace("Địa chỉ:", "").strip()
                location.append(location_elem)

                birth_elem = job_elem.find('div', class_='field').find_next_sibling("div").find_next_sibling("div").text.replace("Ngày sinh", "").strip()
                birthday.append(birth_elem)


            doc = lxml.html.fromstring(page.content)

            section = doc.xpath('//*[@id="view-profile"]/div[2]/div')[0]
            exp_elem = section.xpath('//*[@id="view-profile"]/div[2]/div/div/div[1]/div[1]/div/div[2]/p[2]/text()')
            experience.append(exp_elem)

            place_elem = doc.xpath('//*[@id="view-profile"]/div[2]/div/div/div[1]/div[6]/div/div[2]/p[2]/a/text()')
            place_work.append(place_elem)

            salary_elem = doc.xpath('//*[@id="view-profile"]/div[2]/div/div/div[1]/div[5]/div/div[2]/p[2]/text()')
            salary.append(salary_elem)
            

            contents = doc.xpath('//*[@id="content"]')[0]
            intro_elem = contents.xpath('//*[@id="content"]/div[2]/div/div/text()')
            introduce.append(intro_elem)

            wish_elem = contents.xpath('//*[@id="content"]/div[10]/div/div/text()')
            wishes.append(wish_elem)


            df = pd.DataFrame(
                    {"Name":name, "Gender":gender,"Birthday":birthday, "Location":location, "Experience":experience, "Place want to work":place_work, "Introduce":introduce, "Desired Salary":salary, "Desired":desired, "Wishes":wishes})
            # df.to_excel(os.path.expanduser("~/Desktop/Profile.xlsx"))
            df.to_excel(os.path.join(winshell.desktop(), "Profile.xlsx"))