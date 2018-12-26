"""
title:config item of project in this code page
date:2018-11-12
author:doug zhnag
description:

"""

import os
from enum import Enum, unique

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LIBRARY_BASE_PATH = os.path.join(BASE_DIR, 'library')

SCRAPER_SLEEP_TIME = 5

MY_DOMAIN = 'Athereshopping'
ALIEXPRESS_DOMAIN = r'\n|[aA]liexpress|[aA]libaba'


@unique
class Browser(Enum):
    CHROME = 1
    FIREFOX = 2


@unique
class HtmlParserTool(Enum):
    FILE = 1
    BROWSER = 2


# 售价计算公式参数输入成本价，运费
def get_sale_price_for_tw(unit_price, freight):
    return (unit_price + freight) * 4.6 * 1.1 + 30


# 设置运行浏览器是否弹出窗口
browser_handless_default = True
# 设置浏览器驱动Browser.CHROME Browser.FIREFOX
BASE_BROWSER = Browser.FIREFOX
# 设置解析方式 1.使用浏览器 HtmlParserTool.BROWSER 2.使用.html文件 HtmlParserTool.FILE
use_html_file_or_browser = HtmlParserTool.BROWSER

# 过滤产品描述中的字符串
product_property_field_names = ['建议零售价', '主要下游平台', '主要销售地区', '是否跨境货源', '通讯类型', '加工定制',
                                '加工方式', '加印LOGO', '是否支持混批',
                                '是否支持一件代发', '发票', '售后服务', '是否专利货源']
# 过滤标题中的词语
filter_title_name = '心率表|测脉搏心跳'
# 增加标题中的字段
add_title_field_name = ['品牌', '型号']
# default weight 0.05kg
shopee_tw_default_weight = 0.05
# default ship days
shopee_tw_default_ship_days = 2
