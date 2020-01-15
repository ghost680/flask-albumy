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
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "cookie": "thw=cn; t=e3dde219b045ab0e731a6f51c84aca01; cookie2=7d80114512893e9d5d99112561968ac4; _tb_token_=e11be635eed63; hng=CN%7Czh-CN%7CCNY%7C156; _fbp=fb.1.1575942752140.632883310; UM_distinctid=16f7de828ad125-01e751d70aa453-6701b35-1fa400-16f7de828ae388; enc=Hu%2B8c3uAo8Nz33yvlxAJzgKwME63Xx%2B5els7%2BwcayOyjPEiv%2FsLWiSb%2BpzKTWjb%2FhbXptVpARRRyyhQopjSaWg%3D%3D; linezing_session=AGQXabnfMzHUQmXSbVAbSmi1_1578973872013bzBY_2; _m_h5_tk=cef4d64e9d5cc1f2b028355fd64ed44f_1578981072830; _m_h5_tk_enc=1ea8a1f76f708ec0c467456c22ba2948; cna=JTJuFjINf0MCAW/OdmUsCaYX; v=0; unb=680444539; uc3=nk2=rUsy40dzllLqMA%3D%3D&lg2=UIHiLt3xD8xYTw%3D%3D&vt3=F8dBxdkIp5KC3gDFzgs%3D&id2=VWeROI4beApN; csg=a2391b93; lgc=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; cookie17=VWeROI4beApN; dnk=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; skt=dedad9e322d9b070; existShop=MTU3OTA1MTc4Nw%3D%3D; uc4=id4=0%40V8ZquxYey3ToQrWcugfvKjWsbHY%3D&nk4=0%40r7q0tQqljMBRN2%2BSWbQ7IYzfSVvB; publishItemObj=Ng%3D%3D; tracknick=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; _cc_=WqG3DMC9EA%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=997; _nk_=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; cookie1=VWxl2SuMEDq%2B78NFdezWcami1gr2P%2FVIDTik9xFrvJo%3D; mt=ci=82_1; pnm_cku822=; l=cBr6AKxHQQM9qN7LBOCwlurza77OcIRAguPzaNbMi_5p8_TwbP7OovzqiE96cfWdT4YB43ral1y9-etksmuIt7u0IHaP.; isg=BMLCsSIbKIPEiTTBWD2IXPnpE8gkk8at4xvkuAzbnDXgX2LZ9CLQvUSVDxOGDz5F; uc1=cookie14=UoTblAcBbvD2Kw%3D%3D&lng=zh_CN&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&existShop=true&cookie21=URm48syIZJfmYzXrEixrAg%3D%3D&tag=8&cookie15=WqG3DMC9VAQiUQ%3D%3D&pas=0",
            "referer": "https://shop105628567.taobao.com/search.htm?spm=2013.1.0.0.1c5b6e36YfULwp&search=y"
        }

        for index in range(1):
            path = 'https://shop105628567.taobao.com/i/asynSearch.htm?_ksTS=1578987915300_576&callback=jsonp577&mid=w-3053151168-0&wid=3053151168&path=/search.htm&search=y&spm=2013.1.0.0.1c5b6e36YfULwp&pageNo=%d'%(index+1)

            print(path)
            
            r = s.get(path, headers=headers)
            urls = re.findall(r'item\.taobao\.com\/item.htm?\?id=[\d]{12}', r.text)
            list_urls = list(set(urls))
            for item in list_urls:
                print(item)
                # 获取图书详情数据
                text = s.get('http://%s'% item).text
                html = etree.HTML(text)
                book_title = html.xpath('//h3[@class="tb-main-title"]/text()')[0].strip()
                book_ISBN = html.xpath('//ul[@class="attributes-list"]/li/@title')
                book_price = html.xpath('//em[@class="tb-rmb-num"]/text()')[0].strip()
                book_bn = ''
                for isbn in book_ISBN:
                    if re.match(r'^[\d+]{13}$', isbn):
                        book_bn = isbn
                try:
                    tb = Taobao(book_links=item, book_title=book_title, book_price=str(book_price), book_isbn=str(book_bn))
                    db.session.add(tb)
                    db.session.commit()
                    time.sleep(random.random() * 5)
                    print("sleep...",)
                except Exception as e:
                    print(e)
                    print("链接已存在")
            print('==================================================================================')
