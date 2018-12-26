from bs4 import BeautifulSoup

# fp = open('ali1688html/10004.html', encoding='gb18030')
# soup = BeautifulSoup(fp, features='html.parser')
#
# local_freight = 8
# freight_tag = soup.find('div', class_='cost-entries-type')
# if freight_tag:
#     local_freight=int(freight_tag.find('em', class_='value').string)
#
# print(local_freight)
#
# weight_tag = soup.find('div',class_='attributes-item mod-info kuajing-attribues').select('span em')
# print(float(weight_tag[0].string.replace(' kg','')))

a = [1, 2, 3, 4, 5, 6,7,8,9,10]
i=1
f=0
for ai in a:
    if f==1:
        f = 0
        continue
    if ai in(3,7):
        f=1
    if f==0:
        print(ai)
