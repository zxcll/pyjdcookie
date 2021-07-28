import requests
import time
import json
from urllib import parse
import socket
import socks
#读取配置文件
f = open("./config.json","r")
config = json.load(f)

#获取青龙token
def qltoken():
    url=config['url']+"/api/login?t="+str(round(time.time() * 1000))
    data={
        "password":config['password'],
        "username":config['username']
    }
    res=requests.post(url,json=data)
    if int(res.json()['code']) == 200:
        return res.json()['token']
    else:
        tgbot("青龙登录失败")
        return "false"


# 查询并获取京东cookie
def cxck(token, okl_token,cookies):
    jd_ua = "JD4iPhone/167724 (iPhone; iOS 15.0; Scale/3.00)Accept-Language: zh-Hans-CN;q=1"
    t = round(time.time())
    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthchecktoken?&token={0}&ou_state=0&okl_token={1}'.format(token,okl_token)
    body1 = {
        'lang': 'chs',
        'appid': 300,
        'returnurl': 'https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action'.format(t),
        'source': 'wq_passport',
    }

    headers = {
        'User-Agent': jd_ua,
        'Cookie': cookies,
        'referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state={0}&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'.format(t),
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }

    res = requests.post(url=url, data=body1, headers=headers)

    print(res.json())

    if res.json()['errcode'] == 0:
        ck = "pt_key=%s;pt_pin=%s;" % (res.cookies['pt_key'], res.cookies['pt_pin'])
        errcode = res.json()['errcode']
        print("获取cookie成功：" + ck)
        qlcx(res.cookies['pt_pin'], ck)
        return {"errcode": "" + str(errcode), "ck": "" + str(ck)}
    else:
        return res.json()



#获取青龙环境变量
def qlevn():
    token=qltoken()
    url=config['url']+"/api/envs?searchValue=&t="+str(round(time.time() * 1000))
    headers={
        "Authorization":"Bearer "+token
    }

    res=requests.get(url,headers=headers)
    return res,token

#查询账号是否存在
def qlcx(pin,ck):
    age = 0
    res,token=qlevn()
    for i in res.json()['data']:
        #存在修改
        if pin  in i['value'] :
            ckupdata(i['_id'],ck,i['remarks'],token,i['status'])
            age+=1
            break

    # 不存在新增
    if age==0:
        ckadd(ck,pin,token)

#修改cookie
def ckupdata(id,ck,remarks,token,status):
    url=config['url']+"/api/envs?t="+str(round(time.time() * 1000))
    data={
        "name":"JD_COOKIE",
        "value":ck,
        "_id":id,
        "remarks":remarks
    }
    headers = {
        'Accept''': 'application/json',
        "Authorization":"Bearer "+token,
        'Content-Type': 'application/json;charset=UTF-8'

    }
    res=requests.put(url,data=json.dumps(data),headers=headers)
    if res.json()['code'] == 200:
        print(remarks+"修改成功")
        msg=remarks+"修改成功"
        tgbot(msg)
        #启用cookie
        if int(status)==1:
            ckqy(id, token,remarks)
    else:
        print(remarks+"修改失败")
        msg = remarks + "修改失败"
        tgbot(msg)
    

#新增cookie
def ckadd(ck,pin,token):
    url=config['url']+"/api/envs?t="+str(round(time.time() * 1000))
    data={
        "name":"JD_COOKIE",
        "value":ck,
        "remarks":pin
    }
    headers={
        "Authorization": "Bearer "+token
    }
    res=requests.post(url=url,json=data,headers=headers)
    if res.json()['code'] == 200:
        print(pin + "新增成功")
        msg = pin + "新增成功"
        tgbot(msg)
    else:
        print(pin + "新增失败")
        msg = pin + "新增失败"
        tgbot(msg)


#检查cookie是否过期
def checkCookie():
    print("-------------检查ck状态---------------")
    url = "https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
    res,token=qlevn()

    for i in res.json()['data']:
        if "JD_COOKIE" == i['name']:
            headers = {
                "Host": "me-api.jd.com",
                "Accept": "*/*",
                "Connection": "keep-alive",
                "Cookie": i['value'],
                "User-Agent": "jdapp;iPhone;9.4.4;14.3;network/4g;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",
                "Accept-Language": "zh-cn",
                "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
                "Accept-Encoding": "gzip, deflate, br"
            }
            r=requests.get(url=url,headers=headers)
            #过期禁用
            if int(r.json()['retcode']) == 1001 and int(i['status'] == 0) :
                ckjy(i['_id'],token,i['remarks'])


#禁用cookie
def ckjy(id,token,remarks):
    url=config['url']+"/api/envs/disable?t="+str(round(time.time() * 1000))
    headers={
        "Authorization": "Bearer "+token
    }
    res=requests.put(url,json=[id],headers=headers)
    if int(res.json()['code']) == 200:
        print(remarks+"禁用成功")
        msg=remarks+"禁用成功"
        tgbot(msg)
    else:
        print(remarks+"禁用失败")
        msg = remarks + "禁用失败"
        tgbot(msg)


#启用cookie
def ckqy(id,token,remarks):

    url=config['url']+"/api/envs/enable?t="+str(round(time.time() * 1000))
    headers={
        "Authorization": "Bearer "+token
    }
    res=requests.put(url,json=[id],headers=headers)
    if int(res.json()['code']) == 200:
        print(remarks+"启用成功")
        msg = remarks + "启用成功"
        tgbot(msg)
    else:
        print(remarks+"启用失败")
        msg = remarks + "启用失败"
        tgbot(msg)



#tg通知
def tgbot(msg):
    if config['sock_ip'] !="" and config['sock_port'] !="":
        socks.set_default_proxy(socks.SOCKS5, config['sock_ip'], int(config['sock_port']))
        socket.socket = socks.socksocket
    if config['tgbot'] !="" and config['tguid'] !="":
        try:
            requests.get("https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s" % (
            config['tgbot'], config['tguid'], parse.quote(msg)))
        except Exception as e:
            print("推送失败！原因："+str(e))
