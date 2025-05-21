from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Gender, Users
from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import login_required


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
            return redirect('/login')  # Redirect to the login page

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

                
                next_url = request.GET.get('next', '/user/list')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        except Users.DoesNotExist:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login/Login.html')

@login_required
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


@login_required
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


@login_required
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

@login_required   
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
    

@login_required
def user_list(request):
    q = request.GET.get('q', '')
    users = Users.objects.all()

    if q:
        users = users.filter(full_name__icontains=q)

    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/UserListUpdate.html', {'users': users_page})

    return render(request, 'user/UsersList.html', {'users': users_page})

@login_required
def add_user(request):
    try:
        if request.method == 'POST':
            # Get all form data
            form_data = {
                'full_name': request.POST.get('full_name'),
                'gender': request.POST.get('gender'),
                'birth_date': request.POST.get('birth_date'),
                'email': request.POST.get('email'),
                'address': request.POST.get('address'),
                'contact_number': request.POST.get('contact_number'),
                'other_phone_number': request.POST.get('other_phone_number'),
                'username': request.POST.get('username'),
            }
            
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, 'Password and confirm password do not match')
                # Return with form data and genders
                gender = Gender.objects.all()
                return render(request, 'user/AddUser.html', {
                    'genders': gender,
                    'form_data': form_data
                })

            try:
                Users.objects.create(
                    full_name=form_data['full_name'],
                    gender=Gender.objects.get(pk=form_data['gender']),
                    birth_date=form_data['birth_date'],
                    email=form_data['email'],
                    address=form_data['address'],
                    contact_number=form_data['contact_number'],
                    other_phone_number=form_data['other_phone_number'],
                    username=form_data['username'],
                    password=make_password(password),
                )
                messages.success(request, 'User added successfully')
                return redirect('/user/list')
                
            except IntegrityError as e:
                if 'username' in str(e):
                    messages.error(request, f'Username "{form_data["username"]}" already exists. Please choose a different username.')
                else:
                    messages.error(request, 'An error occurred while adding the user.')
                
                # Return with form data and genders
                gender = Gender.objects.all()
                return render(request, 'user/AddUser.html', {
                    'genders': gender,
                    'form_data': form_data
                })

        else:
            gender = Gender.objects.all()
            return render(request, 'user/AddUser.html', {'genders': gender})

    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {str(e)}')
        gender = Gender.objects.all()
        return render(request, 'user/AddUser.html', {'genders': gender})
    
@login_required
def edit_user(request, userId):
    try:
        
        user = Users.objects.get(pk=userId)

        if request.method == 'POST':
            
            fullName = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birth_date = request.POST.get('birth_date')
            email = request.POST.get('email')
            address = request.POST.get('address')
            contact_number = request.POST.get('contact_number')
            other_phone_number = request.POST.get('other_phone_number')
            username = request.POST.get('username')

            
            user.full_name = fullName
            user.gender = Gender.objects.get(pk=gender)
            user.birth_date = birth_date
            user.email = email
            user.address = address
            user.contact_number = contact_number
            user.other_phone_number = other_phone_number
            user.username = username

            try:
                
                user.save()
                messages.success(request, 'User updated successfully')
                return redirect('/user/list')
            except IntegrityError as e:
                
                if 'Duplicate entry' in str(e):
                    messages.error(request, f"An error occurred: Username '{username}' already exists.")
                else:
                    messages.error(request, "An unexpected error occurred while updating the user.")

                
                genders = Gender.objects.all()
                data = {
                    'user': user,
                    'genders': genders,
                    'form_data': request.POST  
                }
                return render(request, 'user/EditUser.html', data)

        else:
            
            genders = Gender.objects.all()
            data = {
                'user': user,
                'genders': genders
            }
            return render(request, 'user/EditUser.html', data)

    except Users.DoesNotExist:
        
        messages.error(request, "The user does not exist.")
        return redirect('/user/list')

    except Exception as e:
        
        messages.error(request, f"An unexpected error occurred: {e}")
        return redirect('/user/list')

@login_required
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

@login_required
def user_logout(request):
    request.session.flush()  
    messages.success(request, 'You have successfully logged out.')
    return redirect('/login')  