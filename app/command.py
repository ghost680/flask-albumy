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
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            
            "cookie": "thw=cn; t=e3dde219b045ab0e731a6f51c84aca01; cookie2=7d80114512893e9d5d99112561968ac4; _tb_token_=e11be635eed63; hng=CN%7Czh-CN%7CCNY%7C156; _fbp=fb.1.1575942752140.632883310; UM_distinctid=16f7de828ad125-01e751d70aa453-6701b35-1fa400-16f7de828ae388; _m_h5_tk=cef4d64e9d5cc1f2b028355fd64ed44f_1578981072830; _m_h5_tk_enc=1ea8a1f76f708ec0c467456c22ba2948; cna=JTJuFjINf0MCAW/OdmUsCaYX; v=0; _l_g_=Ug%3D%3D; mt=ci=55_1; unb=680444539; lgc=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; cookie17=VWeROI4beApN; dnk=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; publishItemObj=Ng%3D%3D; tracknick=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; tg=0; sg=997; _nk_=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; cookie1=VWxl2SuMEDq%2B78NFdezWcami1gr2P%2FVIDTik9xFrvJo%3D; linezing_session=AGQXabnfMzHUQmXSbVAbSmi1_1579067527744pgEN_3; uc1=lng=zh_CN&existShop=true&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&cookie21=UIHiLt3xSixwG45%2Bs3wzsA%3D%3D&cookie14=UoTblAcDMvGzVg%3D%3D&pas=0&cookie15=WqG3DMC9VAQiUQ%3D%3D&tag=8; uc3=nk2=rUsy40dzllLqMA%3D%3D&vt3=F8dBxdkIpWaYkf0%2FSHs%3D&id2=VWeROI4beApN&lg2=VFC%2FuZ9ayeYq2g%3D%3D; csg=0cad1ab7; skt=697249347f096ac0; existShop=MTU3OTA3NDcyOA%3D%3D; uc4=nk4=0%40r7q0tQqljMBRN2%2BSWbQ7IY57zM5L&id4=0%40V8ZquxYey3ToQrWcugfvKF4pkkY%3D; _cc_=Vq8l%2BKCLiw%3D%3D; enc=tAZnkxPlP9gyBMPpzLfOjcXJ2pKufT8DjDaCW5XITifw3JXjzZ8NjBcRlVgMltZT0rQXZ1xKh6hXAg2xF%2BvN0w%3D%3D; pnm_cku822=; x5sec=7b2273686f7073797374656d3b32223a223130626266613662373538313763633630653130343066393866613961326265434c72462b2f4146454d4f6f30724841734c583144786f4c4e6a67774e4451304e544d354f7a4d3d227d; isg=BFJSDZ5SWPNaHqQRKG04DMm5oxg0Y1b9E-sUSByraYXwL_IpBPLVD1RGn4MTX86V; l=cBr6AKxHQQM9q25JBOCwourza77tbIRAguPzaNbMi_5Cv1T6G1_Oov8Lwe96cfWd9-TB43ral1y9-etk9LSpROu0IHaP.",

            "referer": "https://shop105628567.taobao.com/search.htm?spm=2013.1.0.0.1c5b6e36YfULwp&search=y"
        }

        try:
            for index in range(10):
                path = 'https://shop105628567.taobao.com/i/asynSearch.htm?_ksTS=1578987915300_576&callback=jsonp577&mid=w-3053151168-0&wid=3053151168&path=/search.htm&search=y&spm=2013.1.0.0.1c5b6e36YfULwp&pageNo=%d' % (index + 301)

                print(path)
                # 5085 + 50 * 24 = 1200 6285
                
                r = s.get(path, headers=headers)
                urls = re.findall(r'item\.taobao\.com\/item.htm?\?id=[\d]{12}', r.text)

                if len(urls):
                    list_urls = list(set(urls))

                    for item in list_urls:
                        print('https://%s'% item)
                        
                        """ 查询数据库商品是否存在 """
                        tb_data = Taobao.query.filter_by(book_links=item).first()

                        if tb_data == None:
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
                        
                                tb = Taobao(book_links=item)
                                db.session.add(tb)
                                db.session.commit()
                        else:
                            print('当前图书已经存在 -> https://%s'% item)
                else:
                    print('被抓到了，休息一下')
                    
                time.sleep(10)
                print("sleep...",)

                print('==================================================================================')
        except Exception as e:
            print(e)
            print("发生错误了...")
