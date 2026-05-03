from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.cache import cache


class CachedQueryParamsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request:HttpRequest):
        response = self.get_response(request)
        if len(request.GET) > 0:
            path = request.path.replace("/","")
            items= "".join(f"{key}: {value}" for key,value in request.GET.items())
            if cache.has_key(path, 1):
                cache.set(path, items, 120, 1)
            else:
                cache.add(path, items, 120, 1)
            response.headers[path] = cache.get(path, "")
        return response
    
    
class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        print("SimpleMiddleware")
        print(request.path)

        if "except" in request.path:
            print("Catch word 'except' in request path — redirect to home")
            redirect_string = reverse("homePage")
            print(f"Redirecting to {redirect_string}")
         
            return HttpResponseRedirect(redirect_string)

        return self.get_response(request)
