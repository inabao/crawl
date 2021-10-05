# -*- coding = utf-8 -*-
# @Time: 2021/10/3 15:10
# @Author: ZY Lin
# @File: spider.py
# @Software: PyCharm

from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import xlwt

def main():
    baseurl = "http://www.zhongyaocai360.com/a/alihong.html#6091"
    savepath = "中医药.xls"
    #(1)获取数据
    datalist = getData(baseurl)
    #print(datalist)

    #(3)保存数据
    saveData(datalist,savepath)


#分别对应'药名','出处','拼音','别名','来源','原形态','性味','功能主治'...
findName = re.compile(r'<dd><a.*中的(.*?)">')
findProvenance = re.compile(r'<p>【出处】(.*?)</p>')
findSpell = re.compile(r'<p>【拼音名】(.*?)</p>',re.S)
findAlias = re.compile(r'<p>【别名】(.*?)</p>')
findSource = re.compile(r'<p>【来源】(.*?)</p>')
findForm = re.compile(r'<p>【原形态】(.*?)</p>')
findProperty = re.compile(r'<p>【性味】(.*?)</p>')
findFunction = re.compile(r'<p class="zz">.*【功能主治】</a>(.*?)</p>')
pre = re.compile(r'<[^>]+>',re.S)

#过滤字符串s中的html标签
def filter(s):
    t = pre.sub('',s)
    return t

#获取并且解析数据
def getData(baseurl):
    datalist = []

    html = askUrl(baseurl)
    soup = BeautifulSoup(html,"html.parser")
    #查找符合要求的字符串
    for item in soup.find_all('div',class_ = "spider"):
        #print(item)
        data = []
        item = str(item)

        name = re.findall(findName, item)[0]
        data.append(name)

        provenance = re.findall(findProvenance,item)[0]
        data.append(provenance)
        spell = re.findall(findSpell,item)[0]
        data.append(spell)
        alias = re.findall(findAlias, item)[0]
        data.append(alias)
        source = re.findall(findSource, item)[0]
        data.append(filter(source))
        form = re.findall(findForm, item)[0]
        data.append(filter(form))
        property = re.findall(findProperty, item)[0]
        data.append(filter(property))
        function = re.findall(findFunction,item)[0]
        data.append(filter(function))

        datalist.append(data)


    return datalist

#得到一个指定URL的网页内容
def askUrl(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
    }
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("gb18030")
        #print(html)
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html



#数据保存到excel中
def saveData(datalist,savepath):
    workbook = xlwt.Workbook(encoding="utf-8",style_compression=0)
    worksheet = workbook.add_sheet('中医药大辞典',cell_overwrite_ok=True)
    col = ('药名','出处','拼音','别名','来源','原形态','性味','功能主治')
    for i in range(0,8):
        worksheet.write(0,i,col[i])
    num = len(datalist)
    for i in range(0,num):
        data = datalist[i]
        for j in range(0,8):
            worksheet.write(i+1,j,data[j])
    print('success')
    workbook.save(savepath)





if __name__ == "__main__":
    main()