#小说下载_2018.12.06  @Nuno

from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
import re,time,random

server='http://www.biqukan.com/'
target='http://www.biqukan.com/1_1094/'
target="https://www.biqukan.com/57_57694/"
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.90 Safari/537.36 2345Explorer/9.5.0.17963',
}
def Get_www2htm(target):  #抓取主页分析章节
    Result=requests.get(url = target)#读取首页
    html=Result.text #提取html
    div_bf=BeautifulSoup(html,"html.parser")
    div=div_bf.find_all('div',class_='listmain')
    a_bf=BeautifulSoup(str(div[0]),"lxml")
    a_html=a_bf.find_all('a')
    return a_html
def Fil_htm2yie(a_html,starts,fils,ends):  #过滤模块 进htm返回yield 列表
    k=0 #章节下载选择开关,0则跳过不下载，1为下载
    if starts=="":#设置默认开始和结束章节名字，不包含"第“字样的章节不下载
        starts="第一章"
    if fils=="":
        fils="第"
    if ends=="":
        ends="第1314章"
    for each in a_html:#从列表过滤网址
        if starts in each.string:#设置条件从第一章开始
            k=1
        if k==1 and fils in each.string:
            yield each.string,server + each.get('href')
            if ends in each.string:
                break
def Down_yie2lis(Lis_yie):  #下载模块 进yield列表返回url列表
    #pattern=re.compile(r"(我们的目标.*m.biqukan.com)|(兄弟姐妹.*m.biqukan.com)",re.DOTALL)
    List_err=[] #保存错误的网址列表
    while(True):
        try:
            Result_name,Result_url = (next(Lis_yie))
            print("{\n " + Result_name)
            print(" 网页GET请求中\n  ......\n")
            time.sleep(random.randrange(0,10))
            Result = requests.get(url = Result_url,headers=headers,timeout=0.5)
            if Result.status_code==200:
                bf = BeautifulSoup(Result.text,"html.parser")
                texts = bf.find_all('div', class_ = 'showtxt')
                wt=texts[0].text.replace('\xa0'*8,'\n').replace("\xa0","")
                with open(r"d:\\biqukan\\一念永恒\\"+ Result_name + ".txt","a+") as fx:
                    fx.write(Result_name+"\n")
                    fx.write(wt)
                print(" 下载成功！！！\n}\n\n")
            elif Result.status_code==503:
                List_err.append(eval("'"+ Result_name+"'"+","+"'"+Result_url+"'"))
                print(" 抓取失败，已存列表\n}\n\n")
        except (StopIteration):
            print("\n ......下载模块网址履遍完成......\n\n")
            break
        except (requests.exceptions.ReadTimeout,requests.exceptions.ConnectionError):
            List_err.append(eval("'"+ Result_name+"'"+","+"'"+Result_url+"'"))
            print(" 请求Error！！！\n 已存列表稍后再试\n}\n\n")
    return List_err
        
if __name__=="__main__":
    #设置开始结束章节名字，和过滤的章节名字(如没有“第*章”字样的不抓)。
    s="第一章"
    e="第116章"
    f=""
    Result_Lisyie = Fil_htm2yie(Get_www2htm(target),s,f,e) #调用设置过滤函数，并获取主页信息，返回网址列表可迭代.
    Result_list = Down_yie2lis(Result_Lisyie) #一切就绪，开始下载模块
    print("  ......失败%s个......\n"%len(Result_list))
    if len(Result_list)!=0:
        def List2yie(Result_list): #成生一个可迭代对像，
            for i in Result_list:
                yield i
        Result_yie=List2yie(Result_list)
        while(True):#第一次载失败的网址列表，若为空退出。否则循环这个列表直到全部载成功.
            print("  ......下载重试中......\n\n")
            Result_yie=Down_yie2lis(Result_yie)
            print("  ......%s个章节剩余......\n"%len(Result_yie))
            if len(Result_yie)==0:break
            Result_yie=List2yie(Result_yie)
    print("  ......全部下载已完成：）：）：）......")   
        
