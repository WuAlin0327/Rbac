# import requests
# from lxml import etree
# import time
# headers={
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
# }
# img_dir = '/Users/wualin/Desktop/知乎'
# def get_url(url):
#     resopnse = requests.get(url=url,headers=headers)
#     tree = etree.HTML(resopnse.text)
#     img_url_list = tree.xpath('//div[@class="RichContent-inner"]/span/figure/img/@data-original')
#     return img_url_list
#
# def get_img(url):
#     response = requests.get(url=url,headers=headers).content
#     return response
#
# url='https://www.zhihu.com/question/41895584'
# response_list = get_url(url)
# for index,url in enumerate(response_list):
#     img_date = get_img(url)
#     time.sleep(3)
#     with open('%s/%s.png'%(img_dir,index),'wb') as f:
#         f.write(img_date)
#     print('下载一张图片成功')


# 爬取font Awesome图标
import re
import requests

url = 'http://fontawesome.dashgame.com/#new'
response = requests.get(url=url)
i_list = re.findall('<a class="col-xs-11">(.*?)<span class="sr-only">.*?</span>(.*?)</a>',response.text)
font = []
for i in i_list:
    font.append(['fa-'+i[1],i[0]])

print(tuple(font))


