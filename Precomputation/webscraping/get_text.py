import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

with open("./Problems/Problem_urls.txt", "r") as f:
    all_urls = f.read()
    urls = all_urls.split()

k = 1

for url in urls:
    print("Working on ", k, "out of", len(urls))
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    q_text = soup.find("div", {"class": "MarkdownPreview_problemBody__3im1P"})
    second_X = soup.select(selector="math")
    for elem in second_X:
        elem.decompose()

    final_text = q_text.get_text()
    # to remove contents after the "Constraints" Section of CodeChef
    if not os.path.exists("./Problems/Problem_texts/"):
        os.mkdir("./Problems/Problem_texts")
    with open("./Problems/Problem_texts/problem_text"+str(k)+".txt", "w+", encoding="utf-8") as f:
        f.write(final_text)
        f.close()
    k += 1
