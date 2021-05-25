from django.shortcuts import redirect

def index_redirect(request):
    ''' Redirect to Admin '''
    return redirect('admin/')