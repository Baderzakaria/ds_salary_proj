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

def get_jobs(keyword, num_jobs, verbose,path,sleep_time):

    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    #Initializing the webdriver
    global job_title
    options = webdriver.ChromeOptions()

    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')

    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=UAE,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(sleep_time)
        print("start")
        #Test for the "Sign Up" prompt and get rid of it.
        job_buttons = driver.find_elements(By.CLASS_NAME,"react-job-listing")
        #print(job_buttons[0].text)
        try:
            job_buttons[0].click()
        except ElementClickInterceptedException:
            print("x this is not working 0")

        print("waiting")
        time.sleep(1)
        print("stop")

        try:
            driver.find_element(By.CSS_SELECTOR,'[alt="Close"]').click()  #clicking to the X.
            print("not error")
        except NoSuchElementException:
            print("x this is not working 1")
            pass

        time.sleep(1)
        #Going through each job in this page
        job_buttons = driver.find_elements(By.CLASS_NAME,"react-job-listing")  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might

            #print(job_button.text)
            time.sleep(3)
            collected_successfully = False

            while not collected_successfully:

                try:
                    company_name = driver.find_element(By.XPATH,'.//div[@data-test="employerName"]').text
                    location = driver.find_element(By.XPATH,'.//div[@data-test="location"]').text
                    job_title = driver.find_element(By.XPATH,'.//div[@data-test="jobTitle"]').text
                    job_description = driver.find_element(By.ID,'JobDescriptionContainer').text
                    collected_successfully = True
                    # print("company name_________"+company_name)
                    # print(job_title)
                    # print(job_description)
                    if driver.find_element(By.CLASS_NAME,"h3").text=="Error Loading":
                        print("error")
                        break
                except:
                    print("error 2")
                    time.sleep(5)
                    pass

            try:
                salary_estimate = driver.find_element(By.XPATH,'.//span[@class="detailSalary"]').text
                print(salary_estimate)
            except NoSuchElementException:

                salary_estimate = -1 #You need to set a "not found value. It's important."
                print("______3")
                pass

            try:
                rating = driver.find_element(By.XPATH,'.//span[@class="rating"]').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."
                pass

            # Printing for debugging
            #if verbose:
            print("Job Title: {}".format(job_title))
            print("Salary Estimate: {}".format(salary_estimate))
            print("Job Description: {}\n".format(job_description))
            print("Rating: {}\n".format(rating))
            print("Company Name: {}".format(company_name))
            print("Location: {}".format(location))

            # Going to the Company tab...
            # clicking on this:
            # Company

            try:
                driver.find_element(By.XPATH,'.//div[@class="tab" and @data-tab-type="overview"]').click()

                try:
                    #

                    #    Headquarters
                    #    San Francisco, CA
                    #

                    headquarters = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                except NoSuchElementException:
                    headquarters = -1
                    print("error 4")

                try:
                    size = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1
                    print("error 5")

                try:
                    founded = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1
                    print("error 6")

                try:
                    type_of_ownership = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1
                    print("error 7")

                try:
                    industry = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1

                try:
                    sector = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1

                try:
                    revenue = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1

                try:
                    competitors = driver.find_element(By.XPATH,'.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                except NoSuchElementException:
                    competitors = -1

            except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                headquarters = -1
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1


            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            "Competitors" : competitors})
            # #add job to jobs

        #Clicking on the "next page" button
        try:
            driver.find_element(By.XPATH,'.//li[@class="next"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)