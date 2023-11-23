from django.contrib import auth
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
import openai
from django.utils import timezone

from Backend.models import chatdb
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
openai_api_key="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"
openai.api_key=openai_api_key
def index(request):
    return render(request,'index.html')
def ask_bot(message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="You are an helpful assistant.\nUser: " + message,
        max_tokens=150,
        temperature=0.7
    )
    print(response)
    answer = response.choices[0].text.strip()
    return answer


#def ask_bot(message):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are an helpful assistant."},
#             {"role": "user", "content": message},
#         ]
#     )
#     print(response)
#     answer = response.choices[0].message.content.strip()
#     return answer

@csrf_exempt
def chatbot(request):
    datas = chatdb.objects.filter(user=request.user.id).order_by('-date')[:1]

    if request.method == "POST":

        message = request.POST.get('message')

        if message:
            response = ask_bot(message)
            user = chatdb(user=request.user, message=message, response=response, date=timezone.now())
            user.save()
            return JsonResponse({'message': message, 'response': response})
        else:
            return JsonResponse({'error': 'Missing or empty "message" parameter in the request'}, status=400)

    return render(request, 'chatbot.html', {'datas': datas})


def register(request):
    return render(request,"Register_Login.html")

@csrf_exempt
def Register(request):
    if request.method == "POST":
        username = request.POST.get('name')
        email = request.POST.get('email')

        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                print(user)

                return redirect('chatbot')
            except Exception as e:
                error_message = e
                return render(request, "Register_Login.html", {'error_message': error_message})
        else:
            error_message = 'Passwords did not match'
            return render(request, "Register_Login.html", {'error_message': error_message})

    return render(request, "Register_Login.html")
def logout(request):
    auth.logout(request)
    return redirect(login)
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect(chatbot)
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
def history(request):
    data=chatdb.objects.filter(user=request.user).order_by('-date')
    return render(request,"history.html",{'data':data})
