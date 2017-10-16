from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Q

from .forms import PartTypeForm, EmailForm
from .models import PartType

def find(number=1, **conditions):
    try:
        return PartType.objects.filter(**conditions).exclude(quantity=0)[:number]
    except IndexError:
        return PartType.objects.filter(**conditions).exclude(quantity=0)

def home(request): #Gets list of all posts for homepage
    return render(request, 'manager/home.html', {'msg': 'dw'})

def contact(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        
        if form.is_valid():
            mail = form.cleaned_data
            
            send_mail(
                'Automated CFS Aero Parts Enquiry',
                'A user is interested in part ' + mail['part'] + '.Their message: ' + mail['msg'],
                mail['email'],
                ['admin@cfsaero.com'],
                fail_silently = False,
            )
            
            return render(request, 'manager/error.html', {'msg': "Thanks, we will be in touch as soon as possible"})

    else:
        part = request.GET.get('part', '')
        form = EmailForm()

    return render(request, 'manager/contact.html', {'form': form, 'part':part})    

def filter_match(request, function, search_): #used in search function to check if any parts match condition
    matchparts = list(filter(function, PartType.objects.all()))
    if matchparts: #if matches name or type
        return render(request, 'manager/part_list.html', {'parts':matchparts, 'query':search_})

    else:
        return "no match" 
   
#This function is hideous
#Have fun debugging :)
def search_parts(request):
    Search = request.GET.get('part')
    if not Search:
        return render(request, 'manager/home.html', {'msg': "Please enter a query"})
    Search = Search.lower()
    
    if PartType.objects.filter(number=Search): #if matches number
        return redirect('/parts/' + Search)

    parts = PartType.objects.filter(Q(number__icontains=Search)) #if in number
    
    if parts:
        return render(request, 'manager/part_list.html', {'parts':parts, 'query':Search})

    split = Search.split()

    find_my_results = [
        lambda x: Search == x.description.lower(),
        lambda x: Search in x.description.lower(),
        lambda x: all(word in (x.description + x.condition).lower() for word in split),
        lambda x: any(word in (x.description +  x.condition).lower() for word in split),
    ]

    for func in find_my_results:
        matches = filter_match(request, func, Search)
        if matches != "no match":
            return matches        

    return render(request, 'manager/home.html', {'msg': "We don't have any parts that match '" + Search + "' in stock, please check back soon or try something else"})

def admin(request):
    if request.user.is_authenticated():
        parts = PartType.objects.all()
        return render(request, 'registration/admin.html', {'parts':parts})

    else:
        return redirect('/login/')

def deal_with_multiple(parts, user):            
    if len(parts) > 1:
        for i in range(1, len(parts)): #iters through all except first
            if parts[0].my_str() == parts[i].my_str(): #if is duplicate, delete 2nd and add to quantity of first
                parts[0].quantity += parts[i].quantity
                parts[0].save()
                parts[i].delete()
                
            elif parts[0].my_str().split('---')[1] == parts[0].my_str().split('---')[1] and not user.is_authenticated():
                parts[0].quantity += parts[i].quantity
                parts = list(filter(lambda x: x != parts[i], parts))
    return parts

    
def part_detail(request, part_num):
    try:
        parts = PartType.objects.filter(number=part_num) #gets all part with correct number
        parts = deal_with_multiple(parts, request.user)
        return render(request, 'manager/part.html', {'parts': parts})

    except IndexError:
        return no_match(request)
        
@login_required
def new_type(request):
    if request.method == "POST":
        form = PartTypeForm(request.POST)
        if form.is_valid():
            part = form.save(commit=False)
            if PartType.objects.filter(number=part.number) and not 'already_tried' in request.session.keys():
                request.session['already_tried'] = 'yes'
                return render(request, 'manager/new_part.html', {'form': form, 'msg':'A part with that number already exists <a href="/parts/'+part.number+'">here</a>'})

            part.price = part.price.replace("£", "")
            part.save()
            return redirect('/parts/' + str(part.number))
    else:
        form = PartTypeForm()
        
    return render(request, 'manager/new_part.html', {'form': form})

@login_required
def edit_type(request, part_num, part_str=""):
    parts = PartType.objects.filter(number=part_num)
    parts = deal_with_multiple(parts, request.user)

    if part_str:
        parts = list(filter(lambda x: x.my_str() == part_str, parts))
        if not parts:
            return no_match(request)

    part = parts[0]
        
    if request.method == "POST":
        form = PartTypeForm(request.POST, instance=part)
        if form.is_valid():
            part = form.save(commit=False)
            
            part.price = part.price.replace(u'\u00a3', "")
            part.save()
            return redirect('/parts/' + str(part.number))
    else:
        form = PartTypeForm(instance=part)
        
    return render(request, 'manager/new_part.html', {'form': form})

@login_required
def delete_type(request, part_num, part_str=""):
    parts = PartType.objects.filter(number=part_num)
    parts = deal_with_multiple(parts, request.user)

    if part_str:
        parts = list(filter(lambda x: x.my_str() == part_str, parts))
        if not parts:
            return no_match(request)

    part = parts[0]

    part.delete()
        
    return redirect('/admin/')


def no_match(request):
    return render(request, 'manager/error.html', {'msg': "The page you're looking for doesn't exist"})
   
    
