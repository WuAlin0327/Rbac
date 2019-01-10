from django.urls import reverse
from django.http import QueryDict
"""
保留原搜索条件的url以及解析原搜索条件

"""


def memory(request,name,*args,**kwargs):
    """
    生成带有原搜索条件的URL
    记忆上次访问状态
    :return:
    """
    basic_url = reverse(name,args=args,kwargs=kwargs)

    # 当前url中没有参数
    if not request.GET:
        return basic_url

    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()
    return "%s?%s"%(basic_url,query_dict.urlencode())


def memory_reverse(request,name,*args,**kwargs):
    """
    反向生成url
        - 在url中将原来的搜索条件获取
        - reverse生成原来的url，如/menu/menu_list
        - 拼接_filter的值
    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    """
    url = reverse(name,args=args,kwargs=kwargs)
    orgin_params = request.GET.get('_filter')
    if orgin_params:
        url = "%s?%s" % (url, orgin_params)
    return url
