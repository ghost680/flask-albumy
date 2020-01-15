# -*- coding: utf-8 -*-

import os
import re
import time
import random
import requests
from lxml import etree

import click
from app.extensions import db
from app.models import Taobao

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """ Initialize the datebase. """
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')
    
    @app.cli.command()
    def spider():
        """ spider tb data """
        proxies = {
            "https": "https://58.212.67.253:9999",
        }
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        headers = {
            "User-Agent": "User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "cookie": "thw=cn; t=e3dde219b045ab0e731a6f51c84aca01; cookie2=7d80114512893e9d5d99112561968ac4; _tb_token_=e11be635eed63; hng=CN%7Czh-CN%7CCNY%7C156; _fbp=fb.1.1575942752140.632883310; UM_distinctid=16f7de828ad125-01e751d70aa453-6701b35-1fa400-16f7de828ae388; linezing_session=AGQXabnfMzHUQmXSbVAbSmi1_1578973872013bzBY_2; _m_h5_tk=cef4d64e9d5cc1f2b028355fd64ed44f_1578981072830; _m_h5_tk_enc=1ea8a1f76f708ec0c467456c22ba2948; cna=JTJuFjINf0MCAW/OdmUsCaYX; v=0; uc3=id2=Vv0kxLe47C4U&nk2=F5RBwlFLmC3jNg%3D%3D&vt3=F8dBxdkIp5UQc200bCY%3D&lg2=URm48syIIVrSKA%3D%3D; csg=c285334d; lgc=tb47073_44; dnk=tb47073_44; skt=feacf68e26ebe111; existShop=MTU3OTA1MjMyMQ%3D%3D; uc4=id4=0%40VHtAwi95E0APbfmexftmUCnG0Q8%3D&nk4=0%40FY4KpzVoKGUJ%2FRTE91tOsA0pCsnM; tracknick=tb47073_44; _cc_=VFC%2FuZ9ajQ%3D%3D; tg=5; mt=ci=55_1; enc=X%2FjyXT5jd1JB2TXjZOVfnRKGeDDdB1Xt6CwDkPIoZcBdxvc1Xf39ZTpYDSoJRhkLv5x6zDfaSHL0ld3IhUXAUg%3D%3D; uc1=cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=W5iHLLyFeYZ1WM9hVnmS&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&pas=0&cookie14=UoTblAcBaRo0SQ%3D%3D&tag=8&lng=zh_CN; x5sec=7b2273686f7073797374656d3b32223a223861386436346632323466653931633833393939353039363233616136333635434e62462b76414645495741783632366c2f2f7845686f4c4e544d7a4f4449334e4441784f7a493d227d; pnm_cku822=098%23E1hv09vUvbpvUpCkvvvvvjiPRscv0jlWP2zwgjYHPmPU1jE8PsqOgjYnRsLWzjtbRLyCvvpvvvvvmphvLvB3DQvjOI7rqU0QKoZHAW2I32RTbyzBif0tH2D%2BV8Lrsa06RknbInVyqfVQWl4vQRFE%2BFIlBqeviNoAdcyyGExrl8gcbhet5aV351AEvpvVmvvC9jaRuphvmvvv9bN5o6EyKphv8vvvvvmMpRwmvvm2phCvCvQvvUnvphvpgvvv96CvpCCvvvm2phCvhhvCvpvVvmvvvhCv2QhvCvvvvvm5vpvhvvmv99%3D%3D; l=cBr6AKxHQQM9q3_fBOCwourza77tSIRAguPzaNbMi_5Q66LMD2QOov7L7Fp6cfWd97YB43ral1y9-etkidspROu0IHaP.; isg=BDk51cXFQzYlHR-8r2iz6aa0SKUTRi34jLYP5VtuumDX4ll0o5cDyDE0ZO4U2sUw",
            "referer": "https://shop105628567.taobao.com/search.htm?spm=2013.1.0.0.1c5b6e36YfULwp&search=y"
        }

        for index in range(50):
            path = 'https://shop105628567.taobao.com/i/asynSearch.htm?_ksTS=1578987915300_576&callback=jsonp577&mid=w-3053151168-0&wid=3053151168&path=/search.htm&search=y&spm=2013.1.0.0.1c5b6e36YfULwp&pageNo=%d' % (index+101)

            print(path)
            
            r = s.get(path, headers=headers)
            urls = re.findall(r'item\.taobao\.com\/item.htm?\?id=[\d]{12}', r.text)
            list_urls = list(set(urls))
            for item in list_urls:
                # print('https://%s'% item)
                
                """ 查询数据库商品是否存在 """
                tb_data = Taobao.query.filter_by(book_links=item).first()

                if not tb_data:
                    # 获取图书详情数据
                    # text = s.get('https://%s'% item, headers=headers).text
                    # html = etree.HTML(text)
                    # book_title = html.xpath('//h3[@class="tb-main-title"]/text()')[0].strip()
                    # book_ISBN = html.xpath('//ul[@class="attributes-list"]/li/@title')
                    # book_price = html.xpath('//em[@class="tb-rmb-num"]/text()')[0].strip()
                    # book_bn = ''
                    # for isbn in book_ISBN:
                    #     if re.match(r'^[\d+]{13}$', isbn):
                    #         book_bn = isbn
                    try:
                        tb = Taobao(book_links=item)
                        db.session.add(tb)
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        print("链接已存在")
                else:
                    print('当前图书已经存在 -> https://%s'% item)
            
            
            time.sleep(random.random() * 10)
            print("sleep...",)

            print('==================================================================================')
