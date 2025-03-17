from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required  # Ensures only logged-in users can access the dashboard
def admin_dashboard(request):
    return render(request, 'admin_dashboard/dashboard.html')

@login_required
def admin_logout(request):
    logout(request)  # Logs out the user
    return redirect('login')  # Redirect to login page after logout
