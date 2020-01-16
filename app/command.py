# -*- coding: utf-8 -*-

import os
import re
import time
import random
import requests
from lxml import etree

import click
from flask import current_app
from app.extensions import db
from app.models import Role
from app.models import Taobao, User, Role

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
    
    # 初始化权限角色
    @app.cli.command()
    def init():
        """ Initialize Albumy. """
        click.echo('Initializing the roles and permissions...')
        Role.init_role()
        click.echo('Done.')
    
    # 为已经存在点用户添加角色和权限
    @app.cli.command()
    def init_role_permission():
        """ set role permission """
        for user in User.query.all():
            if user.role is None:
                if user.email == current_app.config['ALBUMY_ADMIN_EMAIL']:
                    user.role = Role.query.filter_by(name='Administrator').first()
                else:
                    user.role = Role.query.filter_by(name='User').first()
            
            db.session.add(user)
        db.session.commit()
    
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
            
            "cookie": "thw=cn; t=e3dde219b045ab0e731a6f51c84aca01; cookie2=7d80114512893e9d5d99112561968ac4; _tb_token_=e11be635eed63; hng=CN%7Czh-CN%7CCNY%7C156; _fbp=fb.1.1575942752140.632883310; UM_distinctid=16f7de828ad125-01e751d70aa453-6701b35-1fa400-16f7de828ae388; _m_h5_tk=cef4d64e9d5cc1f2b028355fd64ed44f_1578981072830; _m_h5_tk_enc=1ea8a1f76f708ec0c467456c22ba2948; cna=JTJuFjINf0MCAW/OdmUsCaYX; v=0; mt=ci=55_1; lgc=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; dnk=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; publishItemObj=Ng%3D%3D; tracknick=%5Cu6211%5Cu5BB6%5Cu4E2B%5Cu593499; tg=0; linezing_session=AGQXabnfMzHUQmXSbVAbSmi1_1579067527744pgEN_3; uc3=nk2=rUsy40dzllLqMA%3D%3D&vt3=F8dBxdkIpWaYkf0%2FSHs%3D&id2=VWeROI4beApN&lg2=VFC%2FuZ9ayeYq2g%3D%3D; csg=0cad1ab7; skt=697249347f096ac0; existShop=MTU3OTA3NDcyOA%3D%3D; uc4=nk4=0%40r7q0tQqljMBRN2%2BSWbQ7IY57zM5L&id4=0%40V8ZquxYey3ToQrWcugfvKF4pkkY%3D; _cc_=Vq8l%2BKCLiw%3D%3D; enc=tAZnkxPlP9gyBMPpzLfOjcXJ2pKufT8DjDaCW5XITifw3JXjzZ8NjBcRlVgMltZT0rQXZ1xKh6hXAg2xF%2BvN0w%3D%3D; uc1=cookie14=UoTblAYTRIM%2Fsw%3D%3D&lng=zh_CN&cookie16=VFC%2FuZ9az08KUQ56dCrZDlbNdA%3D%3D&existShop=true&cookie21=W5iHLLyFfXVRDP8mxoRA8A%3D%3D&tag=8&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&pas=0; pnm_cku822=098%23E1hvyvvUvbpvUvCkvvvvvjiPRschsjE8RFzvzjnEPmPy0jiEPFMWzjYnR2MyQjn8iQhvCvvv9UUtvpvhvvvvvvhCvvOvUvvvphvEvpCWhEf2vva1S47B9CkaU6bnDO2pjLyDZacEKOmAdcHvaNLBtLkAb6evD7zpd3ODN%2BLwaNpBK7ERiNoxfXkfjobhAnLvjX31B%2Bs9%2Bnezr8yCvv9vvUmzqPgIcOyCvvOUvvVva6TtvpvIvvvvvbYvtQUvvUnvphvhRQvv96CvpC29vvm2phCvhhvvvUnvphvppvGCvvpvvPMM; l=cBr6AKxHQQM9q3UoXOCwourza77OSIRAguPzaNbMi_5wE6L1cB_OovvdBFp6VfWd97YB43ral1y9-etkidspROu0IHaP.; isg=BGpqwl5RwDrT2kzJQOXQ1JGxu9AM2-41e9M8sPQjFr1IJwrh3Gs-RbBVt1s712bN",

            "referer": "https://shop105628567.taobao.com/search.htm?spm=2013.1.0.0.1c5b6e36YfULwp&search=y"
        }

        try:
            for index in range(30):
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
