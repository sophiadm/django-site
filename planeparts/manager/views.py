from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import PartTypeForm
from .models import PartType

def find(number=1, **conditions):
    try:
        return PartType.objects.filter(**conditions).exclude(quantity=0)[:number]
    except IndexError:
        return PartType.objects.filter(**conditions).exclude(quantity=0)

def filter_match(request, function, search_):
    matchparts = list(filter(function, PartType.objects.all()))
    if matchparts: #if matches name or type
        return render(request, 'manager/part_list.html', {'parts':matchparts, 'query':search_})

    else:
        return "no match" 
   
def home(request): #Gets list of all posts for homepage
    parts = find(number=2)
    return render(request, 'manager/home.html',{'parts': parts})

#This function is hideous
#Have fun debugging :)
#Eh I'll add some comments to help
def search_parts(request):
    Search = request.GET.get('part')
    if not Search:
        return render(request, 'manager/error.html', {'msg': "Please enter a query"})

    if PartType.objects.filter(number=Search): #if matches number
        return redirect('/parts/' + Search)

    parts = PartType.objects.filter(Q(number__icontains=Search)) #if in number
    
    if parts:
        return render(request, 'manager/part_list.html', {'parts':parts, 'query':Search})

    split = Search.split()

    find_my_results = [
        lambda x: Search in [x.itemtype, x.name],
        lambda x: Search in x.name + x.description,
        lambda x: all(word in x.name + x.description + x.itemtype + x.condition for word in split),
        lambda x: any(word in x.name + x.description + x.itemtype + x.condition for word in split),
    ]

    for func in find_my_results:
        matches = filter_match(request, func, Search)
        if matches != "no match":
            return matches        

    return render(request, 'manager/error.html', {'msg': "We don't have that part in stock, please check back soon :)"})

def admin(request):
    if request.user.is_authenticated():
        parts = PartType.objects.all()
        return render(request, 'registration/admin.html', {'parts':parts})

    else:
        return render(request, 'registration/login.html')
    
def part_detail(request, part_num):
    part = PartType.objects.filter(number=part_num)[0]
    if part:
        return render(request, 'manager/part.html', {'type': part})

@login_required
def new_type(request):
    if request.method == "POST":
        form = PartTypeForm(request.POST)
        if form.is_valid():
            part = form.save(commit=False)
            if PartType.objects.filter(number = part.number):
                return

            part.save()
            return redirect('/parts/' + str(part.number))
    else:
        form = PartTypeForm()
        
    return render(request, 'manager/new_part.html', {'form': form})

@login_required
def edit_type(request, part_num):
    part = get_object_or_404(PartType, number=part_num)
    if request.method == "POST":
        form = PartTypeForm(request.POST, instance=part)
        if form.is_valid():
            part = form.save()
            return redirect('/parts/' + str(part.number))
    else:
        form = PartTypeForm(instance=part)
        
    return render(request, 'manager/new_part.html', {'form': form})

@login_required
def delete_type(request, part_num):
    part = get_object_or_404(PartType, number=part_num)
    part.delete()
    return redirect('home')

"""
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
"""
