from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *
from .qr_gen import generate_qr_code

def index(request):
    if request.method == "POST":
        site_add = request.POST.get("site")
        print(site_add)
        qr_img = generate_qr_code(site_add)
        # Save the QR code image or its identifier in session or database if you need to persist it
        request.session["qr_image"] = qr_img  # Example usage with session
        return HttpResponseRedirect(request.path_info)  # Redirect to the same page after POST
    else:
        qr_img = request.session.pop("qr_image", None)  # Retrieve QR image from session
        print("here")
    return render(request, "index.html", {"photo": qr_img})

def visit(request, uuid):
    print(uuid)
    site = Qrcodes.objects.get(uuid=uuid)
    print(site.site)
    return redirect(site.site)
