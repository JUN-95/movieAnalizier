import json

from flask import Flask, redirect, render_template, url_for, request, flash
from sqlalchemy import create_engine
import pymysql

app = Flask(__name__)

con = create_engine("mysql+pymysql://root:123456@localhost/movie?charset=utf8mb4").connect()
print("connect success!!!!")


@app.route("/movie")
def opinion():
    return render_template("dataVisiable.html")


@app.route("/zhuyan", methods=["GET", "POST"])
def sex():
    res = con.execute("select * from zyDicToDF limit 6")

    sex_name = []
    num = []
    res_dic = {}  # 初始化字典
    for i in res:
        sex_name.append(i[0])
        num.append(i[1])

    res_dic["sex"] = sex_name
    res_dic["num"] = num

    return res_dic



@app.route("/sortedTypeClassify", methods=["POST", "GET"])
def certification():
    res = con.execute("select * from (select * from sortedTypeClassifyToDF order by groupTypeNum desc limit 10) as b")

    cert_res = []
    cert_num = []
    cert_res_dict = {}

    for i in res:
        cert_res.append(i[0])
        cert_num.append(i[1])

    cert_res_dict["cert_res"] = cert_res
    cert_res_dict["cert_num"] = cert_num

    return cert_res_dict


@app.route("/groupByScore", methods=["GET", "POST"])
def hotSpot():

    res = con.execute("select * from (select * from groupbyscoretodf order by groupScoreNum desc limit 20) as b order by groupScoreNum asc")
    score = []
    score_num = []
    score_dict = {}

    for i in res:
        score.append(i[0])
        score_num.append(i[1])

    score_dict["score"] = score
    score_dict["score_num"] = score_num

    return score_dict


@app.route("/daoyan", methods=["GET", "POST"])
def tool():
    res = con.execute("select * from dyDicToDF limit 40")

    tool_name = []
    tool_num = []
    tool_dict = {}

    for i in res:
        tool_name.append(i[0])
        tool_num.append(i[1])

    tool_dict["tool_name"] = tool_name
    tool_dict["tool_num"] = tool_num

    return tool_dict


@app.route("/groupByCountry", methods=["GET", "POST"])
def city():
    res = con.execute("select * from groupByCountryToDF limit 10")
    city_name = []
    city_num = []
    city_dict = {}

    for i in res:
        city_name.append(i[0])
        city_num.append(i[1])

    city_dict["city_name"] = city_name
    city_dict["city_num"] = city_num

    return city_dict


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)


# print(gender())
