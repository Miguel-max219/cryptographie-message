from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.shortcuts import redirect, render

def home(request):
    return render(request, 'home.html')

def room(request, room):
    try:
        room_details = Room.objects.get(name=room)
    except Room.DoesNotExist:
        return HttpResponseNotFound("Cette salle n'existe pas.")
    
    username = request.GET.get('username', 'Anonyme')
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })  

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    room_obj, created = Room.objects.get_or_create(name=room)
    return redirect(f'/{room}/?username={username}')

def send(request):
    if request.method == "POST":
        username = request.POST.get("username")
        room_id = request.POST.get("room_id")
        message = request.POST.get("message")                                                                                                                                                                                                                                                                                                                                           

        room_obj = Room.objects.get(id=room_id)

        new_message = Message(value=message, user=username, room=room_obj)
        new_message.save()

        return HttpResponse("Message envoyé avec succès")
    
def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id).order_by('date')
    
    messages_data = [msg.get_decrypted() for msg in messages]

    users = list({msg['user'] for msg in messages_data})

    return JsonResponse({
        "messages": messages_data,
        "users": users
    })
