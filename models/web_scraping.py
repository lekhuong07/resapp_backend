from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import pandas as pd

NUMBER_JOBS = 100

LINKEDIN_URL = "https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=usa"
driver = webdriver.Chrome()


def get_number_jobs_parsed(wd):
    no_of_jobs = str(wd.find_element(By.CSS_SELECTOR, 'h1>span').get_attribute('innerText'))
    if "+" in no_of_jobs:
        noj = min(int(no_of_jobs[:-1].replace(",", "")), NUMBER_JOBS)
    else:
        noj = min(int(no_of_jobs), NUMBER_JOBS)
    return noj


def get_job_list(wd):
    noj = get_number_jobs_parsed(wd)
    i = 2
    while i <= int(noj / 25) + 1:
        print(i, noj / 25)
        wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        i = i + 1
        try:
            wd.find_element(By.XPATH, '/html/body/main/div/section/button').click()
            time.sleep(5)
        except:
            pass
            time.sleep(5)

    job_lists = wd.find_element(By.CLASS_NAME, 'jobs-search__results-list')
    jobs = job_lists.find_elements(By.TAG_NAME, 'li')  # return a list
    return jobs


def get_job_description(wd):
    jobs = get_job_list(wd)
    jd = []
    seniority = []
    emp_type = []
    job_func = []
    industries = []
    for job in jobs:
        for item in range(len(jobs)):
            job_func0 = []
            industries0 = []
            # clicking job to view job details
            job_click_path = f'/html/body/main/div/section[2]/ul/li[{item + 1}]/img'
            job_click = job.find_element(By.XPATH, job_click_path).click()
            time.sleep(5)

            jd_path = '/html/body/main/section/div[2]/section[2]/div'
            jd0 = job.find_element(By.XPATH, jd_path).get_attribute('innerText')
            jd.append(jd0)

            seniority_path = '/html/body/main/section/div[2]/section[2]/ul/li[1]/span'
            seniority0 = job.find_element(By.XPATH, seniority_path).get_attribute('innerText')
            seniority.append(seniority0)

            emp_type_path = '/html/body/main/section/div[2]/section[2]/ul/li[2]/span'
            emp_type0 = job.find_element(By.XPATH, emp_type_path).get_attribute('innerText')
            emp_type.append(emp_type0)

            job_func_path = '/html/body/main/section/div[2]/section[2]/ul/li[3]/span'
            job_func_elements = job.find_elements_by_xpath(job_func_path)
            for element in job_func_elements:
                job_func0.append(element.get_attribute('innerText'))
                job_func_final = ', '.join(job_func0)
                job_func.append(job_func_final)
            industries_path = '/html/body/main/section/div[2]/section[2]/ul/li[4]/span'
            industries_elements = job.find_elements_by_xpath(industries_path)
            for element in industries_elements:
                industries0.append(element.get_attribute('innerText'))
                industries_final = ', '.join(industries0)
                industries.append(industries_final)

    job_data = pd.DataFrame({
        'Description': jd,
        'Level': seniority,
        'Type': emp_type,
        'Function': job_func,
        'Industry': industries,
    })
    # cleaning description column
    job_data['Description'] = job_data['Description'].str.replace('\n', ' ')
    job_data.to_excel('SWE.xlsx', index=False)
    return jobs


if __name__ == "__main__":
    wd = webdriver.Chrome()
    wd.get(LINKEDIN_URL)
    # print(get_number_jobs_parsed(wd))
    print(len(get_job_description(wd)))
