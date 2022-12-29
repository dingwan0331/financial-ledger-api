from django.http import JsonResponse

class ResponseExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return response

    def process_exception(self, request, exception):
        print(exception)

        try:
            if exception.__class__ == KeyError:
                return JsonResponse({'message' : 'Key error'}, status=400)

            if exception.is_custom:
                return JsonResponse({'message' : exception.message}, status=exception.status)

        except Exception as e:
            print(e)
            return JsonResponse({'message' : 'Server error'}, status=500)