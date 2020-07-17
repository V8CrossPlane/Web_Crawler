import os
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as np
import lxml.html
import winshell

Cpn_name = []
job_name = []
expired =[]
salary = []
number = []
location = []
fields = []
benefit = []
require = []
profile_require = []


pages = np.arange(1, 11, 1)
for page in pages:
    page = requests.get("https://tuyencongnhan.vn/tim-nha-tuyen-dung?keyword=&city_id=&career_id=" + str(page))

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='search-job')
    doc = lxml.html.fromstring(page.content)

    for links in soup.findAll('p', class_='job-title'):
        a = links.findAll('a')
        for link in a:
            # hrefs = link.get('href')
            href = link['href']
            # pages1 = np.arange(1, 6, 1)
            for p in pages:
                p = requests.get("https://tuyencongnhan.vn" + href + "?page=" + str(p))
                soup = BeautifulSoup(p.content, 'html.parser')
                results = soup.find(id='pjax-employer-detail')
                jobs = results.find_all('article', class_='job-available')
                for job in jobs:
                    job_name_elem = job.find('span', class_='i-title').text
                    job_name.append(job_name_elem)

                    href1 = job.find_all('a', class_='btn btn-apply-s m-width-100', href=True)
                    for h in href1:
                        b = h['href']
                        page2 = requests.get("https://tuyencongnhan.vn" + b)
                        soup = BeautifulSoup(page2.content, 'html.parser')
                        results = soup.find(id='tab-job-detail')
                        doc = lxml.html.fromstring(page2.content)
                        
                        Info = doc.xpath('//*[@id="tab-job-detail"]')[0]
                        cpn_name_elem = Info.xpath('//*[@id="tab-job-detail"]/div/div/div[2]/div[5]/address/strong/a/text()')
                        Cpn_name.append(cpn_name_elem)

                        expired_elem = Info.xpath('//*[@id="tab-job-detail"]/div/div/div[1]/div/div[1]/div[2]/p/text()')
                        expired.append(expired_elem)

                        salary_elem = Info.xpath('//*[@id="tab-job-detail"]/div/div/div[1]/div/div[2]/div[2]/p/text()')
                        salary.append(salary_elem)

                        number_elem = Info.xpath('//*[@id="tab-job-detail"]/div/div/div[1]/div/div[3]/div[2]/p/text()')
                        number.append(number_elem)

                        location_elem = Info.xpath('//*[@id="tab-job-detail"]/div/div/div[1]/div/div[5]/div[2]/p/a/text()')
                        location.append(location_elem)

                        fields_elem = Info.xpath('//*[@id="tab-job-detail"]/div/div/div[1]/div/div[6]/div[2]/p/a/text()')
                        fields.append(fields_elem)

                        description = results.find_all('div', class_='col-xs-12 col-md-8 pull-right')
                        for d in description:
                            benefit_elem = d.find('div', class_='content-job-detail quyen-loi-duoc-huong').get_text().strip()
                            benefit.append(benefit_elem)

                            require_elem = d.find('div', class_='content-job-detail yeu-cau-cong-viec').get_text().strip()
                            require.append(require_elem)

                            profile_require_elem = d.find('div', class_='content-job-detail yeu-cau-ho-so').get_text().strip()
                            profile_require.append(profile_require_elem)

                    df = pd.DataFrame(
                    {'Company Name':Cpn_name, 'Job Name':job_name, 'Number':number, 'Expired':expired, 'Salary':salary, 'Location':location, 'Fields':fields, 'Benefit':benefit, 'Require':require, 'Profile_require':profile_require})
                    # df.replace("(['\\n,\s+])", "", regex=True, inplace=True)
                    df['Number'] = [re.sub(r"(['\\n,\s+])", "", str(x)) for x in df['Number']]
                    df['Expired'] = [re.sub(r"(['\\n,\s+])", "", str(x)) for x in df['Expired']]
                    df['Salary'] = [re.sub(r"(['\\n,\s+])", "", str(x)) for x in df['Salary']]
                    df.to_excel(os.path.join(winshell.desktop(), "Companies.xlsx"))