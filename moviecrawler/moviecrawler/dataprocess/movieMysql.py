import pymysql
from sqlalchemy import create_engine
import pandas as pd

conn = create_engine("mysql+pymysql://root:123456@localhost/movie").connect()
tableData = pd.read_sql_table("movie2", conn)

dropIdData = tableData.drop(columns="id")  # id会影响处理后的表结构，所以可以去掉id
dropIdData.drop_duplicates(inplace=True)   # 去重
dropIdData.dropna(inplace=True)  # 去空

# 对分数进行分组，统计各个分数的电影数， 折线图
groupByScore = dropIdData.groupby(by="score", sort=True)   # 对分数进行分组
gbsList = []
for g in groupByScore:
    gbsList.append((g[0], len(g[1])))  # (每个分数  ,每个分数的数量)
groupByScoreToDF = pd.DataFrame.from_records(gbsList, columns=["scoreClassify", "groupScoreNum"]).sort_values(
    "groupScoreNum", ascending=True, inplace=False)
groupByScoreToDF.to_sql(name="groupByScoreToDF", index=False, con=conn, if_exists="replace")

# 按照国家进行分类，对电影国家的数量进行排序， 饼图
groupByCountry = dropIdData.groupby(by="country", sort=False)   # 对国家进行分组
gbcList = []
for g in groupByCountry:
    gbcList.append((g[0], len(g[1])))  # (每个国家  ,每个国家的数量)
groupByCountryToDF = pd.DataFrame.from_records(gbcList, columns=["countryClassify", "groupCountryNum"]).sort_values(
    "groupCountryNum", ascending=False, inplace=False)
groupByCountryToDF.to_sql(name="groupByCountryToDF", index=False, con=conn, if_exists="replace")

# 对分数排名前15的电影进行排序，柱状图
topScoreList = []
topScore = dropIdData.sort_values("score", ascending=False, inplace=False).head(15)
movieName = topScore["movieName"]
for t, m in zip(topScore["score"], movieName):
    topScoreTuple = (m, t)
    topScoreList.append(topScoreTuple)

topScoreListToDF = pd.DataFrame.from_records(topScoreList, columns=["movieName", "score"]).sort_values(
    "score", ascending=False, inplace=False)
topScoreListToDF.to_sql(name="topScoreListToDF", index=False, con=conn, if_exists="replace")


# 分数大于8.5的导演的分组统计数量
# dyDic = {}
# for d in daoyan:
#     ds = d.split(",")
#     for dd in ds:
#         dds = dd.strip()
#         if dds not in dyDic.keys() and (dds is not None):
#             dyDic[dds] = 1
#         elif dds is not None:
#             dyValue = dyDic[dds]
#             dyDic[dds] = dyValue + 1
#
# sorteddyDic = sorted(dyDic.items(), key=lambda x: x[1], reverse=True)   # 会自动将dict转化为list
# dyDicToDF = pd.DataFrame.from_records(sorteddyDic, columns=["daoyanClassify", "groupdaoyanNum"])
# dyDicToDF.to_sql(name="dyDicToDF", index=False, con=conn, if_exists="replace")



# 分数大于8.5的主演的分组统计数量
# zyDic = {}
# for z in zhuyan:
#     zs = z.split(",")
#     for zz in zs:
#         zzs = zz.strip()
#         if zzs not in zyDic.keys() and (zzs is not None):
#             zyDic[zzs] = 1
#         elif zzs is not None:
#             zyValue = zyDic[zzs]
#             zyDic[zzs] = zyValue + 1
#
# sortedzyDic = sorted(zyDic.items(), key=lambda x: x[1], reverse=True)  # 会自动将dict转化为list
# zyDicToDF = pd.DataFrame.from_records(sortedzyDic, columns=["zhuyanClassify", "groupzhuyanNum"])
# zyDicToDF.to_sql(name="zyDicToDF", index=False, con=conn, if_exists="replace")

# typeClassifyDic = {}
# for d in dropIdData["type"]:
#     types = d.split("/")
#     for t in types:
#         ts = t.strip()
#         if ts not in typeClassifyDic.keys() and (ts is not None):
#             typeClassifyDic[ts] = 1
#         elif ts is not None:
#             tsValue = typeClassifyDic[ts]
#             typeClassifyDic[ts] = tsValue + 1
#
# sortedTypeClassifyDic = sorted(typeClassifyDic.items(), key=lambda x: x[1], reverse=True)
#
# sortedTypeClassifyDicToDF = pd.DataFrame.from_records(sortedTypeClassifyDic, columns=["typeClassify", "groupTypeNum"])
# sortedTypeClassifyDicToDF.to_sql(name="sortedTypeClassifyToDF", index=False, con=conn, if_exists="replace")


# 获取电影评分大于8.5分的导演和主演
# scoreFilter = [d for d in dropIdData["score"] if float(d) >= 8.5]
scoreFilter = dropIdData[dropIdData["score"].apply(lambda x: float(x)) >= 8.5]  # 选出分数大于等于8.5的行
daoyan = scoreFilter["daoyan"]  # 对分数进行过滤后重新得到导演
zhuyan = scoreFilter["zhuyan"]  # 对分数进行过滤后重新得到主演


# 创建封装重复代码的函数
def scoreLimit(dicItem, splitBy, colName1, colName2, tableName):
    dic = {}
    for d in dicItem:
        ds = d.split(splitBy)
        for dd in ds:
            dds = dd.strip()
            if dds not in dic.keys() and (dds is not None):
                dic[dds] = 1
            elif dds is not None:
                dValue = dic[dds]
                dic[dds] = dValue + 1   # 统计值

    sorteddDic = sorted(dic.items(), key=lambda x: x[1], reverse=True)  # 会自动将dict转化为list
    dDicToDF = pd.DataFrame.from_records(sorteddDic, columns=[colName1, colName2])
    dDicToDF.to_sql(name=tableName, index=False, con=conn, if_exists="replace")

# 分数大于8.5的导演的分组统计数量
scoreLimit(daoyan, ",", "daoyanClassify", "groupdaoyanNum", "dyDicToDF")

# 分数大于8.5的主演的分组统计数量
scoreLimit(zhuyan, ",", "zhuyanClassify", "groupzhuyanNum", "zyDicToDF")

# 对电影类型进行分类，柱状图
scoreLimit(dropIdData["type"], "/", "typeClassify", "groupTypeNum", "sortedTypeClassifyToDF")
