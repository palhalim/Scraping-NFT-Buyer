'''
Scraping by @paltoonMy on twitter, pls donate for continuous maintenance of this repository.
'''
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
from selenium.webdriver.chrome.options import Options
# import requests

##### Web scrapper for infinite scrolling page #####


options = Options()
options.add_argument("window-size=1920,1080")
options.headless = True
# options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome(executable_path=r"C:\chromedriver.exe", options=options ) #! download chromedriver similar version to your chrome version >> https://chromedriver.chromium.org/ options=options
driver.get("https://app.pentas.io/user/0xc1B8914212a85EB45Bae15E5C7435d66F2A60FBA") #! <<< pentas acc link here - click sold tab first
time.sleep(2)  # Allow 2 seconds for the web page to open
scroll_pause_time = 5#60 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break 

##### Extract Reddit URLs #####
urls = []
nfts = []
users = []
twts = []
names = []
wallets = []
soup = BeautifulSoup(driver.page_source, "html.parser")
for parent in soup.find_all(class_="relative bg-white dark:bg-darkBg2 sm:rounded-xl shadow border-t border-b sm:border border-white dark:border-darkBg3 overflow-hidden mx-auto sm:max-w-xl"):

    #get holder pentas acc link and name
    a_tag = parent.find("a", class_="absolute inset-0 focus:outline-none")
    userlink = parent.find("a", class_="group block mt-4")
    link = userlink.attrs['href']

    name = parent.find("p", class_="block text-lg text-textPrimary dark:text-dmTextPrimary truncate pointer-events-none")
    name = name.get_text()

    #get nft name and link
    user = parent.find_all("p", class_="text-sm text-textPrimary dark:text-dmTextPrimary line-clamp-1 break-all")
    user = user[1].get_text()
    
    nft = a_tag.attrs['href']

    base = "https://app.pentas.io/"
    
    
    link = urljoin(base, link)
    nft = urljoin(base, nft)
    w = link[-42:]

    nfts.append(nft)
    users.append(user)
    urls.append(link)
    names.append(name)
    wallets.append(w)
    print(users)

#get twitter from user pentas acc link
for i in urls:  
    # print(i)
    
    # ext_page = requests.get(i)
    # print(ext_page)
    driver.get(i)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # r = requests.get(i)
    # time.sleep(5)
    # html = r.page_source
    # soup = BeautifulSoup(r.page_source, "html.parser")
    twitter = soup.find("a", class_="ml-2 hover:underline", target="_blank")
    twt_alt = soup.find("a", class_="ml-2 hover:underline w-11/12", target="_blank")
    print(twitter)
    if twitter:
        twitter = twitter.attrs['href']
    elif twt_alt:
        twitter = twt_alt.attrs['href']
    else:
        twitter = "-" #not linked to twitter
    print(twitter)
    twts.append(twitter)

print(wallets)
# print(urls)
# print(twts)


# save all to csv files
demo = pd.DataFrame({"Nft name / no":names, "ID": nfts, "User pentas":urls, "Wallet address":wallets, "Username":users, "Twt":twts})
demo.to_csv('Owner_list.csv', index=False, encoding='utf-8', mode = 'a')
