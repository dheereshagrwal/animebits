from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Address
# Create your views here.
@login_required(login_url="/login")
def addresses(request):
    addresses = Address.objects.order_by("-updated_at").filter(user=request.user)
    context = {"addresses": addresses}
    return render(request, "addresses.html", context)