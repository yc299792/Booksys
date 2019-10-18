from django.utils.deprecation import MiddlewareMixin

#要继承 MiddlewareMixin
class TestMiddleware(MiddlewareMixin):


    def __init__(self,a):
        super().__init__(a)
        print('---------ini-----')
    #
    def process_request(self, request):
        print('--------------request')

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('--------------view')

    def process_template_response(self, request, response):
        print('--------------template')
        return response

    def process_response(self, request, response):
        print('--------------response')
        return response
    # def get_response(self,response):
    pass