import re
import requests
import random
from django.utils.safestring import mark_safe



def get_font():
    url = 'http://fontawesome.dashgame.com/#new'
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }
    response = requests.get(url=url,headers=headers)
    i_list = re.findall('<a class="col-xs-11">(.*?)<span class="sr-only">.*?</span>(.*?)</a>', response.text)
    font = []
    for i in i_list:
        font.append(['fa fa-' + i[1], mark_safe(i[0])])

    start_num = random.randrange(100,150)
    end_num = random.randrange(150,200)
    return tuple(font[start_num:end_num])
