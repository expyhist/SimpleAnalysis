#-*- coding:utf-8 -*-
import requests,xlwt,re,time
from lxml import etree

result1_1 = []#工作名称
result2_1 = []#公司名称
result3_1 = []#公司性质
result4_1 = []#公司规模
result5_1 = []#所属行业
result6_1 = []#所在城市
result7_1 = []#薪水
result8_1 = []#经验
result9_1 = []#教育背景
result10_1 = []#招聘人数
result11_1 = []#职位类型
result12_1 = []#待遇

#获取51job的html
def get_html(url):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    req = requests.get(url,headers = header,timeout = 30)
    html = req.content.decode('gb18030','ignorehtml')
    return html
#获取50个左右不同职业的html
def get_each_html(html):
    html_xpath = etree.HTML(html)
    each_job_url = html_xpath.xpath('//div[@class="dw_table"]/div/p/span/a/@href')
    for i in each_job_url:
        htmls = get_html(i)
        get_content(htmls)
#解析html，然后写入excel
def get_content(htmls):
    htmls_xpath = etree.HTML(htmls)
    result1 = htmls_xpath.xpath('//div[@class="cn"]/h1/@title')
    result2 = htmls_xpath.xpath('//div[@class="cn"]/p/a/@title')
    result3 = re.compile(r'\r\n\t\t\t\t(.*?)    \t\t    \t\t\t').findall(htmls)
    result4 = re.compile(r'&nbsp;&nbsp;(.*?)    \t\t    \t\t    \t\t\t').findall(htmls)
    result5 = re.compile(r'<p[^<>]+>\s+.*?\s[^<>]*&nbsp;&nbsp;(.*?)\s').findall(htmls)
    result6 = re.compile(r'<span class="lname">(.*?)</span>').findall(htmls)
    result7 = re.compile(r'<div class="cn">.*?<strong>(.*?)</strong>', re.S).findall(htmls)
    result8 = re.compile(r'<span class="sp4"><em class="i1"></em>(.*?)</span>', re.S).findall(htmls)
    result9 = re.compile(r'<em class="i2"></em>(.*?)</span>', re.S).findall(htmls)
    result10 = re.compile(r'<em class="i3"></em>(.*?)</span>').findall(htmls)
    result11 = re.compile(r'<div[^<>]+>\s+<p[^<>]+>\s+<span[^<>]+>.*\s+<span[^<>]+>(.*)</span>').findall(htmls)
    result12 = htmls_xpath.xpath('//p[@class="t2"]/span/text()')

    result1_1.append(result1)
    result2_1.append(result2)
    result3_1.append(result3)
    result4_1.append(result4)
    result5_1.append(result5)
    result6_1.append(result6)
    result7_1.append(result7)
    result8_1.append(result8)
    result9_1.append(result9)
    result10_1.append(result10)
    result11_1.append(result11)
    result12_1.append(result12)

    book = xlwt.Workbook()
    sheet = book.add_sheet('Sheet', cell_overwrite_ok=True)
    sheet.write(0, 0, 'work_name')
    sheet.write(0, 1, 'company_name')
    sheet.write(0, 2, 'company_character')
    sheet.write(0, 3, 'company_size')
    sheet.write(0, 4, 'industry')
    sheet.write(0, 5, 'city')
    sheet.write(0, 6, 'salary')
    sheet.write(0, 7, 'exp')
    sheet.write(0, 8, 'edu')
    sheet.write(0, 9, 'recruitment')
    sheet.write(0, 10, 'category')
    sheet.write(0, 11, 'treatment')
    #表头
    a = 0
    for k in range(0, len(result1_1)):
        sheet.write(k + 1, a, result1_1[k])
        sheet.write(k + 1, a + 1, result2_1[k])
        sheet.write(k + 1, a + 2, result3_1[k])
        sheet.write(k + 1, a + 3, result4_1[k])
        sheet.write(k + 1, a + 4, result5_1[k])
        sheet.write(k + 1, a + 5, result6_1[k])
        sheet.write(k + 1, a + 6, result7_1[k])
        sheet.write(k + 1, a + 7, result8_1[k])
        sheet.write(k + 1, a + 8, result9_1[k])
        sheet.write(k + 1, a + 9, result10_1[k])
        sheet.write(k + 1, a + 10, result11_1[k])
        sheet.write(k + 1, a + 11, str(result12_1[k]))
    #内容
    book.save('E:\\51job_detail_4.xls')
#主函数
def main():
    for page in range(1,13):
        print("正在爬取第" + str(page) + "页")
        print("start tiem:%s:" % time.ctime())
        url = 'http://search.51job.com/list/180200%252C200200%252C070200%252C090200%252C060000,000000,0000,00,2,99,%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590,2,'+str(page)+'.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
        html = get_html(url)
        get_each_html(html)
        print("stop tiem:%s:" % time.ctime())

if __name__ == '__main__':
    main()