# -*- coding:utf-8 -*-
import pygame
import json, os.path
import datetime
import sys
#import threading
import time
from pygame.locals import *
from urllib import request
from PIL import Image
#from threading import Timer
from ondo2 import *

def download(url,i):
    img = request.urlopen(url)
    localfile = open( i+".gif", 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()

def img_show(filename):
    img = Image.open(filename, 'r')
    #out=img.resize((150,93))
    img.show()
    img.close()

def merge():
    # 矢印ダウンロード
    arraw = request.urlopen("http://livedoor.blogimg.jp/may_05_2008/imgs/1/d/1d5afad5.jpg?350260")
    arrawfile = open("right.jpg", "wb")
    arrawfile.write(arraw.read())
    arraw.close()
    arrawfile.close()
    # 既存画像を読み込み
    a_jpg = Image.open('0.gif', 'r').resize((150,93))
    b_jpg = Image.open('1.gif', 'r').resize((150, 93))
    right = Image.open("right.jpg", 'r').resize((30, 50)) #矢印
    # マージに利用する下地画像を作成する
    canvas = Image.new('RGB', (330, 93), (255, 255, 255))
    # pasteで、座標（0, 0）と（0, 100）に既存画像を乗せる。
    canvas.paste(a_jpg, (0, 0))
    canvas.paste(right,(151,20))
    canvas.paste(b_jpg, (181, 0))
    # 保存
    canvas.save('c.gif', 'GIF', quality=100, optimize=True)

def forecast():
    rssurl = "http://weather.livedoor.com/forecast/webservice/json/v1?city=250010"
    resp = request.urlopen(rssurl).read().decode('utf-8')
    resp = json.loads(resp)
    forefore=[]
    i = 0
    for forecast in resp['forecasts']:
        if type(forecast['temperature']['max']) is dict:
            forecast['temperature']['max'] = forecast['temperature']['max']['celsius']
        if type(forecast['temperature']['min']) is dict:
            forecast['temperature']['min'] = forecast['temperature']['min']['celsius']
        if str(forecast['temperature']['max']) == "None":
            forecast['temperature']['max'] = ' -'
        if str(forecast['temperature']['min']) == "None":
            forecast['temperature']['min'] = ' -'
        forefore.append(forecast['temperature'])
        foreimg=str(forecast['image']['url']) #画像情報
        download(foreimg, str(i))  # 画像をカレントディレクトリに保存
        i+=1
    time.sleep(0.2)
    merge()
    return forefore

def main():
    setup()
    get_calib_param() ##??
    pygame.init()                               # Pygameの初期化
    screen = pygame.display.set_mode((480, 320))    # 大きさ600*500の画面を生成
    pygame.display.set_caption("Piweather")              # タイトルバーに表示する文字
    font_b = pygame.font.Font(None, 160)               # フォントの設定(25px)
    font_s = pygame.font.Font(None,70)
    font_ss = pygame.font.Font(None, 45)
    now = datetime.datetime.now()
    forecast()

    screen.fill((255, 255, 255))  # 画面を白色に塗りつぶし
    date = font_s.render(str(now.year) + "/" + str(now.month) + "/" + str(now.day), True, (0, 0, 0))
    screen.blit(date, [10, 5])
    weatherimg = pygame.image.load("c.gif").convert_alpha()  # 天気の表示位置
    screen.blit(weatherimg, [10, 190])
    maxmin1 = font_ss.render(str(forecast()[0]["max"]) + "/" + str(forecast()[0]["min"]), True, (0, 0, 0))
    screen.blit(maxmin1, [50, 293])
    maxmin2 = font_ss.render(str(forecast()[1]["max"]) + "/" + str(forecast()[1]["min"]), True, (0, 0, 0))
    screen.blit(maxmin2, [255, 293])
    pygame.draw.line(screen, (0, 0, 0), (0, 180), (480, 180), 5)
    pygame.draw.line(screen, (0, 0, 0), (360, 180), (360, 320), 5)
    pygame.draw.line(screen, (0, 0, 0), (20, 291), (130, 291), 3)
    pygame.draw.line(screen, (0, 0, 0), (20, 291), (20, 320), 3)
    pygame.draw.line(screen, (0, 0, 0), (130, 291), (130, 320), 3)
    pygame.draw.line(screen, (0, 0, 0), (220, 291), (330, 291), 3)
    pygame.draw.line(screen, (0, 0, 0), (220, 291), (220, 320), 3)
    pygame.draw.line(screen, (0, 0, 0), (330, 291), (330, 320), 3)
    pygame.display.update()


    while (1):
        refran=[Rect(10, 50, 470, 120),Rect(380,220, 80, 80)]
        now = datetime.datetime.now()
        triger = [now.hour, now.minute, now.second]

        if now.second<10 and now.minute<10 and now.hour<10:
            now_t = font_b.render("0"+str(now.hour) + ":0" + str(now.minute) + ":0" + str(now.second), True, (0, 0, 0))
        elif now.second<10 and now.minute<10:
            now_t = font_b.render(str(now.hour) + ":0" + str(now.minute) + ":0" + str(now.second), True, (0, 0, 0))
        elif now.second<10 and now.hour<10:
            now_t = font_b.render("0"+str(now.hour) + ":" + str(now.minute) + ":0" + str(now.second), True, (0, 0, 0))
        elif now.minute<10 and now.hour<10:
            now_t = font_b.render("0"+str(now.hour) + ":0" + str(now.minute) + ":" + str(now.second), True, (0, 0, 0))
        elif now.second<10:
            now_t = font_b.render(str(now.hour)+":" +str(now.minute)+":0"+str(now.second), True, (0,0,0))   # 時間を取得して描画する文字に設定
        elif now.minute<10:
            now_t = font_b.render(str(now.hour) + ":0" + str(now.minute) + ":" + str(now.second), True, (0, 0, 0))
        elif now.hour<10:
            now_t = font_b.render("0"+str(now.hour) + ":" + str(now.minute) + ":" + str(now.second), True, (0, 0, 0))
        else:
            now_t = font_b.render(str(now.hour) + ":" + str(now.minute) + ":" + str(now.second), True, (0, 0, 0))

        #負荷軽減のために処理を分ける
        #天気画像と天気情報を得る
        #Weather Hacksは5時、11時、17時に更新される
        if triger==[5,0,0] or triger==[11,0,0] or triger==[17,0,0]:
            forecast()
            date = font_s.render(str(now.year) + "/" + str(now.month) + "/" + str(now.day), True, (0, 0, 0))
            screen.blit(date, [10, 5])
            weatherimg = pygame.image.load("c.gif").convert_alpha()  # 天気の表示位置
            screen.blit(weatherimg, [10, 190])
            refran.append(Rect(10, 60, 430, 153))
            #pygame.display.update(Rect(10, 60, 430, 153))

        #最低最高気温更新
        if triger==[5,0,30] or triger==[11,0,30] or triger==[17,0,30]:
            pygame.draw.rect(screen, (255, 255, 255), Rect(45, 293, 60, 30))
            pygame.draw.rect(screen, (255, 255, 255), Rect(245, 293, 60, 30))
            maxmin1 = font_ss.render(str(forecast()[0]["max"]) + "/" + str(forecast()[0]["min"]), True, (0, 0, 0))
            screen.blit(maxmin1, [50, 293])
            maxmin2 = font_ss.render(str(forecast()[1]["max"]) + "/" + str(forecast()[1]["min"]), True, (0, 0, 0))
            screen.blit(maxmin2, [255, 293])
            refran.append(Rect(45, 293, 60, 30))
            refran.append(Rect(245, 293, 60, 30))
            #pygame.display.update([Rect(45, 293, 60, 30), Rect(245, 293, 60, 30)])

               
        pygame.draw.rect(screen, (255, 255, 255), Rect(10, 50, 460, 120))  # 時計位置を白色に塗りつぶし
        pygame.draw.rect(screen, (255, 255, 255), Rect(380,220, 80, 80))
        temp = font_ss.render(readData()[0] + "°C", True, (0, 0, 0))
        hum = font_ss.render(readData()[1] + "  %", True, (0, 0, 0))
        screen.blit(temp, [380, 220])
        screen.blit(hum, [380, 260])
        screen.blit(now_t, [15, 60])  # 時刻の表示位置
        pygame.display.update(refran)     # 画面を更新
        time.sleep(0.2)

        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()       # Pygameの終了(画面閉じられる)
                sys.exit()

if __name__ == "__main__":
    main()
    try:
        readData()
    except KeyboardInterrupt:
        pass
