from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time, datetime
from selenium.webdriver.common.by import By

def main():
    driver = webdriver.Chrome()

    # url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=as&searchTextText=India&txtKeywords=&txtLocation=India'
    url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=&txtLocation=India&cboWorkExp1=0'
    driver.get(url)
    # print(driver)

    time.sleep(15)

    try:
        driver.find_element(By.XPATH,'/html/body/div[2]/div[1]/table/tbody/tr/td[2]/div/span').click()
    except Exception as e:
        pass

    
    time.sleep(10)

    soup = BeautifulSoup(driver.page_source, features='html.parser')
    # print(soup.encode('utf-8'))

    result = soup.find('ul',class_ = 'new-joblist')
    result2 = result.find_all('li',class_= 'clearfix job-bx wht-shd-bx')
    # print(result2) 
    # driver.find('span', id = 'closeSpanId')
    
    
# Now lets extract the company name, title, apply link etc
    pages = np.arange(1,2)
    for page in pages:
        job_data = []
        for i in result2:
            #TITLE
            title = i.find('a')
            title = title.text
            # print(title)

            #COMPANY
            company = i.find('h3', class_ = 'joblist-comp-name')
            company = company.text
            # print(company)

            #EXPERIENCE
            experience = i.find('i', class_ = 'material-icons').next_sibling
            # print(experience)

            #SALARY
            try:
                salary = i.find('i', class_ = 'material-icons rupee').next_sibling.strip()
                # print(salary)
            except Exception as e:
                salary = 'Salary Information Not Available'

            #CITY
            city = i.find('span').text.strip()
            # city = i.find('i', 'span')
            # city = city.text
            # print(city)

            #URL
            link = i.find('a').get('href')
            # print(url)

            job_data.append([title, company, experience, salary, city, link])

        # driver.quit() 

        df = pd.DataFrame(job_data, columns=['Title', 'Company', 'Experience', 'Salary','City', 'URL'])
        print(df.head())

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        try:
            driver.find_element(By.XPATH, '/html/body/div[3]/div[4]/section/div[2]/div/div[3]/em[2]/a').click()
        except Exception as e:
            pass
            

    today = datetime.datetime.today().strftime('%Y-%m-%d')
    path_to_save = f'E:\\DATA SCIENCE\\WEB_SCRAPPING\\TimeJobs_{today}.csv'
    df.to_csv(path_to_save) 
# print(df)
if __name__ == "__main__":
    main()
