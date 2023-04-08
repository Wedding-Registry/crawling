import math
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/search', methods=['POST'])
def crawling():  # put application's code here
    # url 추출
    body = request.get_json()
    url = body["url"]

    # url 호출
    try:
        req = Request(url)
        web_page = urlopen(req)
        soup = BeautifulSoup(web_page, "html.parser")

        name = soup.find("fieldset", "_10hph879os").find("h3", "_22kNQuEXmb").text

        moneys_element = soup.findAll("span", "_1LY7DqCnwR")
        money = math.inf
        for money_element in moneys_element:
            money_text = money_element.text
            money_text_replace = money_text.replace(",", "")
            money = min(money, int(money_text_replace))

        image = soup.find("div", "_2tT_gkmAOr").find("img")['src']

        response = {"status": 200, "goodsName": name, "goodsPrice": money, "goodsImgUrl": image}

        return jsonify(response)

    except:
        return jsonify({"status": 500, "goodsName": None, "goodsPrice": None, "goodsImgUrl": None})


if __name__ == '__main__':
    app.run()
