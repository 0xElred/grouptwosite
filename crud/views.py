from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Gender, Users
from django.contrib.auth.hashers import check_password, make_password 
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator

def create_account(request):
    try:
        if request.method == 'POST':
            # Retrieve form data
            full_name = request.POST.get('full_name')
            gender_id = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            email = request.POST.get('email')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')
            other_phone_number = request.POST.get('other_phone_number')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Validate passwords
            if password != confirm_password:
                messages.error(request, 'Password and confirm password do not match.')
                return redirect('/createaccount')

            # Hash the password
            hashed_password = make_password(password)

            # Save the user to the database
            Users.objects.create(
                full_name=full_name,
                gender=Gender.objects.get(pk=gender_id),
                birth_date=birth_date,
                email=email,
                address=address,
                contact_number=contact_number,
                other_phone_number=other_phone_number,
                username=username,
                password=hashed_password,
            )
            messages.success(request, 'Account created successfully.')
            return redirect('/login')  # Redirect to the Users List page

        # Render the form for GET requests
        genders = Gender.objects.all()
        return render(request, 'login/CreateAccount.html', {'genders': genders})

    except Exception as e:
        return HttpResponse(f"An error occurred while creating the account: {e}")


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Users.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.user_id
                request.session['username'] = user.username
                messages.success(request, 'You have successfully logged in.')

                # Debugging the next parameter
                next_url = request.GET.get('next', '/user/list')
                print(f"Redirecting to: {next_url}")  # Debugging line
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        except Users.DoesNotExist:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login/Login.html')


def gender_list(request):

    search_query = request.GET.get('search', '')
    genders = Gender.objects.all()

    if search_query:
        genders = genders.filter(gender__icontains=search_query)

    paginator = Paginator(genders, 10)
    page_number = request.GET.get('page')
    genders_page = paginator.get_page(page_number)

    return render(request, 'gender/GendersList.html', {
        'genders': genders_page,
        'search_query': search_query,
    }) 


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



def user_list(request):
    q = request.GET.get('q', '')  # Get the search query
    users = Users.objects.all()  # Fetch all users initially

    if q:  # If a search query is provided, filter the users
        users = users.filter(full_name__icontains=q)

    # Add pagination
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    users_page = paginator.get_page(page_number)  # Get the users for the current page

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's an AJAX request
        return render(request, 'partials/UserListUpdate.html', {'users': users_page})

    # For non-AJAX requests, render the full page
    return render(request, 'user/UsersList.html', {'users': users_page})


def add_user(request):
    try:
        if request.method == 'POST':
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            email = request.POST.get('email')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')
            other_phone_number = request.POST.get('other_phone_number')
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, 'Password and confirm password do not match')
                return redirect('/user/add')

            Users.objects.create(
                full_name= fullName,
                gender= Gender.objects.get(pk=gender),
                birth_date=birth_date,
                email=email,
                address=address,
                contact_number=contact_number,
                other_phone_number=other_phone_number,
                username=username,
                password= make_password(password),
                
            ).save()  
            messages.success(request, 'User added successfully')
            return redirect('/user/list')      
        else:
            gender = Gender.objects.all()
            data = {
                'genders': gender 
            }
            return render(request, 'user/AddUser.html', data)


    except Exception as e:
        return HttpResponse(f"An error occurred while adding a user: {e}")


def edit_user(request, userId):
    try:
        # Retrieve the user by ID
        user = Users.objects.get(pk=userId)

        if request.method == 'POST':
            # Retrieve form data
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            email = request.POST.get('email')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')
            other_phone_number = request.POST.get('other_phone_number')
            username = request.POST.get('username')

            # Update user fields
            user.full_name = fullName
            user.gender = Gender.objects.get(pk=gender)
            user.birth_date = birth_date
            user.email = email
            user.address = address
            user.contact_number = contact_number
            user.other_phone_number = other_phone_number
            user.username = username

            try:
                # Save the updated user
                user.save()
                messages.success(request, 'User updated successfully')
                return redirect('/user/list')
            except IntegrityError as e:
                # Handle duplicate username error
                if 'Duplicate entry' in str(e):
                    messages.error(request, f"An error occurred: Username '{username}' already exists.")
                else:
                    messages.error(request, "An unexpected error occurred while updating the user.")

                # Re-render the form with the current data
                genders = Gender.objects.all()
                data = {
                    'user': user,
                    'genders': genders,
                    'form_data': request.POST  # Pass the submitted form data back to the template
                }
                return render(request, 'user/EditUser.html', data)

        else:
            # Render the form for GET requests
            genders = Gender.objects.all()
            data = {
                'user': user,
                'genders': genders
            }
            return render(request, 'user/EditUser.html', data)

    except Users.DoesNotExist:
        # Handle case where user does not exist
        messages.error(request, "The user does not exist.")
        return redirect('/user/list')

    except Exception as e:
        # Handle unexpected errors
        messages.error(request, f"An unexpected error occurred: {e}")
        return redirect('/user/list')

def delete_user(request, userId):
    try:
        user = Users.objects.get(pk=userId)

        if request.method == 'POST':
            user.delete()
            messages.success(request, 'User deleted successfully')
            return redirect('/user/list')

        data = {
            'user': user
        }
        return render(request, 'user/DeleteUser.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred while deleting the user: {e}")
