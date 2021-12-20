from ladon.server.wsgi import LadonWSGIApplication
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'appops.settings'  # 这里是项目的名称设置

application = LadonWSGIApplication(
    ['appapi.views'],  # 引用当前目录下views里的内容
    [os.path.join(os.path.dirname(__file__), os.path.pardir)],
    catalog_name='OPS APP API',
    catalog_desc='This is the root of my cool webservice catalog')