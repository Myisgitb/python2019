#小说下载_2018.12.06

from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
import re,time,random

server='http://www.biqukan.com/'
target='http://www.biqukan.com/1_1094/'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.5.0.17963',
}
def Get_main_url(target):  #抓取主页分析章节
    #获取小说主页所有章节信息
    req=requests.get(url = target)#读取首页
    html=req.text #提取html
    div_bf=BeautifulSoup(html,"html.parser")
    div=div_bf.find_all('div',class_='listmain')
    a_bf=BeautifulSoup(str(div[0]),"lxml")
    a_html=a_bf.find_all('a')
    return a_html
def Filurl(a_html,starts,fils,ends):  #过滤模块
    k=0 #章节下载选择开关,0则跳过不下载，1为下载
    if starts=="":
        starts="第一章"
    if fils=="":
        fils="第"
    for each in a_html:#从列表过滤网址
        if starts in each.string:#设置条件从第一章开始
            k=1
        if k==1 and fils in each.string:
            yield each.string,server + each.get('href')
            if ends in each.string:
                break
def DownUrl(Durl):  #下载模块
    #下载,过滤内容
    #pattern=re.compile(r"(我们的目标.*m.biqukan.com)|(兄弟姐妹.*m.biqukan.com)",re.DOTALL)
    Err_l=[] #保存错误的网址列表
    while(True):
        try:
            reqn,requ = (next(Durl))
            print(reqn,"......")
            reqt = s.get(url = requ,headers=headers,timeout=0.5)
            if reqt.status_code==200:
                bf = BeautifulSoup(reqt.text,"html.parser")
                texts = bf.find_all('div', class_ = 'showtxt')
                wt=texts[0].text.replace('\xa0'*8,'\n').replace("\xa0","")
                with open(r"d:\\biqukan\\一念永恒\\"+ reqn + ".txt","a+") as fx:
                    fx.write(reqn+"\n")
                    fx.write(wt)
                print("下载成功！\n\n")
            elif reqt.status_code==503:
                Err_l.append(eval("'"+ reqn+"'"+","+"'"+requ+"'"))
                print("抓取失败，已存列表\n\n")
        except (StopIteration):
            print("循环列表完毕，退出下载循环模块!!!")
            break
        else:
            Err_l.append(eval("'"+ reqn+"'"+","+"'"+requ+"'"))
            print("链接错误，存于列表，稍后重新下载")
    return Err_l
if __name__=="__main__":
    #设置开始结束章节名字，和过滤的章节名字(如没有“第*章”字样的不抓)。
    s="第一章"
    e="第1314章"
    f=""
    Durl = Filurl(Get_main_url(target),s,f,e) #调用设置过滤函数，并获取主页信息，返回网址列表可迭代.
    EL=DownUrl(Durl) #一切就绪，开始下载模块
    print("剩余%s个章节未下载成功\n"%len(EL))
    if len(EL)!=0: #第一次载失败存于列表，若为空下面不继续。否则循环这个列表直到载成功.
        def rget(EL): #成生一个可迭代对像，
            for i in EL:
                yield i
        rd=rget(EL)
        while(True):
            rd=DownUrl(rd)
            print("剩余%s个章节\n"%len(rd))
            if len(rd)==0:break
            rd=rget(rd)
 
    
       
        
