import settings
from ali1688scraperbrowser import ScraperBrowser
from bs4 import BeautifulSoup
import datetime
from functools import reduce
import re


def get_attr_content(aa, bb):
    cc = []
    for a in aa:
        for b in bb:
            ctemp = []
            tmp0 = a[0] + ',' + b[0]
            ctemp.append(tmp0)
            tmp1 = ''
            if len(a) > 1 and len(b) > 1:
                tmp1 = a[1] + ' ' + b[1]
            elif len(a) > 1:
                tmp1 = a[1]
            elif len(b) > 1:
                tmp1 = b[1]
            ctemp.append(tmp1)
            cc.append(ctemp)
    return cc


class DougHtmlParse(object):
    def __init__(self):
        pass

    # 整理资料格式product_id;category_name;url
    def get_product_info(self, product_id, category_name, exclude_img, web_page_url):
        soup = None
        if settings.use_html_file_or_browser == settings.HtmlParserTool.FILE:
            fp = open('ali1688html/' + product_id + '.html', encoding='gb18030')
            soup = BeautifulSoup(fp, features='html.parser')
        else:
            sb = ScraperBrowser()
            sb.web_page_url= web_page_url
            html_text=sb.get_html_text()
            soup = BeautifulSoup(html_text, features='html.parser')

        exclude_imgs = []
        if exclude_img:
            exclude_imgs = exclude_img.split(',')
        # print('exclude_imags:',exclude_imgs)

        print('开始解析...')
        shopee_product = []
        for r in range(78):
            shopee_product.append(None)
        # print('shopee_product_len:',len(shopee_product))
        shopee_product[0] = category_name
        # 产品标题
        productname = soup.find('h1', class_='d-title')
        # print('productname:', productname.get_text())
        shopee_product[1] = re.sub(settings.filter_title_name, '', productname.get_text())
        print('开始解析产品描述...')
        # 查找产品描述
        # psummary=soup.select('div.product-property-main')
        psummary = soup.find('div', id='mod-detail-attributes', class_='mod-detail-attributes')
        feature_tds = psummary.select('td')
        tdi = 0
        tds = []
        # 跳过过滤取值标志
        f = 0
        # 设置增加标题值标志
        tf = 0
        add_title_str = ''
        for td in feature_tds:
            tdi += 1
            spans = td.get_text()
            if spans:
                if f == 1:
                    f = 0
                    continue

                if tf == 1:
                    tf = 0
                    add_title_str += spans
                if spans in settings.add_title_field_name:
                    tf = 1

                if spans in settings.product_property_field_names:
                    f = 1
                if f == 0:
                    tds.append(spans)
        # print('spans:')
        # print(spans.replace('\n','')+':'+str(tdi))
        product_desc = reduce(lambda x, y: x + y,
                              map(lambda x: x + ':' if tds.index(x) % 2 == 0 and x else x + '\n', tds))
        # print(product_desc)
        shopee_product[1] = re.sub('[/]+', '', add_title_str) + ' ' + shopee_product[1]
        shopee_product[2] = product_desc
        shopee_product[6] = settings.shopee_tw_default_ship_days
        shopee_product[7] = product_id

        local_freight = 8
        freight_tag = soup.find('div', class_='cost-entries-type')
        if freight_tag:
            local_freight = int(freight_tag.find('em', class_='value').string)

        weight = settings.shopee_tw_default_weight
        weight_tag = soup.find('div', class_='attributes-item mod-info kuajing-attribues')
        if weight_tag:
            w_tag = weight_tag.select('span em')
            weight += float(w_tag[0].string.replace(' kg',''))

        shopee_product[5] = weight
        # 查找产品价格及价格折扣
        # pricetag=soup.find('span', class_='value price-length-6')
        # # print(pricetag)
        # if not pricetag:
        #     pricetag=soup.find('div', class_='price-original-sku')
        # # print(pricetag)
        # productprice=pricetag.get_text()
        # if productprice.find('-') < 0:
        #     print('productprice:', productprice)
        # else:
        #     print('productprice[]:', productprice.split('-')[1].strip())
        print('开始解析产品选项...')
        # 查找产品attibutes及attributes相应的价格
        attrscontent = {}
        attr_list = []
        attr_one_part = soup.select('div.d-content div.obj-leading')
        # print(attr_one_part)
        if attr_one_part:
            # print('attr_one_part:[dddd]')
            for one_part in attr_one_part:
                # print(header)
                header_tag = one_part.find('span', class_='obj-title')
                attrkey = header_tag.string
                # print('attrkey:', attrkey)
                dllis = []
                list_tag = one_part.select('div.obj-content li a')
                for lli in list_tag:
                    # print(lli['title'])
                    dllis.append([lli['title']])
                attrscontent[attrkey] = dllis
                attr_list.append(dllis)
            # print(attrscontent)
        else:
            print('attr_one_part:[]')

        attr_sku_part = soup.select('div.d-content div.obj-sku')
        if attr_sku_part:
            for obj_sku in attr_sku_part:
                header_tag = obj_sku.find('span', class_='obj-title')
                attrkey = header_tag.string
                # print('attrkey:', attrkey)
                dllis = []
                list_tag = obj_sku.select('div.obj-content tr')
                for tr in list_tag:
                    # print(lli['title'])
                    name_span = tr.find('td', class_='name').find('span')
                    if name_span.string:
                        name = name_span.string
                    else:
                        name = name_span['title']
                    # print('name:', name)
                    price = tr.find('td', class_='price').find('em', class_='value').string
                    # print('price:', price)
                    count = tr.find('td', class_='count').find('em', class_='value').string
                    # print('count:', count)
                    if count != '0':
                        dllis.append([name, price, count])
                attrscontent[attrkey] = dllis
                attr_list.append(dllis)
        # print('attrscontent:', attrscontent)
        attr_values_array = reduce(get_attr_content, attr_list) if len(attr_list) > 0 else []
        # print('attr_values_array:', attr_values_array)
        vi = 1
        for attr_value in attr_values_array:
            if vi > 15:
                break
            vti = (vi - 1) * 4 + 1
            shopee_product[vti + 8] = str(product_id) + '-' + str(vi)
            shopee_product[vti + 9] = re.sub('[ ]+', ' ', attr_value[0])
            shopee_product[vti + 10] = str(settings.get_sale_price_for_tw(float(attr_value[1]) , local_freight))
            shopee_product[vti + 11] = 200
            vi += 1

        # 查找产品图片
        productimages = []
        # images = soup.select('div.tab-content-container')
        # print(images)
        print('开始解析产品图片...')
        ulimages = soup.select('div.tab-content-container div.vertical-img img')
        # print(ulimages)
        for img in ulimages:
            imgurl = img['src']
            if 'lazyload.png' in imgurl:
                imgurl = img['data-lazy-src']
            imgurl = imgurl.replace('.60x60.jpg', '.jpg')
            productimages.append(imgurl)
        # print(productimages)
        mi = 1
        mb = 1
        for img in productimages:
            # 判断是否要去掉此图片
            if str(mi) in exclude_imgs:
                # print('Imgs:', mi, '-', exclude_imgs)
                mi += 1
                continue
            if mb > 9:
                break
            # print('mb:',mb+68)
            shopee_product[mb + 68] = img
            mi += 1
            mb += 1
        if settings.use_html_file_or_browser==settings.HtmlParserTool.FILE:
            fp.close()
        # print('shopee_product:',shopee_product)
        print('完成解析产品...')
        return shopee_product

    def __del__(self):
        pass
