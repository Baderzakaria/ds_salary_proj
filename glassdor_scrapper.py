# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By


def get_jobs(keyword, num_jobs, verbose, path, sleep_time):
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    global job_title, salary_estimate2, size
    options = webdriver.ChromeOptions()

    # Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    # options.add_argument('headless')

    # Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)
    keyword = keyword.replace(' ', '-')
    url = 'https://www.glassdoor.com/Job/' + keyword + '-jobs-SRCH_KO0,10.htm?seniorityType=entrylevel&applicationType=1&remoteWorkType=1'
    # url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=UAE,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) <= num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(sleep_time)
        print("start")
        # Test for the "Sign Up" prompt and get rid of it.
        job_buttons = driver.find_elements(By.CLASS_NAME, "react-job-listing")
        # print(job_buttons[0].text)
        try:
            job_buttons[0].click()
        except ElementClickInterceptedException:
            print("x this is not working 0")

        print("waiting")
        time.sleep(1)
        print("stop")

        try:
            driver.find_element(By.CSS_SELECTOR, '[alt="Close"]').click()  # clicking to the X.
            print("not error")
        except NoSuchElementException:
            print("x this is not working 1")
            pass

        time.sleep(1)
        # Going through each job in this page
        job_buttons = driver.find_elements(By.CLASS_NAME,
                                           "react-job-listing")  # jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  # You might

            # print(job_button.text)
            time.sleep(3)
            collected_successfully = False

            while not collected_successfully:

                try:
                    company_name = driver.find_element(By.XPATH, '//div[@data-test="employerName"]').text
                    location = driver.find_element(By.XPATH, '//div[@data-test="location"]').text
                    job_title = driver.find_element(By.XPATH, '//div[@data-test="jobTitle"]').text
                    job_description = driver.find_element(By.ID, 'JobDescriptionContainer').text
                    collected_successfully = True
                    # print("company name_________"+company_name)
                    # print(job_title)
                    # print(job_description)
                    if driver.find_element(By.CLASS_NAME, "h3").text == "Error Loading":
                        print("error")
                        break
                except:
                    print("error 2")
                    time.sleep(5)
                    pass

            try:
                # salary_estimate = driver.find_element(By.XPATH, '//span[@class="css-0 e1wijj240"]').text
                salary_estimate = driver.find_element(By.XPATH, '//div[@class="css-1bluz6i e2u4hf13"]').text
                print(salary_estimate)
            except NoSuchElementException:

                salary_estimate = -1  # You need to set a "not found value. It's important."
                print("______3")
                pass

            try:
                rating = driver.find_element(By.XPATH, './/span[@class="css-1m5m32b e1tk4kwz2"]').text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found value. It's important."
                pass

            # Printing for debugging
            # if verbose:
            print("->Job Title: {}".format(job_title))
            print("->Salary Estimate: {} ".format(salary_estimate))
            print("->Job Description: {}\n".format(job_description[10]))
            print("->Rating: {}\n".format(rating))
            print("->Company Name: {}".format(company_name))
            print("->Location: {}".format(location))

            # Going to the Company tab...
            # clicking on this:
            # Company
            size = sector = founded = type_of_ownership = industry = revenue = competitors  = -1
            try:
                flex = driver.find_elements(By.XPATH,
                                            '//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]')

                for box in flex:
                    try:
                        value_var = -1
                        name_var = box.find_element(By.XPATH,
                                                    './/span[@class="css-1taruhi e1pvx6aw1"]').text
                        value_var = box.find_element(By.XPATH,
                                                     './/span[@class="css-i9gxme e1pvx6aw2"]').text

                        match name_var:
                            case "Size":
                                size = value_var
                            case "Industry":
                                industry = value_var
                            case "Type":
                                type_of_ownership = value_var
                            case "Revenue":
                                revenue = value_var
                            case "Founded":
                                founded = value_var
                            case "Sector":
                                sector = value_var

                    except NoSuchElementException:
                        print("error")
            except NoSuchElementException:
                print("error 2")
            # try:
            #     size = driver.find_element(By.XPATH,
            #                                   '//span[@class="css-i9gxme e1pvx6aw2"]').text
            # except NoSuchElementException:
            #     founded = -1
            #     pass
            #     print("error 6")
            #
            # try:
            #     founded = driver.find_element(By.XPATH,
            #                                       '//span[@class="css-i9gxme e1pvx6aw2"]').text
            # except NoSuchElementException:
            #     founded = -1
            #     pass
            #     print("error 6")
            #
            # try:
            #     type_of_ownership = driver.find_element(By.XPATH,
            #                                                 '//span[@class="css-i9gxme e1pvx6aw2"]').text
            # except NoSuchElementException:
            #
            #     type_of_ownership = -1
            #     print("error 7")
            #     pass
            # try:
            #     industry = driver.find_element(By.XPATH,
            #                                        '//span[@class="css-1taruhi e1pvx6aw1"]').text
            # except NoSuchElementException:
            #     industry = -1
            #     pass
            #
            # try:
            #     sector = driver.find_element(By.XPATH,
            #                                      '//span[@class="css-i9gxme e1pvx6aw2"]').text
            # except NoSuchElementException:
            #     sector = -1
            #     pass
            #
            # try:
            #     revenue = driver.find_element(By.XPATH,
            #                                       '//span[@class="css-i9gxme e1pvx6aw2"]').text
            # except NoSuchElementException:
            #     revenue = -1
            #     pass

            try:
                url_web = driver.find_element(By.XPATH, '// *[ @ id = "EmpBasicInfo"] / div[2] / div / a').get_attribute("href")

            except NoSuchElementException:
                url_web = -1
                pass
            # try:
            #     recomended = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div[2]/section/div/div/article/div/div[2]/div[1]/div[4]/div/div/div[2]/div[1]/div[1]/svg/g/text').get_attribute("x")
            # except NoSuchElementException:
            #     recomended = -1
            #     pass

            print("Size: {}".format(size))
            print("Founded: {}".format(founded))
            print("Type of Ownership: {}".format(type_of_ownership))
            print("Industry: {}".format(industry))
            print("Sector: {}".format(sector))
            print("Revenue: {}".format(revenue))
            print("link: {}".format(url_web))
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue,
                         "link": competitors})
            # #add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH, '//*[@id="MainCol"]/div[2]/div/div[1]/button[7]/span/svg/path').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs,
                                                                                                         len(jobs)))
            break

    return pd.DataFrame(jobs)
