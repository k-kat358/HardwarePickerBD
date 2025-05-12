from .forms import UserProfileForm
from django.shortcuts import render, redirect
from .models import UserProfile

def userprofile(request):
    return render(request, 'userprofile/profile.html')



def edit_profile(request):
    # Get the current user's profile or create one if it doesn't exist
    profile = UserProfile.objects.get(user=request.user)

    # Check if the form is submitted
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to a profile page (you can create this)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'userprofile/edit_profile.html', {'form': form})