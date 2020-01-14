# -*- coding: utf-8 -*-

import os
import re
import time
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
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36",
            "cookie": "thw=cn; v=0; t=e3dde219b045ab0e731a6f51c84aca01; cookie2=7d80114512893e9d5d99112561968ac4; _tb_token_=e11be635eed63; cna=JTJuFjINf0MCAW/OdmUsCaYX; hng=CN%7Czh-CN%7CCNY%7C156; _fbp=fb.1.1575942752140.632883310; publishItemObj=Ng%3D%3D; miid=54963891934606821; UM_distinctid=16f7de828ad125-01e751d70aa453-6701b35-1fa400-16f7de828ae388; mt=ci=53_1; lgc=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; dnk=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; tracknick=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; tg=0; uc3=id2=VWeROI4beApN&nk2=rUsy40dzllLqMA%3D%3D&vt3=F8dBxdkL1DDt4Cn5nYg%3D&lg2=W5iHLLyFOGW7aA%3D%3D; csg=a7651bf9; skt=9ac68098dc5c68e1; existShop=MTU3ODk3MjYwNA%3D%3D; uc4=nk4=0%40r7q0tQqljMBRN2%2BSWbQ6N10Z2tvU&id4=0%40V8ZquxYey3ToQrWcugYLd1273HE%3D; _cc_=U%2BGCWk%2F7og%3D%3D; enc=Hu%2B8c3uAo8Nz33yvlxAJzgKwME63Xx%2B5els7%2BwcayOyjPEiv%2FsLWiSb%2BpzKTWjb%2FhbXptVpARRRyyhQopjSaWg%3D%3D; linezing_session=AGQXabnfMzHUQmXSbVAbSmi1_1578973872013bzBY_2; _m_h5_tk=cef4d64e9d5cc1f2b028355fd64ed44f_1578981072830; _m_h5_tk_enc=1ea8a1f76f708ec0c467456c22ba2948; uc1=cookie14=UoTbldsMpYm5qA%3D%3D&lng=zh_CN&cookie16=Vq8l%2BKCLySLZMFWHxqs8fwqnEw%3D%3D&existShop=true&cookie21=UtASsssmfaCONGki4KTH3w%3D%3D&tag=8&cookie15=UtASsssmOIJ0bQ%3D%3D&pas=0; pnm_cku822=098%23E1hv%2BvvUvbpvUvCkvvvvvjiPRsLygj1HPLFpQjivPmPptjr2RFdWQjD8PLFpgjEHiQhvCvvvpZptvpvhvvCvpvGCvvpvvPMMvphvC9vhphvvvvyCvhACMhxHjc7JRqJ6EvLv%2Bb8rVTtYVVzwd34AdcwuYU9BHd8rJoL6F404d3ODN%2BLvdigqrADn9Wv7%2Bu0Owos6QC465i3spJLOHFKzrmphKphv8vvvph2MMM1vvvCj1Qvvvh%2BvvhNjvvvmjvvvBGwvvvUUvvCj1Qvvv9kivpvUvvCCbIgWpDVEvpvVvpCmpYsy; l=cBr6AKxHQQM9qajWBOCZourza779SIRAguPzaNbMi_5C56L1eTQOovZKaFp6cfWd9g8B43ral1y9-etkidspROzwoGVO.; isg=BBMTR_mrSScgBwVu0RbJm7BSopc9yKeK-tC118UwazJpRDPmTZoy2jWSfvyPZP-C",
            "referer": "https://shop105628567.taobao.com/search.htm?spm=2013.1.0.0.1c5b6e36YfULwp&search=y"
        }

        for index in range(1):
            r = requests.get('https://shop105628567.taobao.com/i/asynSearch.htm?_ksTS=1578987915300_576&callback=jsonp577&mid=w-3053151168-0&wid=3053151168&path=/search.htm&search=y&spm=2013.1.0.0.1c5b6e36YfULwp&pageNo=%d'%(index), headers=headers)

            urls = re.findall(r'item\.taobao\.com\/item.htm?\?id=[\d]{12}', r.text)
            for item in urls:
                print(item)
                try:
                    tb = Taobao(book_links=item, book_title='', book_ISBN='')
                    db.session.add(tb)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    print("链接已存在")
            print('==================================================================================')