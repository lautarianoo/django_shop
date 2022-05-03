from django.shortcuts import render, redirect
from django.views import View
from .models import Room
from customer.models import Customer

class RoomView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        room = Room.objects.get(id=request.GET.get('sell'))
        if request.user not in room.members.all():
            return redirect('messages')
        context['messages'] = room.messages_room.order_by('date_add')
        context['room'] = room
        context['room_id'] = room.id
        context['company'] = room.company
        room.messages_room.filter(read=False).exclude(author=request.user).update(read=True)
        return render(request, 'messenger/room.html', context)

    def dispatch(self, request, *args, **kwargs):
        if not Room.objects.filter(id=kwargs.get('room_id'), customer=request.user.customer).exists() \
                and not Room.objects.filter(id=kwargs.get('room_id'), customer=request.user.company).exists():
            return redirect('catalog')
        return super().dispatch(request, *args, **kwargs)