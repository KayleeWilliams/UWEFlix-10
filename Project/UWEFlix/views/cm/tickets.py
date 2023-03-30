from django.shortcuts import redirect, render

from ...forms import TicketForm
from ...models import Ticket

# Create your views here.


def add_ticket(request):

    if request.method == 'POST':
        # Get form inputs
        form = TicketForm(request.POST)

        if form.is_valid():
            # Get form inputs
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']

            # Check not null
            for data in [name, price]:
                if data == None:
                    form.add_error(None, 'Please fill in all fields')
                    return render(request, 'cm/tickets/form.html', {'form': form, 'action': 'Add'})
                
            # Create showing
            ticket = Ticket.objects.create(name=name, price=price)
            ticket.save()

            return render(request, 'cm/success.html', {'message': 'Ticket added successfully', 'redirect': 'tickets_management', 'redirect_text': 'Ticket Management'})

    form = TicketForm()
    return render(request, 'cm/tickets/form.html', {'form': form, 'action': 'Add'})


def modify_ticket(request):

    if request.method == 'POST':
        # Get form inputs
        form = TicketForm(request.POST)

        if form.is_valid():
            # Get form inputs
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']

            # Check not null
            for data in [name, price]:
                if data == None:
                    form.add_error(None, 'Please fill in all fields')
                    return render(request, 'cm/tickets/form.html', {'form': form, 'action': 'Modify'})

            # Create showing
            ticket = Ticket.objects.get(id=request.GET.get('ticket'))
            ticket.name = name
            ticket.price = price
            ticket.save()

            return render(request, 'cm/success.html', {'message': 'Ticket modified successfully', 'redirect': 'tickets_management', 'redirect_text': 'Ticket Management'})
    
    # Get ticket
    ticket = Ticket.objects.get(id=request.GET.get('ticket'))

    form = TicketForm(initial={'name': ticket.name, 'price': ticket.price})
    return render(request, 'cm/tickets/form.html', {'form': form, 'action': 'Modify'})


def delete_ticket(request):
    # Get ticket
    ticket = Ticket.objects.get(id=request.GET.get('ticket'))

    # Delete ticket
    ticket.delete()

    # Redirect to film dash
    return render(request, 'cm/success.html', {'message': 'Ticket deleted successfully', 'redirect': 'tickets_management', 'redirect_text': 'Ticket Management'})
