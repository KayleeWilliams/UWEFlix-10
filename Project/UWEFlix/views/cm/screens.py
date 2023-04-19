from django.shortcuts import redirect, render

from ...forms import ScreenForm
from ...models import Screen

# Create your views here.


def add_screen(request):

    if request.method == 'POST':
        # Get form inputs
        form = ScreenForm(request.POST)

        if form.is_valid():
            # Get form inputs
            capacity = form.cleaned_data['capacity']

            # Check not null
            for data in [capacity]:
                if data == None:
                    form.add_error(None, 'Please fill in all fields')
                    return render(request, 'cm/screens/form.html', {'form': form, 'action': 'Add'})

            # Create showing
            screen = Screen.objects.create(capacity=capacity)
            screen.save()

            return render(request, 'cm/success.html', {'message': 'Screen modified successfully', 'redirect': 'screens_management', 'redirect_text': 'Screen Management'})

    form = ScreenForm()
    return render(request, 'cm/screens/form.html', {'form': form, 'action': 'Add'})


def modify_screen(request):

    if request.method == 'POST':
        # Get form inputs
        form = ScreenForm(request.POST)

        if form.is_valid():
            # Get form inputs
            capacity = form.cleaned_data['capacity']

            # Check not null
            for data in [capacity]:
                if data == None:
                    form.add_error(None, 'Please fill in all fields')
                    return render(request, 'cm/screens/form.html', {'form': form, 'action': 'Modify'})

            # Create showing
            screen = Screen.objects.get(id=request.GET.get('screen'))
            screen.capacity = capacity
            screen.save()

            return render(request, 'cm/success.html', {'message': 'Screen modified successfully', 'redirect': 'screens_management', 'redirect_text': 'Screen Management'})

    form = ScreenForm()
    return render(request, 'cm/screens/form.html', {'form': form, 'action': 'Modify'})


def delete_screen(request):
    # Get screen
    screen = Screen.objects.get(id=request.GET.get('screen'))

    # Delete screen
    screen.delete()

    # Redirect to film dash
    return render(request, 'cm/success.html', {'message': 'Screen deleted successfully', 'redirect': 'screens_management', 'redirect_text': 'Screens Management'})
