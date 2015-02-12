def simple_path(request):
    return {'path': request.path,
            'full_path': request.get_full_path()}
