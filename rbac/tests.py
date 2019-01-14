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
# import re
# import requests
#
# url = 'http://fontawesome.dashgame.com/#new'
# response = requests.get(url=url)
# i_list = re.findall('<a class="col-xs-11">(.*?)<span class="sr-only">.*?</span>(.*?)</a>',response.text)
# font = []
# for i in i_list:
#     font.append(['fa-'+i[1],i[0]])
#
# print(tuple(font))


# 爬取墨迹天气并发送到微信
import wxpy
import requests
from lxml import etree

# def get_moji(url):
#     moji_page = requests.get(url=url).text
#     tree = etree.HTML(moji_page)
#     ul_list = tree.xpath('//div[@class="forecast clearfix"]/ul')
#     tianqi_str = ''
#     for ul in ul_list:
#         day = ul.xpath('./li[1]/a/text()')[0]
#         tianqi = ul.xpath('./li[2]/span/img/@alt')[0]
#         qiwen = ul.xpath('./li[3]/text()')[0]
#         feng = ul.xpath('./li[4]//text()')
#         feng_str = ''
#         for index,f in enumerate(feng):
#             if index in [1,3]:
#                 feng_str += f
#
#         tianqi_str += '%s  |%s  |%s  |%s \n'%(day,tianqi,qiwen,feng_str)
#
#     return tianqi_str
#
#
#
#
#
# if __name__ == '__main__':
#     city = input('请输入需要查询的城市(拼音):')
#     url = 'https://tianqi.moji.com/weather/china/jiangxi/'+city+'-district'
#

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


