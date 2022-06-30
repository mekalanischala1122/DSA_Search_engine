import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

whole_site_temp1 = "https://www.codechef.com/practice?page="
whole_site_temp2 = "&limit=20&sort_by=difficulty_rating&sort_order=asc&search=&start_rating=0&end_rating=5000&topic=&tags=&group=all"
all_pages = []
# total number of pages = 176
for i in range(176):
    all_pages.append(whole_site_temp1+str(i)+whole_site_temp2)

all_questions = []
all_titles = []
for page in all_pages:
    driver.get(page)
    time.sleep(6)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    question_set = soup.findAll("a", {"class": "PracticePage_m-link__xLfvv"})
    for q in question_set:
        all_questions.append(q['href'])
        all_titles.append(q.getText())

if not os.path.exists("./Problems/"):
        os.mkdir("./Problems")
with open("./Problems/Problem_urls.txt", "w+") as f:
    for item in all_questions:
        f.write(item+"\n")
with open("./Problems/Problem_titles.txt", "w+") as f:
    for item in all_titles:
        f.write(item+"\n")