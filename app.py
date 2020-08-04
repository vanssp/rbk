import requests
import ssl
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect,  url_for, flash, make_response, session

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a really really really really long secret key'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about', methods=['POST','GET'])
def about():
    url = 'http://static.feed.rbc.ru/rbc/logical/footer/news.rss'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    newStr = soup.get_text()

    bs_test = open('bs_test.txt', 'w')
    bs_test.write(newStr)
    bs_test.close()

    with open('bs_test.txt', 'r') as f:
        message_txt = f.read()

    #b = message_txt.replace("+0300",'  ')

    #print(b)

    newString = []
    j = 0
    i = 0
    lol = ''

    z = message_txt.find("+0300")  # 86
    ending = message_txt.rfind("+0300", 0, len(message_txt) - 6)  # 5500

    for j in range(len(message_txt) - 1):  # от 0 до 5900
        while i != z:  # пока 0 не равен 86
            lol = lol + message_txt[i]  # лол = пример текста 123
            i += 1

        newString.append(lol)  # newString = пример текста 123
        lol = ''  # лол = 0
        i = z + 5  # i = 91
        newPoz = z + 5  # новое начало = 91
        z = message_txt.find("+0300", newPoz, ending)  # z = найти (+0300, от 91 до 5500)
        if z == -1:
            break
    newString.pop(1)
    newString.pop(0)


    return render_template('bs_test.html', message = newString)

@app.route('/go_to_http', methods = ['POST', 'GET'])
def go_to_http():
    return render_template('http.html')

if __name__ == "__main__":
    app.run(debug=True)
