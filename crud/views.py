from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Gender

def gender_list(request):
    try:
         genders = Gender.objects.all()
         data = {
              'genders':genders
         }
         return render(request, 'gender/GendersList.html', data)

    except Exception as e:
        return HttpResponse(f"An error occurred while retrieving  the gender list: {e}")  

def add_gender(request):
    try:
        if request.method == 'POST':
             gender = request.POST.get('gender')
             Gender.objects.create(gender=gender).save()  
             messages.success(request, 'Gender added successfully')
             return redirect('/gender/list')            
        else:
            return render(request, 'gender/AddGender.html')       
    except Exception as e:
            return HttpResponse(f"An error occurred while adding a gender: {e}")     


def edit_gender(request, genderId):
    try:
        
        if request.method == 'POST':
            gender = Gender.objects.get(pk=genderId)
            gender_name = request.POST.get('gender')
            
            gender.gender = gender_name
            gender.save()
            messages.success(request, 'gender updated successfully')
            data = {
                'gender':gender
            }
            return render(request, 'gender/EditGender.html', data)
        else:
            gender = Gender.objects.get(pk=genderId)    
            data = {
                'gender':gender
            }

            return render(request, 'gender/EditGender.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred while editing gender: {e}")



def delete_gender(request, genderId):
    try:
        if request.method == 'POST':
            gender = Gender.objects.get(pk=genderId) 
            gender.delete()
            messages.success(request, 'Gender deleted successfully')
            return redirect('/gender/list')
        else:
            gender = Gender.objects.get(pk=genderId) 
            data = {
                'gender':gender
            }
            return render(request, 'gender/DeleteGender.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred while deleting gender: {e}")