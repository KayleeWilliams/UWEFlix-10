from django.shortcuts import redirect, render

def account(request):
    if request.user.is_authenticated:
        # Print user perms
        # print(request.user.get_all_permissions(), flush=True)
        return render(request, 'account.html')
    else:
        # Redirect to login page
        return redirect('/login')
