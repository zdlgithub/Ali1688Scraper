
from ali1688shopeehtmlparse import DougHtmlParse
import os, settings, datetime, time
import openpyxl

if __name__ == '__main__':
    line_strings = []
    # 整理资料格式product_id;category_name;url
    url_file_path = os.path.join(settings.BASE_DIR,'datafiles','webpage1688url.csv')
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H')
    product_file_path = os.path.join(settings.BASE_DIR,'datafiles','shopee_products_'+current_datetime+'.xlsx')


    with open(url_file_path,'r') as fs:
        for fl in fs.readlines():
            line_strings.append(fl)
    print('开始')
    file_path = os.path.join(settings.BASE_DIR,'datafiles', 'shopee.xlsx')
    wb=openpyxl.load_workbook(file_path)
    # 切换到目标数据表
    # ws = wb[]
    ws=wb['Sheet1']

    product_id =''
    for ls in line_strings:
        urls=ls.split(';')
        try:
            product_id = urls[0]
            print('ProductID: %s begin' % product_id)
            dhp = DougHtmlParse()
            html_text = dhp.get_product_info(urls[0],urls[1],urls[2],urls[3])
        except Exception as e:
            print('Get URL Error:%s,ErrorInfo:%s' % urls[0],urls[2], repr(e))

        # 待填充数据
        ws.append(html_text)
        print('产品:', product_id, "处理完成")
        time.sleep(1)

    wb.save('shopee_products_'+current_datetime+'.xlsx')
    wb.close()
    print('数据处理完成,保存于:', 'shopee_products_'+current_datetime+'.xlsx')
