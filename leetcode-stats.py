#!/usr/bin/env python
""" An simple script to retrieve stats from LeetCode OJ.
"""
from __future__ import print_function, division
import sys
import os

try:
    import selenium
except ImportError:
    selenium = None
    print("selenium not found. Please run 'pip install selenium'.")
    sys.exit(1)

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import Select
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

try:
    import pandas as pd
except ImportError:
    print("pandas not found. Please run 'pip install pandas'.")
    sys.exit(1)


if __name__ == '__main__':

    try:
        browser = webdriver.PhantomJS(service_log_path=os.path.devnull)
        # browser = webdriver.Chrome(service_log_path=os.path.devnull)
    except WebDriverException as err:
        print("PhantomJS", err)
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(description="extract algorithm stats from LeetCode OJ.")
    parser.add_argument('-u', '--username', required=True, help="website username")
    parser.add_argument('-p', '--password', required=True, help="website password")
    parser.add_argument('-o', '--out', default=None, help="dump problems in a csv file")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # login
    browser.get("https://leetcode.com/accounts/login/")

    try:
        user_name = WebDriverWait(browser, 10).until(
            ec.presence_of_element_located((By.ID, "id_login"))
        )
        user_name.clear()
        user_name.send_keys(args.username)
    except TimeoutException as err:
        print("Network", err)
        sys.exit(1)

    password = browser.find_element_by_id('id_password')
    password.clear()
    password.send_keys(args.password)
    try:
        element_login_form = \
            browser.find_element_by_xpath("//form[@class='form-signin']")
        element_login_form.submit()
    except NoSuchElementException:
        print("Cannot find login form element.")
        sys.exit()

    try:
        browser.get("https://leetcode.com/problemset/all/");
        element_rowsperpage = WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.XPATH, "//span[@class='row-selector']/select[@class='form-control']"))
        )
    except TimeoutException as err:
        print("Network", err)
        sys.exit(1)

    # show all table entries
    try:
        rowsperpage_select = Select(element_rowsperpage)
        rowsperpage_select.select_by_visible_text('all')
    except NoSuchElementException:
        print("Cannot find rows/page select element.")
        sys.exit()

    # extract table contents
    try:
        element_problem_table = WebDriverWait(browser, 5).until(
            ec.presence_of_element_located((By.XPATH, "//tbody[@class='reactable-data']"))
        )
    except TimeoutException as err:
        print("Network", err)
        sys.exit(1)

    element_problem_table_rows = element_problem_table.find_elements_by_tag_name("tr")  # type: list[WebElement]

    problem_list = []
    for row in element_problem_table_rows:
        element_entry_cells = row.find_elements_by_tag_name("td")  # type: list[WebElement]
        problem_list.append(
            (
                1 if element_entry_cells[0].get_attribute("value") == "ac" else 0,
                int(element_entry_cells[1].text),
                element_entry_cells[2].get_attribute("value"),
                element_entry_cells[5].text
            )
        )

    browser.close()

    dataframe = pd.DataFrame.from_records(problem_list, index="ID", columns=['solved', 'ID', 'problem', 'difficulty'])

    if args.out:
        dataframe.to_csv(args.out)

    print("Total problems", dataframe.shape[0])
    print("--------------")
    print("Easy   problems solved:", dataframe[(dataframe.difficulty == "Easy") & (dataframe.solved == 1)].shape[0],
          '/', dataframe[dataframe.difficulty == "Easy"].shape[0])
    print("Medium problems solved:", dataframe[(dataframe.difficulty == "Medium") & (dataframe.solved == 1)].shape[0],
          '/', dataframe[dataframe.difficulty == "Medium"].shape[0])
    print("Hard   problems solved:", dataframe[(dataframe.difficulty == "Hard") & (dataframe.solved == 1)].shape[0],
          '/', dataframe[dataframe.difficulty == "Hard"].shape[0])
    print("--------------")
