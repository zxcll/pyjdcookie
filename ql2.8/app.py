#coding:utf-8
import jdck
from flask import Flask,request,render_template,Response
from io import BytesIO
import qrcode
import ql
from flask_apscheduler import APScheduler

app = Flask(__name__)

@app.route('/')
def jdlog():
    token,okl_token,cookies,cookieurl,jd_ua=jdck.ck()
    list={
        "token":""+token,
        "okl_token":""+okl_token,
        "cookies":""+cookies,
        "jd_ua":""+jd_ua
    }


    return render_template('index.html', qcode=cookieurl,list=list)

@app.route('/cxck')
def cxck():
    token=request.args.get('token')
    okl_token=request.args.get('okl_token')
    cookies=request.args.get('cookies')
    jd_ua=request.args.get('jd_ua')

    data=ql.cxck(token,okl_token,cookies)

    return data


@app.route('/jdcookie')
def cr():
    print("-------------------------------------------")
    url = request.args.get('ckurl') + "&client_type=m" + "&token=" + request.args.get('token')

    im = qrcode.make(url)

    img = BytesIO()  # 创建图片流
    im.save(img, format='PNG')  # 将图片放图片流里面
    img = img.getvalue()  # 返回图片流
    return Response(img, mimetype='image/png')  # 用自定义返回的数据及类型



#定时禁用过期cookie
def job_function():
    ql.checkCookie()


def task():


    scheduler = APScheduler()
    scheduler.init_app(app)
    #
    scheduler.add_job(func=job_function, trigger='interval', seconds=1800, id='my_job_id')
    scheduler.start()


task()




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
