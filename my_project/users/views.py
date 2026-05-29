from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Profile
from reviews.models import Review 
from .forms import CustomRegisterForm, ProfileForm


def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('users:profile')
    else:
        form = CustomRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=user_profile)

    user_reviews = Review.objects.filter(user=request.user).select_related('product')

    context = {
        'profile': user_profile,
        'form': form,
        'reviews': user_reviews
    }
    return render(request, 'users/profile.html', context)
