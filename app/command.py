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
            "cookie": "thw=cn; t=e3dde219b045ab0e731a6f51c84aca01; cookie2=7d80114512893e9d5d99112561968ac4; _tb_token_=e11be635eed63; hng=CN%7Czh-CN%7CCNY%7C156; _fbp=fb.1.1575942752140.632883310; UM_distinctid=16f7de828ad125-01e751d70aa453-6701b35-1fa400-16f7de828ae388; enc=Hu%2B8c3uAo8Nz33yvlxAJzgKwME63Xx%2B5els7%2BwcayOyjPEiv%2FsLWiSb%2BpzKTWjb%2FhbXptVpARRRyyhQopjSaWg%3D%3D; linezing_session=AGQXabnfMzHUQmXSbVAbSmi1_1578973872013bzBY_2; _m_h5_tk=cef4d64e9d5cc1f2b028355fd64ed44f_1578981072830; _m_h5_tk_enc=1ea8a1f76f708ec0c467456c22ba2948; cna=JTJuFjINf0MCAW/OdmUsCaYX; v=0; unb=533827401; uc3=id2=Vv0kxLe47C4U&nk2=F5RBwlFLmC3jNg%3D%3D&vt3=F8dBxdkIp5UQc200bCY%3D&lg2=URm48syIIVrSKA%3D%3D; csg=c285334d; lgc=tb47073_44; cookie17=Vv0kxLe47C4U; dnk=tb47073_44; skt=feacf68e26ebe111; existShop=MTU3OTA1MjMyMQ%3D%3D; uc4=id4=0%40VHtAwi95E0APbfmexftmUCnG0Q8%3D&nk4=0%40FY4KpzVoKGUJ%2FRTE91tOsA0pCsnM; tracknick=tb47073_44; _cc_=VFC%2FuZ9ajQ%3D%3D; tg=5; _l_g_=Ug%3D%3D; sg=418; _nk_=tb47073_44; cookie1=VvkkTyVk0JxSo0caJfrka2ssyGEFWmUb%2B1OrWDX%2Fch8%3D; mt=ci=55_1; pnm_cku822=098%23E1hvo9vUvbpvUvCkvvvvvjiPRscvljDnP2s9QjD2PmPy6jnmRLcU1jlbnLcZ0jimiQhvChCvCCptvpvhphvvvvhCvvXvovvvvvmEvpvVpyUUCEKwuphvmhCvCblLqwCFKphv8hCvvv2MMqytphvwv9vvpwDvpCQmvvChNhCvjvUvvhBZphvwv9vvBHpEvpCWB7x6v8ROwkYYmq0DW3CQcmx%2F1nmK5eEvJQMEtf6sbllIjIcEhbpDVjaW0f06WeCpOxs6if8a4BIzcrVnnCpiLVxpiR01%2B2n7OH2I3vGCvvpvvPMM; uc1=cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&cookie21=V32FPkk%2FgihF%2FS5nr3O5&cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=false&pas=0&cookie14=UoTblAcBaKZQBA%3D%3D&tag=8&lng=zh_CN; isg=BGRk3oR_5smMQhIbSgM25ks_NWJW_Yhn0a1Cwn6FxS_yKQTzpg1Y95rI7Ykx8cC_; l=cBr6AKxHQQM9qjfJBOCwnurza77tIIRAguPzaNbMi_5I16LsEM7Oovr9LFp6cfWdOzLB43ral1J9-etlwKrNApDgcGAN.",
            "referer": "https://shop105628567.taobao.com/search.htm?spm=2013.1.0.0.1c5b6e36YfULwp&search=y"
        }

        for index in range(100):
            path = 'https://shop105628567.taobao.com/i/asynSearch.htm?_ksTS=1578987915300_576&callback=jsonp577&mid=w-3053151168-0&wid=3053151168&path=/search.htm&search=y&spm=2013.1.0.0.1c5b6e36YfULwp&pageNo=%d' % (index+101)

            print(path)
            
            r = s.get(path, headers=headers)
            urls = re.findall(r'item\.taobao\.com\/item.htm?\?id=[\d]{12}', r.text)
            list_urls = list(set(urls))
            for item in list_urls:
                print('https://%s'% item)
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
                    time.sleep(random.random() * 5)
                    print("sleep...",)
                except Exception as e:
                    print(e)
                    print("链接已存在")
            print('==================================================================================')
