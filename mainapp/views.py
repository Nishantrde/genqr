from django.shortcuts import render, redirect
from .models import *
from .qr_gen import generate_qr_code

def index(request):
    qr_img = None
    if request.method == "POST":
        site_add = request.POST.get("site")
        print(site_add)
        qr_img = generate_qr_code(site_add)
    return render(request, "index.html", {"photo":qr_img})

def visit(request, uuid):
    print(uuid)
    site = Qrcodes.objects.get(uuid=uuid)
    print(site.site)
    return redirect(site.site)


