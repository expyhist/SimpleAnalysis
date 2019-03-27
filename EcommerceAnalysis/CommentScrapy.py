# -*- coding=gb18030 -*-
import requests
import json,re,pprint,time
import pandas as pd
from datetime import datetime

def jdsku():
    df = pd.read_csv('C:/Users/Administrator.PC-20160914KUGY/Desktop/jdsku.csv')
    sku = list(df['SKU'])
    return sku
'''jdsku是为了调用csv'''
def get_maxpages(sku):
    maxpages = []
    new_sku = []
    headers = {'authority': 'sclub.jd.com',
               'method': 'GET',
               'path': '/comment/productPageComments.action?callback=fetchJSON_comment98vv338&productId=3750799&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1',
               'scheme': 'https',
               'referer': 'https://item.jd.com/3750799.html',
               'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url = 'https://sclub.jd.com/comment/productPageComments.action'
    s = requests.session()
    for id in sku:
        params = {'callback': 'fetchJSON_comment98vv338',
                 'productId': id,
                 'score': '1',
                 'sortType': '5',
                 'page': '0',
                 'pageSize': '100',
                 'isShadowSku': '0',
                 'fold': '1'}
        r = s.get(url, headers=headers, params=params).text
        json_comments = json.loads(r[len('fetchJSON_comment98vv338('):-2])
        pages = json_comments['maxPage']
        if pages == 0:
            continue
        else:
            new_sku.append(id)
            maxpages.append(pages)

    return maxpages ,new_sku
'''get_maxpages是为了获取评论的最大页数，为了构建params做准备'''
def make_params(new_sku,maxpage):
    params_list = []
    for id,i in zip(new_sku,range(len(new_sku))):
        for maxpage in range(maxpages[i]):
            params = {'callback':'fetchJSON_comment98vv338',
                     'productId':id,
                     'score':'1',
                     'sortType':'5',
                     'page':maxpage,
                     'pageSize':'10',
                     'isShadowSku':'0',
                     'fold':'1'}
            params_list.append(params)
    return params_list
'''make_params是为了抓取SKU评论而构建的参数'''
def get_comments(params_list):
    referenceId = []
    content = []
    creationTime = []
    productColor = []
    productSize = []
    nickname = []
    userClientShow = []
    userLevelName = []

    headers = {'authority':'sclub.jd.com',
               'method':'GET',
               'path':'/comment/productPageComments.action?callback=fetchJSON_comment98vv338&productId=3750799&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1',
               'scheme':'https',
               'referer':'https://item.jd.com/3750799.html',
               'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url = 'https://sclub.jd.com/comment/productPageComments.action'
    s = requests.session()
    date_Threshold = datetime(2017, 1, 1, 00, 00)
    for param in params_list:
        try:
            r = s.get(url,headers=headers,params=param).text
            json_comments = json.loads(r[len('fetchJSON_comment98vv338('):-2])
            # print(json_comments)
            for i in range(len(json_comments['comments'])):
                date_check = json_comments['comments'][i]['creationTime']
                if datetime.strptime(date_check,'%Y-%m-%d %H:%M:%S') > date_Threshold:
                    referenceId.append(json_comments['comments'][i]['referenceId'])
                    content.append(json_comments['comments'][i]['content'])
                    creationTime.append(json_comments['comments'][i]['creationTime'])
                    productColor.append(json_comments['comments'][i]['productColor'])
                    productSize.append(json_comments['comments'][i]['productSize'])
                    nickname.append(json_comments['comments'][i]['nickname'])
                    userClientShow.append(json_comments['comments'][i]['userClientShow'])
                    userLevelName.append(json_comments['comments'][i]['userLevelName'])
                    print('成功获取第'+str(i)+'份评论数据')
                    save_comments(referenceId, content, creationTime, productColor, productSize, nickname,userClientShow, userLevelName)

        except Exception as e:
            print(e)
            break

    return
'''get_conmments将评论相关特征存储到list，然后用pd.to_cvs完成数据的储存'''
def save_comments(referenceId,content,creationTime,productColor,productSize,nickname,userClientShow,userLevelName):
    df = pd.DataFrame({'referenceId':referenceId,
                       'content':content,
                       'creationTime':creationTime,
                       'productColor':productColor,
                       'productSize':productSize,
                       'nickname':nickname,
                       'userClientShow':userClientShow,
                       'userLevelName':userLevelName
                       })
    df.to_csv('comment.csv',index=False,sep=',')

if __name__ == '__main__':
    sku = jdsku()
    maxpages,new_sku = get_maxpages(sku)
    params_list = get_params(new_sku,maxpages)
    get_comments(params_list)
