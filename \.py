# -*- coding: utf-8 -*-

# coding: utf-8

import bs4
from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt
import sqlite3
import pymysql



#
findnum = re.compile(r'点击数：(.*?) ')
findtype = re.compile(r'<strong>(.*?)</strong>')
findpic=re.compile(r'href="(.*?)"')
findtime=re.compile(r'录入时间：(.*?) ')# 创建正则表达式对象，标售规则   影片详情链接的规则
#findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
#findTitle = re.compile(r'<span class="title">(.*)</span>')
# findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# findJudge = re.compile(r'<span>(\d*)人评价</span>')
# findInq = re.compile(r'<span class="inq">(.*)</span>')
# findBd = re.compile(r'<p class="">(.*?)</p>', re.S)




def main():
    baseurl = "http://www.gzmdxzulin.com/ProductShow.asp?ID="  #要爬取的网页链接
    # 1.爬取网页
    datalist = getData(baseurl)
    savepath = "服装信息.xls"    #当前目录新建XLS，存储进去
         #当前目录新建数据库，存储进去
    # 3.保存数据
    #saveData(datalist,savepath)      #2种存储方式可以只选择一种
    saveDataDB(datalist)
    #askURL("http://www.gzmdxzulin.com/ProductShow.asp?ID=1000")



# 爬取网页
def getData(baseurl):
    datalist = []  #用来存储爬取的网页信息
    for i in range(900, 1100):  # 调用获取页面信息的函数，10次   200-1145
        url = baseurl + str(i)
        html = askURL(url)  # 保存获取到的网页源码
        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('table', width="100%", border="0", cellspacing="0", cellpadding="0"):  # 查找符合要求的字符串
            #print(item)
            data = []  # 保存一件服装所有信息
            item = str(item)

            name = re.findall(findtype, item)[1]  # 名称
            data.append(name)

            type = re.findall(findtype, item)[4]  # 服装类型
            data.append(type)

            pic = re.findall(findpic, item)[1]  # 图片
            data.append(pic)

            num = re.findall(findnum, item)[0] #点击量
            data.append(num)

            time = re.findall(findtime, item)[0]  # 点击量
            data.append(time)

            #print(num)
            datalist.append(data)
    return datalist


# 得到指定一个URL的网页内容
def askURL(url):
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("gb18030")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    return html


# # 保存数据到表格
# def saveData(datalist,savepath):
#     print("save.......")
#     book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
#     sheet = book.add_sheet('服装信息', cell_overwrite_ok=True) #创建工作表
#     col = ("服装名称","服装类型","图片地址","点击量","发布时间")
#     for i in range(0,5):
#         sheet.write(0,i,col[i])  #列名
#     for i in range(0,10):
#         #print("第%d条" %(i+1))
#         data = datalist[i]
#         for j in range(0,5):
#             sheet.write(i+1,j,data[j])  #数据
#     book.save(savepath) #保存


# 保存数据到数据库
def saveDataDB(datalist):
    conn = pymysql.connect(host='127.0.0.1',user= 'root',password= 'root', db='clothing',charset='utf8')
    cur = conn.cursor()
    for data in datalist:
            for index in range(len(data)):
                #if index == 4:
                    #continue
                data[index] = '"'+data[index]+'"'
            sql = '''
                    insert into clothspider(
                    name,type,pic_link,num,time)
                    values (%s)'''%",".join(data)
            print(sql)     #输出查询语句，用来测试
            cur.execute(sql)
            conn.commit()
    cur.close
    conn.close()


if __name__=="__main__":
    main();
    print("1");