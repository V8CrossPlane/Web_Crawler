import os
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import lxml.html
import winshell


name = []
desired = []
wishes = []
location = []
work_place = []
salary = []
introduce =[]
birthday = []
gender =[]
updated = []
experience = []
introduce = []


pages = np.arange(1, 11, 1)
for page in pages:
    page = requests.get("https://tuyencongnhan.vn/tim-ho-so?&page=" + str(page))

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='result-search-job')
    #print(results.prettify())
    # jobs = results.find_all('div', class_='mng-company')
    
    for job in results.find_all('div', class_='mng-company'):
        updated_elem = job.find('p', class_='expired').text
        updated.append(updated_elem)

        hrefs = job.find_all('a', class_='btn btn-apply-s m-width-100', href=True)
        for links in hrefs:
            href = links['href']
            page2 = requests.get("https://tuyencongnhan.vn" + href)
            soup2 = BeautifulSoup(page2.content, 'html.parser')
            results2 = soup2.find(id='view-profile')
            
            TopCard = results2.find_all('div', class_='masthead')
            for job_elem in TopCard:
                name_elem = job_elem.find('h1', class_='mar-0').text.strip()
                name.append(name_elem)
                
                desired_elem = job_elem.find('h2', class_='mar-0 mb-15').text.strip()
                desired.append(desired_elem)

                gender_elem = job_elem.find('div', class_='field').text.replace("Giới tính", "").strip()
                gender.append(gender_elem)

                location_elem = job_elem.find('div', class_='field').find_next_sibling("div").text.replace("Địa chỉ:", "").strip()
                location.append(location_elem)

                birth_elem = job_elem.find('div', class_='field').find_next_sibling("div").find_next_sibling("div").text.replace("Ngày sinh", "").strip()
                birthday.append(birth_elem)


            doc = lxml.html.fromstring(page2.content)
            # section = doc.xpath('//*[@id="view-profile"]/div[2]/div')[0]

            exp_elem = doc.xpath('//*[@id="view-profile"]/div[2]/div/div/div[1]/div[1]/div/div[2]/p[2]/text()')
            experience.append(exp_elem)

            place_elem = doc.xpath('//*[@id="view-profile"]/div[2]/div/div/div[1]/div[6]/div/div[2]/p[2]/a/text()')
            work_place.append(place_elem)

            salary_elem = doc.xpath('//*[@id="view-profile"]/div[2]/div/div/div[1]/div[5]/div/div[2]/p[2]/text()')
            salary.append(salary_elem)
            

            # contents = doc.xpath('//*[@id="content"]')[0]
            intro_elem = doc.xpath('//*[@id="content"]/div[2]/div/div/text()')
            introduce.append(intro_elem)

            wish_elem = doc.xpath('//*[@id="content"]/div[10]/div/div/text()')
            wishes.append(wish_elem)


            df = pd.DataFrame(
                    {"Name":name, "Gender":gender,"Birthday":birthday, "Location":location, "Updated":updated, "Experience":experience,
                     "Place want to work":work_place, "Introduce":introduce, "Desired Salary":salary, "Desired":desired, "Wishes":wishes})
            df.to_excel(os.path.join(winshell.desktop(), "Profile.xlsx"))