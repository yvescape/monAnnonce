from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

# Create your views here.
def inscription(request):
    roles = Group.objects.all()
    if request.method == "POST":
        role_select = request.POST['role_select']
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpwd = request.POST['comfirmpwd']
        if User.objects.filter(username=username):
            messages.error(request, "nom d'utilisateur déjà pris, veuillez en essayer un autre.")
            return redirect('inscription')
        if User.objects.filter(email=email):
            messages.error(request, 'Cet email a un compte.')
            return redirect('inscription')
        if len(username)>10:
            messages.error(request, "S'il vous plaît, le nom d'utilisateur ne doit pas contenir plus de 10 caractères.'")
            return redirect('inscription')
        if len(username)<5:
            messages.error(request, "S'il vous plaît, le nom d'utilisateur doit contenir au moins 5 caractères.")
            return redirect('inscription')
        if not username.isalnum():
            messages.error(request, "le nom d'utilisateur doit être alphanumérique.")
            return redirect('inscription')
        if password != confirmpwd:
            messages.error(request, 'Le mot de passe ne correspond pas!')  
            return redirect('inscription')  
        try:
            validate_password(password)
        except ValidationError as e:
            # Gérer les erreurs de validation du mot de passe
            messages.error(request, e)
            return redirect('inscription')
                        
        
        role = Group.objects.get(name = role_select)
        my_user = User.objects.create_user(username, email, password)
        my_user.first_name =firstname
        my_user.last_name = lastname
        my_user.groups.set([role]) 
        for permission in role.permissions.all():
            my_user.user_permissions.add(permission)
        # my_user.user_permissions.set([role.permissions.all(id)])
        my_user.is_active = True
        my_user.save()
        
        user = authenticate(username=username,password=password)
        if user is not None and user.is_active:
            login(request,user)
            #### redirection si les infos sont correctes
            return redirect('index')
    datas={
        'roles': roles
    }
    return render(request, 'inscription.html',datas) 


def connexion(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        password = request.POST.get("password")
        user = authenticate(username=name,password=password)
        if user is not None and user.is_active:
            login(request,user)
            if request.user.is_superuser:
                return redirect('admin_site')
            else:
                return redirect('index')
        else:
            print("login échoué")

    return render(request,"login.html")


def custom_logout(request):
    logout(request)
    # Rediriger vers la page d'accueil ou toute autre page souhaitée après la déconnexion
    return redirect('index') 


def modifie_mot_de_passe(request):
    user=request.user
    is_announceur = user.groups.filter(name='annonceurs').exists()
    if request.method == 'POST':
        password_old = request.POST.get("password_old")
        password_new_1 = request.POST.get("password_new_1")
        password_new_2 = request.POST.get("password_new_2")
        user_md = authenticate(username=user.username,password=password_old)
        if user_md is not None and user_md.is_active:
            if password_new_1 == password_new_2:
                user_md.password = password_new_1
                user_md.set_password(user_md.password)
                user_md.save()
                user_co = authenticate(username=user.username,password=password_new_1)
                login(request,user_co)
                return redirect('announce')
                
        else:
            messages.success(request, 'password_old not correct')
            return render(request,"change_password.html")
    datas= {
        'is_announceur': is_announceur
    }
    return render(request,"change_password.html",datas)