from datetime import datetime
from instabot import Bot
from selenium import webdriver
import time

Data = []


def create_txt():
    users = [a["user"]["username"] for a in comentarios]
    users_unic = sorted([{a: users.count(a)} for a in set(users)], key=lambda i: i[[*i.keys()][0]])
    for user in users_unic:
        Data.append(str(user.keys()).replace('dict_keys([', '').replace('])', '').replace("'", ""))

    textos = [comentario['text'] for comentario in comentarios]
    users_marcados = []
    for texto in textos:
        users_marcados += [a for a in texto.replace("\n", "").split(" ") if "@" in a and 3 <= len(a) <= 25]
    for user_marcado in users_marcados[:]:
        Data.append(user_marcado.replace('@', '').replace(',', ''))

    for i in range(len(likes)):
        name = bot.get_user_info(likes[i])
        Data.append(name['username'])


def get_posts(link):
    driver = webdriver.Chrome()
    driver.get(link)
    posts = []

    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); "
                                      "var lenOfPage = document.body.scrollHeight;"
                                      "return lenOfPage; ")

    links = driver.find_elements_by_tag_name('a')

    for link in links:
        post = link.get_attribute('href')
        if '/p/' in post:
            posts.append(post)

    match = False
    while not match:
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight); "
                                          "var lenOfPage = document.body.scrollHeight;"
                                          "return lenOfPage; ")
        if lastCount == lenOfPage:
            match = True

    links = driver.find_elements_by_tag_name('a')

    for link in links:
        post = link.get_attribute('href')
        if '/p/' in post:
            posts.append(post)

    driver.close()
    return posts


bot = Bot()
username = input("Enter username: ")
password = input("Enter Password: ")
url = input("Enter the link to the profile: ")
post = get_posts(url)
post = list(dict.fromkeys(post))

for i in range(len(post)):
    bot.login(username=username, password=password, ask_for_code=True)
    media_id = bot.get_media_id_from_link(post[i])
    comentarios = bot.get_media_comments_all(media_id)
    likes = bot.get_media_likers(media_id)
    create_txt()
    print("Number of Posts Scanned: " + str(i + 1))
    Data = list(dict.fromkeys(Data))
    print(Data)
    bot.logout()
    time.sleep(5)

fname = datetime.now().strftime('%H-%M-%S') + ".txt"
f = open(fname, "w")

for i in range(len(Data)):
    data = Data[i] + "\n"
    f.write(data)

f.close()
