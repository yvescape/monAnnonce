from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Categorie, Announce, Commentaire, Contact
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.auth.models import User,Group


def index(request):
    announces = Announce.objects.annotate(num_comments=Count('commentaire')).filter(status = 'True').order_by("-date_add")

    if request.method == 'GET':
        name = request.GET.get('query')
        if name is not None:
            announces = Announce.objects.annotate(num_comments=Count('commentaire')).filter(titre__icontains = name, status = 'True').order_by("-date_add")
            page = request.GET.get('page', 1)
            paginator = Paginator(announces, 2)
            try:
                announces = paginator.page(page)
            except PageNotAnInteger:
                announces = paginator.page(1)
            except EmptyPage:
                announces = paginator.page(paginator.num_pages)

    page = request.GET.get('page', 1)
    paginator = Paginator(announces, 2)
    try:
        announces = paginator.page(page)
    except PageNotAnInteger:
        announces = paginator.page(1)
    except EmptyPage:
        announces = paginator.page(paginator.num_pages)
    
    datas = {
        'announces': announces,
    }
    return render(request,'index.html',datas)


def post(request,id):
    announce = Announce.objects.get(id=id)
    categories = Categorie.objects.all()
    commentaires = Commentaire.objects.filter(announce_com =announce)
    user=request.user
    if request.method =='POST':
        message = request.POST.get('message')
        commentaire = Commentaire()
        commentaire.autor = user
        commentaire.announce_com = announce
        commentaire.commantaire = message
        commentaire.save()
        return redirect('post', id=announce.id)
    datas = {
        'announce': announce,
        'categories': categories,
        'commentaires': commentaires,
    }
    return render(request,'post.html',datas)


def about(request):
    return render(request,'about.html')


def contact(request):
    if request.method =='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact = Contact()
        contact.name = name
        contact.email = email
        contact.sujet = subject
        contact.contenu = message
        contact.save()
        return redirect('index')
    return render(request,'contact.html')


@login_required
def announce(request):
    user=request.user
    is_announceur = user.groups.filter(name='annonceurs').exists()
    announces = Announce.objects.annotate(num_comments=Count('commentaire')).filter(autor = user).order_by("-date_add")
    if request.method == 'GET':
        name = request.GET.get('query')
        if name is not None:
            announces = Announce.objects.annotate(num_comments=Count('commentaire')).filter(titre__icontains = name, autor = user).order_by("-date_add")
            page = request.GET.get('page', 1)
            paginator = Paginator(announces, 2)
            try:
                announces = paginator.page(page)
            except PageNotAnInteger:
                announces = paginator.page(1)
            except EmptyPage:
                announces = paginator.page(paginator.num_pages)

    page = request.GET.get('page', 1)
    paginator = Paginator(announces, 2)
    try:
        announces = paginator.page(page)
    except PageNotAnInteger:
        announces = paginator.page(1)
    except EmptyPage:
        announces = paginator.page(paginator.num_pages)
    datas = {
        'announces': announces,
        'is_announceur': is_announceur
    }
    return render(request,'my_announce.html',datas)


@login_required
@permission_required('announce.add_announce', raise_exception=True)
def createannounce(request):
    categories = Categorie.objects.all()
    user=request.user
    if request.method =='POST':
        titre = request.POST.get('titre')
        categorie = request.POST.get('categorie_select')
        image = request.FILES.get('image')
        video = request.FILES.get('video')
        contenu = request.POST.get('contenu')
        categorie_final = Categorie.objects.get(nom=categorie)
        announce = Announce()
        announce.titre = titre
        announce.categorie = categorie_final
        announce.image = image
        announce.video = video
        announce.contenu = contenu
        announce.autor = user
        announce.save()
        return redirect('announce')
    datas = {
        'categories': categories,
    }
    return render(request,'createannounce.html',datas)


@login_required
@permission_required('announce.change_announce', raise_exception=True)
def editannounce(request,id):
    announce = Announce.objects.get(id=id)
    categories = Categorie.objects.all()
    user=request.user
    if request.method =='POST':
        titre = request.POST.get('titre')
        categorie = request.POST.get('categorie_select')
        contenu = request.POST.get('contenu')
        categorie_final = Categorie.objects.get(nom=categorie)
        announce.titre = titre
        announce.categorie = categorie_final
        announce.contenu = contenu
        announce.status = 'False'
        announce.autor = user
        announce.save()
        return redirect('announce')
    datas = {
        'categories': categories,
        'announce': announce,
    }
    return render(request,'editannounce.html',datas)



@login_required
@permission_required('announce.delete_announce', raise_exception=True)
def supannounce(request,id):
    announce = Announce.objects.get(id=id)
    if request.method =='POST':
        announce.delete()
        return redirect('announce')
    datas = {
        'announce': announce,
    }
    return render(request,'supannounce.html',datas)


@login_required
def dev_ann(request):
    user=request.user
    if request.method =='POST':
        my_user = User.objects.get(username = user)
        role = Group.objects.get(name = 'annonceurs')
        my_user.groups.set([role])
        my_user.save()
        return redirect('announce')
    return render(request,'dev_annonceur.html')


def admin_site(request):
    announces = Announce.objects.all()
    if request.method =='POST':
        if 'form1_submit' in request.POST:
            titre = request.POST.get('titre')
            ad_app = Announce.objects.get(titre=titre)
            ad_app.status = 'True'
            ad_app.save()
            return redirect('admin_site')

        # Action pour le deuxième formulaire
        if 'form2_submit' in request.POST:
            titre = request.POST.get('titre')
            ad_app = Announce.objects.get(titre=titre)
            ad_app.delete()
            return redirect('admin_site')
        
        if 'form3_submit' in request.POST:
            titre = request.POST.get('titre')
            ad_app = Announce.objects.get(titre=titre)
            ad_app.status = 'False'
            ad_app.save()
            return redirect('admin_site')
    datas= {
        'announces': announces
    }
    return render(request,'admin.html',datas)