import requests
import json
import time
import datetime
 
if __name__ =="__main__":
    appid='wx461dada8b42217ec'
    secret='2275b0f171b57f29fc750871459be07d'
    touser=['oFQRR53xjtQSw_nBvkEWNAAa32WQ','oFQRR524fThpTCo9-CtERnieIpZo']#微信用户id
    template_id='LfGdm2BTfZkZ0rVRqrnwNoYYkjDCpuiHJTQyGOfAx6s'#模板id
    city_id='101030500'#城市天气id
    birthday = "2001-01-30"
    inday = "2020-07-13"
    info="爱老婆~"#底部信息
    e='库洛米大人万岁！！'#底部信息
 
 
    grant_type = 'client_credential'
    url=f'https://api.weixin.qq.com/cgi-bin/token?grant_type={grant_type}&appid={appid}&secret={secret}'
    response=requests.get(url).json()
    access_token=''
    if response['expires_in']==7200:
        # 获取token
        access_token=response['access_token']
        #天气获取
        headers = {
            'Referer': 'http://www.weather.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }
        url = f'http://d1.weather.com.cn/weather_index/{city_id}.html?_=' + str(int(round(time.time() * 1000)))
        #日期计算
        r = requests.get(url, headers=headers)
        r.encoding = "utf8"
        res = eval(r.text.split(";")[0].split("=")[-1])
        time=res['weatherinfo']['fctime']
        year=time[0:4]
        month=time[4:6]
        day=time[6:8]
        week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        week=week_list[datetime.date(int(year),int(month),int(day)).weekday()]
        date = f'{year}年{month}月{day}日  {week}'
        date2 = f'{int(month)}月{day}日'
 
        # 你活了多久
        birthday_date = datetime.datetime.strptime(birthday, "%Y-%m-%d")
        curr_datetime = datetime.datetime.now()
        minus_datetime = curr_datetime - birthday_date
        #在一起多久了
        inday_date = datetime.datetime.strptime(inday, "%Y-%m-%d")
        cur_datetime = datetime.datetime.now()
        minu_datetime = cur_datetime - inday_date
        #发送消息
        sendMessage_url=f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
        for user in touser:
            data={
               "touser":user,
               "template_id":template_id,
               "appid":appid,
               "data":{
                   "demo": {
                       "value": "巴库来了！！",
                       "color": "#AAFF00"
                   },
                   "live": {
                       "value": minus_datetime.days,
                       "color": "#00FF00"
                   },                  
                   "in": {
                       "value": minu_datetime.days,
                       "color": "#FF0000"
                   },
                   "date2": {
                       "value": date2,
                       "color": "#6B6A66"
                   },
                   "date": {
                       "value": date,
                       "color": "#CAA06A"
                   },
                    "city":{
                        "value":res['weatherinfo']['city'],
                        "color": "#00FF00"
                    },
                   "weather":{
                       "value":res['weatherinfo']['weather'],
                       "color": "#F9AD08"
                   },
                    "tempn":{
                        "value":res['weatherinfo']['tempn'],
                        "color": "#9DB981"
                    },
                   "temp":{
                        "value":res['weatherinfo']['temp'],
                        "color":"#CAA06A"
                    },
                   "wd":{
                        "value":info,
                        "color":"#92CAD9"
                    },
                   'english':{
                       "value":e,
                       "color":"#FF0000"
                   }
 
               }
           }
 
            getTemp=requests.post(sendMessage_url,data=json.dumps(data)).json()
    else:
        print("appid或secret错误")
