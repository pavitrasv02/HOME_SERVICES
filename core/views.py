from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg, Prefetch
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import (
    User, ServiceProvider, Service, Booking, 
    Payment, Review, CookingService, VegDish, NonVegDish,
    SERVICE_TYPE_CHOICES, MenuItem, Bread
)


def home(request):
    # Get all services and organize them by type
    services = Service.objects.all().order_by('service_type', 'name')
    services_by_type = {}
    
    for service in services:
        if service.service_type not in services_by_type:
            services_by_type[service.service_type] = []
        services_by_type[service.service_type].append(service)
    
    providers = None
    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        location = request.POST.get('location')

        filter_kwargs = {}
        if service_type:
            filter_kwargs['service_type__icontains'] = service_type
        if location:
            filter_kwargs['location__icontains'] = location

        if filter_kwargs:
            providers = ServiceProvider.objects.filter(**filter_kwargs)
        else:
            providers = ServiceProvider.objects.all()
    
    context = {
        'services': services,
        'services_by_type': services_by_type,
        'providers': providers,
        'service_types': dict(SERVICE_TYPE_CHOICES),
    }
    return render(request, 'home.html', context)


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        pw = request.POST['password']
        pw2 = request.POST['confirm_password']
        if pw != pw2:
            return render(request, 'signup.html', {'error': 'Passwords do not match.'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered.'})
        user = User.objects.create(name=name, email=email, phone=phone, password=pw, address=address)
        request.session['user_id'] = user.id
        return redirect('home')
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        pw = request.POST['password']
        user = User.objects.filter(email=email, password=pw).first()
        if not user:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
        request.session['user_id'] = user.id
        return redirect('home')
    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('home')


def book_provider(request, provider_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    # Get the service first
    service = get_object_or_404(Service, id=provider_id)
    
    # Get available providers for this service
    providers = ServiceProvider.objects.filter(service_type=service.service_type)

    if request.method == 'POST':
        user_obj = User.objects.get(id=user_id)
        user_obj.name = request.POST['name']
        user_obj.email = request.POST['email']
        user_obj.phone = request.POST['phone']
        user_obj.address = request.POST['address']
        user_obj.save()

        booking_date = request.POST['booking_date']
        booking_time = request.POST['booking_time']
        provider = ServiceProvider.objects.filter(service_type=service.service_type, availability=True).first()

        Booking.objects.create(
            user=user_obj,
            provider=provider,
            service=service,
            booking_date=booking_date,
            booking_time=booking_time,
            status='Pending',
        )
        return redirect('booking_success')

    # Get selected food from session for cooking services
    selected_food = request.session.get('selected_food', []) if service.service_type == 'cooking' else None

    # Always flatten to a list of names and prices
    if isinstance(selected_food, str):
        selected_food = [item for item in selected_food.split(';') if item]
    elif isinstance(selected_food, list):
        # If it's a list with a single string with semicolons, split that string
        if len(selected_food) == 1 and isinstance(selected_food[0], str) and ';' in selected_food[0]:
            selected_food = [item for item in selected_food[0].split(';') if item]
        # If it's a list of strings, but some strings have semicolons, flatten them
        elif any(';' in s for s in selected_food):
            flat = []
            for s in selected_food:
                flat.extend([item for item in s.split(';') if item])
            selected_food = flat

    return render(request, 'book.html', {
        'service': service,
        'providers': providers,
        'selected_food': selected_food
    })


def booking_success(request):
    return render(request, 'success.html')


def view_bookings(request):
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = Booking.objects.filter(status=status_filter)
    else:
        bookings = Booking.objects.all()

    bookings = bookings.select_related('user', 'provider', 'service')
    return render(request, 'bookings.html', {
        'bookings': bookings,
        'status_filter': status_filter
    })


def my_bookings(request):
    uid = request.session.get('user_id')
    if not uid:
        return redirect('login')

    bookings = (
        Booking.objects
        .filter(user_id=uid)
        .select_related('provider', 'service')
        .prefetch_related(
            Prefetch('review_set',
                     queryset=Review.objects.all(),
                     to_attr='reviews')
        )
    )
    return render(request, 'my_bookings.html', {'bookings': bookings})


def leave_review(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    user_id = request.session.get('user_id')

    if not user_id or booking.user.id != user_id:
        return redirect('login')

    if booking.status != 'Completed':
        messages.error(request, "You can only leave a review for completed bookings.")
        return redirect('my_bookings')

    if request.method == 'POST':
        rating = int(request.POST['rating'])
        comment = request.POST['comment']
        Review.objects.create(
            booking=booking,
            rating=rating,
            comment=comment
        )

        # Update provider's average rating
        provider = booking.provider
        avg_rating = Review.objects.filter(booking__provider=provider).aggregate(Avg('rating'))['rating__avg']
        provider.rating = round(avg_rating or 0, 1)
        provider.save()

        return redirect('my_bookings')

    return render(request, 'review.html', {'booking': booking})


def provider_reviews(request, provider_id):
    provider = get_object_or_404(ServiceProvider, id=provider_id)
    reviews = Review.objects.filter(booking__provider=provider).select_related('booking__user')
    return render(request, 'provider_reviews.html', {
        'provider': provider,
        'reviews': reviews
    })


@csrf_exempt
def update_status(request, booking_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = new_status
        booking.save()
    return redirect('view_bookings')


def cooking_services(request):
    service_id = request.GET.get('service_id')
    service = None
    if service_id:
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            service = None
    flatbreads = [
        {'name': 'Roti', 'img': 'roti.jpg', 'price': 15},
        {'name': 'Chapati', 'img': 'chapati.jpg', 'price': 15},
        {'name': 'Paratha', 'img': 'paratha.jpg', 'price': 30},
        {'name': 'Naan', 'img': 'naan.png', 'price': 40},
        {'name': 'Phulka', 'img': 'phulka.jpg', 'price': 15},
        {'name': 'Kulcha', 'img': 'kulcha.jpg', 'price': 35},
        {'name': 'Tandoori Roti', 'img': 'tandoori.jpg', 'price': 45},
        {'name': 'Thepla', 'img': 'thepla.jpg', 'price': 25},
    ]
    curries = [
        {'name': 'Paneer Butter Masala', 'img': 'paneer.jpg', 'price': 250},
        {'name': 'Chana Masala', 'img': 'chana.jpg', 'price': 180},
        {'name': 'Aloo Gobi', 'img': 'aloo.jpg', 'price': 160},
        {'name': 'Baingan Bharta', 'img': 'Baingan_Bharta.webp', 'price': 170},
        {'name': 'Dal Tadka', 'img': 'Dal_Tadka.jpg', 'price': 150},
        {'name': 'Malai Kofta', 'img': 'malai.png', 'price': 280},
        {'name': 'Palak Paneer', 'img': 'palak.png', 'price': 260},
        {'name': 'Vegetable Korma', 'img': 'veg.jpg', 'price': 220},
    ]
    rice_items = [
        {'name': 'Biryani', 'img': 'biriyani.png', 'price': 200},
        {'name': 'Pulao (Pilaf)', 'img': 'pulao.png', 'price': 150},
        {'name': 'Jeera Rice', 'img': 'jeera.png', 'price': 120},
        {'name': 'Lemon Rice', 'img': 'lemon.png', 'price': 130},
        {'name': 'Khichdi', 'img': 'khichidi.png', 'price': 140},
        {'name': 'Fried Rice', 'img': 'fried.png', 'price': 160},
        {'name': 'Curd Rice', 'img': 'curd.png', 'price': 120},
        {'name': 'Tamarind Rice', 'img': 'tamarind.png', 'price': 130},
        {'name': 'Steamed Rice', 'img': 'steamed.png', 'price': 100},
        {'name': 'Saffron Rice', 'img': 'safforn.png', 'price': 180},
        {'name': 'Coconut Rice', 'img': 'coconut.png', 'price': 150},
        {'name': 'Vegetable Rice', 'img': 'veg_rice.png', 'price': 160},
    ]
    nv_flatbreads = [
        {'name': 'Roti', 'img': 'roti.jpg', 'price': 15},
        {'name': 'Chapati', 'img': 'chapati.jpg', 'price': 15},
        {'name': 'Paratha', 'img': 'paratha.jpg', 'price': 30},
        {'name': 'Naan', 'img': 'naan.png', 'price': 40},
        {'name': 'Phulka', 'img': 'phulka.jpg', 'price': 15},
        {'name': 'Kulcha', 'img': 'kulcha.jpg', 'price': 35},
        {'name': 'Tandoori Roti', 'img': 'tandoori.jpg', 'price': 45},
        {'name': 'Thepla', 'img': 'thepla.jpg', 'price': 25},
    ]
    nv_curries = [
        {'name': 'Butter Chicken', 'img': 'butter.png', 'price': 350},
        {'name': 'Chicken Curry', 'img': 'chicken.png', 'price': 280},
        {'name': 'Egg Curry', 'img': 'egg_curry.png', 'price': 200},
        {'name': 'Fish Curry', 'img': 'fish_curry.png', 'price': 300},
        {'name': 'Chicken Do Pyaza', 'img': 'chicken_do.png', 'price': 290},
        {'name': 'Chicken Chettinad', 'img': 'chicken_c.jpg', 'price': 320},
        {'name': 'Goan Fish Curry', 'img': 'fish_curry.png', 'price': 310},
        {'name': 'Prawn Masala', 'img': 'prawn.png', 'price': 380},
    ]
    nv_rice_items = [
        {'name': 'Chicken Biryani', 'img': 'chicken_briyani.png', 'price': 280},
        {'name': 'Egg Fried Rice', 'img': 'egg_frie.png', 'price': 180},
        {'name': 'Fish Pulao', 'img': 'fish_pulao.png', 'price': 250},
        {'name': 'Prawn Biryani', 'img': 'prawn_briyani.png', 'price': 350},
        {'name': 'Keema Rice', 'img': 'keema.png', 'price': 220},
        {'name': 'Chicken Pulao', 'img': 'chicken_palvo.png', 'price': 200},
        {'name': 'Mutton Biryani', 'img': 'mutton_briyani.png', 'price': 320},
        {'name': 'Egg Pulao', 'img': 'egg_pulao.png', 'price': 180},
    ]
    selected_food = request.session.get('selected_food', [])
    return render(request, 'core/cooking_services.html', {
        'flatbreads': flatbreads,
        'nv_flatbreads': nv_flatbreads,
        'curries': curries,
        'rice_items': rice_items,
        'nv_rice_items': nv_rice_items,
        'nv_curries': nv_curries,
        'user': request.user,
        'service': service,
        'selected_food': selected_food,
    })


def veg_dishes(request):
    dish_type = request.GET.get('dish_type')
    if dish_type:
        dishes = VegDish.objects.filter(dish_type=dish_type)
    else:
        dishes = VegDish.objects.all()
    return render(request, 'veg_dishes.html', {
        'dishes': dishes,
        'dish_type': dish_type
    })


def non_veg_dishes(request):
    dishes = NonVegDish.objects.all()
    return render(request, 'non_veg_dishes.html', {
        'dishes': dishes
    })


def add_dish(request):
    if request.method == 'POST':
        dish_type = request.POST.get('dish_type')
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        
        if dish_type == 'veg':
            dish_type = request.POST.get('veg_dish_type')
            VegDish.objects.create(
                name=name,
                dish_type=dish_type,
                description=description,
                price=price
            )
        else:
            NonVegDish.objects.create(
                name=name,
                description=description,
                price=price
            )
        return redirect('cooking_services')
    
    return render(request, 'add_dish.html')


def services(request):
    services = Service.objects.all()
    return render(request, 'core/services.html', {
        'services': services
    })


def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'service_detail.html', {
        'service': service
    })


@require_POST
def order_dish(request):
    if not request.session.get('user_id'):
        return JsonResponse({'status': 'error', 'message': 'Please log in to place an order'}, status=401)
    
    try:
        dish_type = request.POST.get('dish_type')
        dish_id = request.POST.get('dish_id')
        
        # Get the appropriate dish model
        if dish_type == 'veg':
            dish = get_object_or_404(VegDish, id=dish_id)
        else:
            dish = get_object_or_404(NonVegDish, id=dish_id)
        
        # Create a booking for the dish
        user = User.objects.get(id=request.session['user_id'])
        
        # Find a cooking service provider
        provider = ServiceProvider.objects.filter(
            service_type='cooking',
            availability=True
        ).first()
        
        if not provider:
            return JsonResponse({
                'status': 'error',
                'message': 'No cooking service providers available at the moment'
            }, status=400)
        
        # Create the booking
        booking = Booking.objects.create(
            user=user,
            provider=provider,
            service=Service.objects.get(service_type='cooking'),
            booking_date=timezone.now().date(),
            booking_time=timezone.now().time(),
            status='Pending'
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Order placed successfully',
            'booking_id': booking.id
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@login_required
def order_dish(request, dish_id):
    try:
        dish = VegDish.objects.get(id=dish_id)
        dish_type = 'veg'
    except VegDish.DoesNotExist:
        try:
            dish = NonVegDish.objects.get(id=dish_id)
            dish_type = 'non_veg'
        except NonVegDish.DoesNotExist:
            messages.error(request, 'Dish not found')
            return redirect('cooking_services')

    if request.method == 'POST':
        date = request.POST.get('date')
        time = request.POST.get('time')
        address = request.POST.get('address')
        special_instructions = request.POST.get('special_instructions')

        booking = Booking.objects.create(
            user=request.user,
            dish=dish if dish_type == 'veg' else None,
            non_veg_dish=None if dish_type == 'veg' else dish,
            dish_type=dish_type,
            date=date,
            time=time,
            address=address,
            special_instructions=special_instructions,
            total_amount=dish.price,
            status='Pending'
        )

        return redirect('booking_confirmation', booking_id=booking.id)

    return render(request, 'core/order_form.html', {
        'dish': dish,
        'dish_type': dish_type,
        'today': timezone.now().date()
    })


@login_required
def booking_confirmation(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'core/booking_confirmation.html', {
        'booking': booking
    })


def book_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    menu_items = MenuItem.objects.all()
    if request.method == 'POST':
        # ... get user details as per your form ...
        selected_items_ids = request.POST.getlist('menu_items')
        selected_items = MenuItem.objects.filter(id__in=selected_items_ids)
        total_price = sum(item.price for item in selected_items)
        # Create booking (add your user/provider logic as needed)
        booking = Booking.objects.create(
            service=service,
            total_price=total_price,
            # ... other fields ...
        )
        booking.menu_items.set(selected_items)
        # ... handle redirect or success ...
        return redirect('success')
    return render(request, 'book.html', {
        'service': service,
        'menu_items': menu_items,
    })


@csrf_exempt
def save_food_selection(request):
    if request.method == 'POST':
        food_items_str = request.POST.get('food_items', '')
        food_items = [item.strip() for item in food_items_str.split('||') if item.strip()]
        service_id = request.POST.get('service_id')
        
        if not food_items:
            messages.warning(request, 'Please select at least one food item.')
            return redirect('cooking_services')
        
        if not service_id:
            messages.error(request, 'Service ID missing. Please try again.')
            return redirect('cooking_services')
            
        request.session['selected_food'] = food_items
        return redirect('book_provider', provider_id=service_id)
    return redirect('cooking_services')
