from urllib.request import urlopen
from bs4 import BeautifulSoup

list_user = []

for userID in range(1, 100000):
    link = "https://vozforums.com/member.php?u=" + str(userID)
    html = urlopen(link)
    bsObj = BeautifulSoup(html, "lxml")
    user_name = bsObj.find("div", {"id":"main_userinfo"}).h1.get_text()
    list_user.append(user_name)
    print("username", userID, "is: ", user_name)
    with open("voz.txt", "a") as myfile:
        myfile.write(user_name)
~
