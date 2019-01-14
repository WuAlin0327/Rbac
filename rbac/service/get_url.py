from collections import OrderedDict
from django.utils.module_loading import import_string
from django.conf import settings
from django.urls import URLPattern
from django.urls import URLResolver
import re
def check_url_exclude(url):
    """
    排除特定的url
    :param url:
    :return:
    """
    for reg in settings.AUTO_EXCLUDE_LIST:
        if re.match(reg,url):
            return True



def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    :param pre_namespace:获取namespace前缀，以后用于拼接name
    :param pre_url:url的前缀，以后用于拼接url
    :param urlpatterns:路由关系列表
    :param url_ordered_dict:用户保存递归中获取的所有路由
    :return:
    """
    for item in urlpatterns:

        if isinstance(item, URLPattern):  # 非路由分发,将路由添加到字典中
            if not item.name:
                continue
            # if pre_namespace:
            #     # name = '%s:%s' % (pre_namespace, item.name)
            # else:
            name = item.name
            url = pre_url + str(item.pattern)
            url = url.replace('^', '').replace('$','')
            if check_url_exclude(url):
                continue
            url_ordered_dict[name] = {'name': name, 'url': url}


        elif isinstance(item, URLResolver):  # 路由分发，递归操作
            if pre_namespace:
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace)
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            pattern = str(item.pattern)
            recursion_urls(namespace, pre_url + pattern, item.url_patterns, url_ordered_dict)


def get_all_url_dict():
    """
    获取项目中所有的URL
    :return:
    """
    url_ordered_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF)  # 以字符串形式导入模块，Root_Urlconf是url根目录
    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)

    return url_ordered_dict
