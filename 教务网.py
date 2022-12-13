import encodings
from os import times
from chaojiying import Chaojiying_Client
from lxml import etree
import requests
import time
import re
import json

# 通过传入的session对象，发送登录请求，并将cookie信息等保留在传入session对象中
def get_info_page(session, username, password):
    # 获取图片验证码url，并将图片储存在本地
    img_url = "http://jwc.swjtu.edu.cn/vatuu/GetRandomNumberToJPEG?"
    img_data = {
        "test": time.time()
    }
    img_heraders = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "jwc.swjtu.edu.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    }
    img_code = session.get(url=img_url, headers=img_heraders, data=img_data)
    with open("img_code.jpg", "wb")as f:
        f.write(img_code.content)
        f.close()

    # 识别图片验证码
    ID = '' #超级鹰图像识别账号
    Password = ''#超级鹰图像识别密码
    type = ''#验证码类型
    chaojiying = Chaojiying_Client('ID', 'Password.com', 'type')
    im = open('img_code.jpg', 'rb').read()
    img_code = chaojiying.PostPic(im, 1004)["pic_str"]

    # 向login_url发送登录请求
    login_data = {
        "username": username,
        "password": password,
        "url": "http: // jwc.swjtu.edu.cn/index.html?version = 2020",
        "returnType": "",
        "returnUrl": "",
        "area": "",
        "ranstring": img_code
    }
    login_url = "http://jwc.swjtu.edu.cn/vatuu/UserLoginAction"
    login_heraders = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "jwc.swjtu.edu.cn",
        "Origin": "http://jwc.swjtu.edu.cn",
        "Referer": "http://jwc.swjtu.edu.cn/vatuu/UserLoadingAction",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "X-Requested-With": "XMLHttpReques",
    }
    login_page = session.post(
        url=login_url, headers=login_heraders, data=login_data)
    login_page.encoding = "utf-8"

    # 获取登录状态码，如果登录失败终止程序，并输出提示
    login_result = json.loads(login_page.text)['loginStatus']
    if int(login_result) == -2:
        print("Verification code error! Login failed!")
        exit()

    # 向loading_url发送加载请求
    loading_url = "http://jwc.swjtu.edu.cn/vatuu/UserLoadingAction"
    loading_data = {
        "url": "http: // jwc.swjtu.edu.cn/index.html?version = 2020",
        "returnUrl": "",
        "returnType": "",
    }
    session.post(url=loading_url, headers=login_heraders, data=loading_data)

    # 通过session对象，向info_page_url发送get请求，获取个人信息页面
    info_page_url = "http://jwc.swjtu.edu.cn/vatuu/UserFramework"
    info_page_heraders = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "jwc.swjtu.edu.cn",
        "Referer": "http://jwc.swjtu.edu.cn/vatuu/UserLoadingAction",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }
    info_page = session.get(url=info_page_url, headers=info_page_heraders)
    if info_page.status_code == 200:
        print("Get info_pege sucessfully!")


# 通过session对象，访问成绩页面并将成绩保存在score.txt文件中
def get_score(session):
    # 为了不改变原session对象新建一个session1对象
    session1 = requests.session()
    session1 = session
    # 向score_url发送请求，请求成绩详情网页
    score_url = "http://jwc.swjtu.edu.cn/vatuu/StudentScoreInfoAction?setAction=studentMarkUseProgram"
    score_data = {
        "setAction": "studentMarkUseProgram"
    }
    score_hearders = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "jwc.swjtu.edu.cn",
        "Referer": "http://jwc.swjtu.edu.cn/vatuu/UserFramework",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }
    response = session1.get(
        url=score_url, headers=score_hearders, data=score_data)

    # 请求成功后向detail_score_url发请求，拿到成绩详情网页
    detail_score_url = "http://jwc.swjtu.edu.cn/vatuu/StudentScoreInfoAction?setAction=studentMarkUseProgram"
    detail_score_data = {
        "setAction": "studentScoreQuery",
        "viewType": "studentScore",
        "orderType": "submitDate",
        "orderValue": "desc"
    }
    detail_score_hearders = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9Accept-Encoding: gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Host": "jwc.swjtu.edu.cn",
        "Referer": "http://jwc.swjtu.edu.cn/vatuu/StudentScoreInfoAction?setAction=studentMarkUseProgram",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }
    detail_score_page = session.get(
        url=detail_score_url, headers=detail_score_hearders, data=detail_score_data)
    detail_score_page.encoding = "utf-8"

    # 将成绩详情网页转换为字符串，给etree对象，进行数据解析
    score_page_text = detail_score_page.text
    tree = etree.HTML(score_page_text)

    # 该xpath匹配到所有tr单元，每一个tr单元对应一个学科的信息
    tr_list = tree.xpath('//*[@id="table3"]/tr')
    score_list = []
    f = open("score.txt", "a", encoding="utf-8")

    # 依次取出每一个tr单元中的信息，并存入text_list中
    for i in range(1, 33):
        temp_list = tr_list[i].xpath('./td//text()')  # 从每一个tr单元中分别取出学科名 学分 成绩
        score_list.append(temp_list[2]+(15-len(temp_list[2]))*'  ')
        score_list.append(temp_list[4]+'     ')

        # 成绩通过正则进行解析，去掉中间大量的空格字符
        if len(re.findall(r'\d*\.\d*', str(temp_list[10]), re.S)) == 1:
            score_list.append(re.findall(
                r'\d*\.\d*', str(temp_list[10]), re.S)[0])
        score_list.append('\n')

    # 依次将score_list中的元素写入score.txt文件中
    for j in range(0, len(score_list)):
        f.write(score_list[j])
    f.close()
    print("Get score sucessfully!")
    # 完成成绩的爬取


if __name__ == "__main__":
    # 初始化session对象
    session = requests.session()
    ID = ''#学号
    Password = ''#密码
    info_page_text = get_info_page(session, "ID", "Password")
    get_score(session)
    print("Over!")
