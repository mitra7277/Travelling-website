from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from django.http import JsonResponse


from .forms import ContactForm
from service.models import ContactMessage, TravelHistory

ORS_API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjBhMGRkMmI5YmI5MTQ2M2M4MThiOTE5NGY5NTk5ZmM0IiwiaCI6Im11cm11cjY0In0="
# Replace with your ORS API key

# Cab page
def cab(request):
    return render(request, "cab.html")  # your template for cab booking

# Cab search API (AJAX call)
def cab_search(request):
    pickup_city = request.GET.get("pickup")
    drop_city = request.GET.get("drop")

    if not pickup_city or not drop_city:
        return JsonResponse({"error": "Pickup and Drop cities are required"}, status=400)

    try:
        # Geocode Pickup
        pickup_res = requests.get(
            "https://api.openrouteservice.org/geocode/search",
            params={"api_key": ORS_API_KEY, "text": pickup_city}
        ).json()
        pickup_coords = pickup_res["features"][0]["geometry"]["coordinates"]

        # Geocode Drop
        drop_res = requests.get(
            "https://api.openrouteservice.org/geocode/search",
            params={"api_key": ORS_API_KEY, "text": drop_city}
        ).json()
        drop_coords = drop_res["features"][0]["geometry"]["coordinates"]

        # Route summary
        route_res = requests.post(
            "https://api.openrouteservice.org/v2/directions/driving-car",
            headers={"Authorization": ORS_API_KEY, "Content-Type": "application/json"},
            json={"coordinates": [pickup_coords, drop_coords]}
        ).json()

        summary = route_res["routes"][0]["summary"]
        distance_km = round(summary["distance"] / 1000, 1)
        duration_min = round(summary["duration"] / 60)

        fares = {
            "Mini": distance_km * 10,
            "Sedan": distance_km * 15,
            "SUV": distance_km * 20
        }

        return JsonResponse({
            "pickup": pickup_city,
            "drop": drop_city,
            "distance_km": distance_km,
            "duration_min": duration_min,
            "fares": fares
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# --------- Pages ----------
def homePage(request):
    return render(request, "index.html", {'title': 'Home New'})

def about(request):
    return render(request, "about.html")

def insurance_view(request):
    return render(request, "insurance.html")

def index(request):
    return render(request, "index.html")

def travel_guides(request):
    # You can pass a list of guides if you want dynamic content
    guides = [
        {"name": "Rahul Sharma", "expertise": "Cultural Tours", "experience": 5},
        {"name": "Anita Verma", "expertise": "Adventure Trips", "experience": 7},
        {"name": "Vikram Singh", "expertise": "Heritage Walks", "experience": 4},
    ]
    return render(request, "travel_guides.html", {"guides": guides})

def cab(request):
    return render(request, "cab.html")

def weather(request):
    return render(request, "weather.html")

def hotel(request):
    return render(request, "hotel.html")

def package(request):
    return render(request, "package.html")

def profile(request):
    if not request.user.is_authenticated:
        return redirect("auth")
    return render(request, "profile.html")

def Help(request):
    return render(request, "Help.html")

def Course(request):
    return HttpResponse("Welcome to Wscubetech")

def add_history(request):
    return render(request, "add_history.html")  

def courseDetails(request, courseid):
    return HttpResponse(courseid)


# --------- Auth ----------
def auth_view(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "signup":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                return redirect("profile")  # go to profile after signup

        elif action == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("profile")
            else:
                messages.error(request, "Invalid credentials")

    return render(request, "auth.html")  # combined login/signup page


@login_required
def profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        if User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
            messages.error(request, "Username already taken!")
        else:
            request.user.username = username
            request.user.email = email
            request.user.save()
            messages.success(request, "Profile updated successfully!")

    return render(request, "profile.html")

# --------- Contact ----------
def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Your message has been sent successfully!")
            return redirect('contact')  # same page par reload karega
        else:
            messages.error(request, "❌ There was an error. Please try again.")
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def messages_list_view(request):
    messages_data = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'messages_list.html', {'messages': messages_data})
@login_required
def add_history(request):
    if request.method == "POST":
        place = request.POST.get("place")
        date = request.POST.get("date")
        trip_type = request.POST.get("trip_type")
        TravelHistory.objects.create(
            user=request.user,
            place=place,
            date_visited=date,
            trip_type=trip_type
        )
        return redirect("profile")