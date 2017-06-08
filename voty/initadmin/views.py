from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from account.models import SignupCodeResult, SignupCode
from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from datetime import datetime, timedelta
from django import forms

from .models import InviteBatch
from uuid import uuid4
from io import StringIO, TextIOWrapper
import csv

class UploadFileForm(forms.Form):
    file = forms.FileField()


def invite_em(file):
    site = Site.objects.get_current()
    total = newly_added = 0
    reader = csv.DictReader(file, delimiter=";")
    results = StringIO()
    writer = csv.DictWriter(results, fieldnames=["first_name","last_name","email_address_1","invite_code"])

    writer.writeheader()

    for item in reader:
        total += 1
        email = item['email_address_1']
        first_name = item['first_name']
        last_name = item['last_name']

        try:
            code = SignupCode.objects.get(email=email)
        except SignupCode.DoesNotExist:
            code = SignupCode(email=email,
                              code=uuid4().hex[:20],
                              max_uses=1,
                              sent=datetime.utcnow(),
                              expiry=datetime.utcnow() + timedelta(days=14))
            newly_added += 1
            code.save()

            EmailMessage(
                    'Dein Einladungscode zur DiB Abstimmungsplattform',
                    render_to_string('initadmin/email_invite.txt', context=dict(
                                     domain=site.domain,
                                     code=code,
                                     first_name=first_name)),
                    settings.DEFAULT_FROM_EMAIL,
                    [email]
                ).send()

        writer.writerow({
                "first_name": first_name,
                "last_name": last_name,
                "email_address_1": email,
                "invite_code": code.code
            })


    InviteBatch(payload=results.getvalue(), total_found=total, new_added=newly_added).save()

    return total, newly_added


@login_required
@user_passes_test(lambda u: u.is_staff)
def download_csv(request, id):
    batch = get_object_or_404(InviteBatch, pk=id)
    response = HttpResponse(batch.payload, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mass_invited.csv'
    return response

@login_required
@user_passes_test(lambda u: u.is_staff)
def mass_invite(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            total, send = invite_em(TextIOWrapper(request.FILES['file'].file, encoding=request.encoding))
            messages.success(request, "Coolio. Aus {} sind {} neue Einladungen versand worden".format(total, send))
    else:
        form = UploadFileForm()

    return render(request, 'initadmin/mass_invite.html', context=dict(form=form,
        invitebatches=InviteBatch.objects.order_by("-created_at")))