from bs4 import BeautifulSoup
import json
import requests
import re

url = 'http://tjj.yantai.gov.cn/art/2021/3/4/art_11148_2876139.html'
title = '烟台市2021年01月月报----主要经济指标'
csvindex = ['date', 'primary_industry',
            'Secondary_industry', 'Tertiary_industry']

#设置爬取字段
indexlst = ['第一产业税收', '第二产业税收', '第三产业税收']


def gethtml(url):
    '''
    获取并解码相关页面
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'}
    r = requests.get(url, headers=headers)
    html_content = r.text.encode('ISO-8859-1')
    html_soup = BeautifulSoup(html_content)
    return html_soup


def get_raw_data(html_soup):
    '''
    获取相关数据，此处默认获取累计数据
    '''
    traget_table = html_soup.findAll('table')[-4]
    data = []
    names = []
    for name in traget_table.findAll('td'):
        names.append(name.text.strip())
    for i in indexlst:
        index = names.index(i)
        dataitem = names[index + 2]
        data.append(dataitem)
    return data


def csv_writer(processed_date, data, path):
    '''
    将数据写入csv文件
    '''
    with open(path, 'a') as f:
        f.write(processed_date + ',' + ','.join(data) + '\n')


def geturl(path):
    '''
    获取url，此处默认从json文件中获取
    '''
    with open(path, 'r') as f:
        urldict = json.load(f)
    return urldict


def strtodate(strdata):
    '''
    将烟台市统计局网页标题更换为标准格式
    '''
    date = re.findall('\d+', strdata)
    date = ''.join(date)
    return date


with open('2019data.csv', 'w') as f:
    f.write(','.join(csvindex) + '\n')
urldict = geturl('urldictnew.json')

for date, url in urldict.items():
    html_soup = gethtml(url)
    data = get_raw_data(html_soup)
    processed_date = strtodate(date)
    csv_writer(processed_date, data, '2019data.csv')
