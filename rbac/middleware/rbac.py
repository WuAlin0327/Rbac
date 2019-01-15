from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect,render
from django.conf import settings
import re
class RbacMiddleware(MiddlewareMixin):
    """
    用户权限信息校验
    """
    def process_request(self,request):
        """
        当用户进入时触发执行
        1. 获取当前用户请求的url
        2. 获取当前用户在session保存的权限列表
        3. 进行匹配，判断用户请求的url是否在session保存的权限列表中
        :param request:
        :return:
        """

        request_url = request.path_info
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url,request_url):
                # 白名单的url无需权限验证
                return None

        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)

        if not permission_dict:
            return HttpResponse('请进行登陆')

        for url in settings.NO_PERMISSION_URL:
            if re.match(url,request_url):
                # 登陆后不需要权限就可以进行访问的
                request.selected_id = 0
                request.url_record = request_url
                return None



        flag = False

        url_record = [
            {'title':'首页','url':'#'},
        ]
        for item in permission_dict.values():
            reg = "^%s$"%item['url']
            if re.match(reg,request_url):
                # 利用正则进行匹配，匹配成功则说明是可以进行访问的
                flag = True
                # 将pid值传递到inclusion_tag中，去进行选中渲染
                request.selected_id = item['pid'] or item['id']

                if not item['pid']:
                    url_record.extend([
                        {'title': item['title'], 'url': item['url'],'class':'disabled'}
                    ])
                else:
                    url_record.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'],'class':'disabled'},
                    ])
                request.url_record = url_record
                break
        if not flag:
            response = render(request,'not_fount.html')
            response.status_code = 403
            return response




    #
    # def process_response(self,response):
    #     pass