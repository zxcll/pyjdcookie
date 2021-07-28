#coding:utf-8
import time
import requests



def ck():
    t = round(time.time())
    millis=format(t)
    session = requests.session()
    #不好使更新UA，一般能好
    jd_ua="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.80 Mobile/15E148 Safari/604.1"
    #stokenurl = 'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state=%s&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport' % millis
    stokenurl =  'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state=%s&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'% millis

    sheaders = {
        'Referer': 'https://plogin.m.jd.com/cgi-bin/mm/new_login_entrance?lang=chs&appid=300&returnurl=https://wq.jd.com/passport/LoginRedirect?state=%s&returnurl=https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport' % millis,
        'User-Agent': jd_ua

    }
    s = session.get(url=stokenurl, headers=sheaders)


    url = 'https://plogin.m.jd.com/cgi-bin/m/tmauthreflogurl?s_token={0}&v={1}&remember=true'.format(s.json()['s_token'], t)

    body = {
        'lang': 'chs',
        'appid': 300,
        'returnurl': 'https://wqlogin2.jd.com/passport/LoginRedirect?state=%sreturnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'% millis
        }
    headers = {
        'User-Agent': jd_ua,
        'referer': 'https://plogin.m.jd.com/login/login?appid=300&returnurl=https://wqlogin2.jd.com/passport/LoginRedirect?state=%s&returnurl=//home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&/myJd/home.action&source=wq_passport'% millis,
        'Content-Type': 'application/x-www-form-urlencoded; Charset=UTF-8'
    }
    res = session.post(url=url, data=body, headers=headers)
    onekeylog_url = res.json()['onekeylog_url']
    token = res.json()['token']
    okl_token = res.cookies['okl_token']

    cookieurl = "https://plogin.m.jd.com/cgi-bin/m/tmauth?appid=300&client_type=m&token=" + token


    cookies = "guid=%s;lang=chs;lsid=%s;lstoken=%s;" % (
    session.cookies['guid'], session.cookies['lsid'], session.cookies['lstoken'])
    print(cookieurl)


    return token,okl_token,cookies,cookieurl
