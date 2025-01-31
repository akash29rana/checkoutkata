from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def shopowner_required(func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  
        if not request.user.groups.filter(name='ShopOwners').exists():
            return HttpResponseForbidden("You do not have permission to access this page.")
        
        return func(request, *args, **kwargs)
    
    return wrapped