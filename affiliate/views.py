from decimal import Context
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.views import generic
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.messages.api import success
from django.db.models import fields
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages

from profiles.token import account_activation_token
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.safestring import mark_safe

# custom imports here.
from profiles.forms import CreateUserForm, Editprofileform, EditBankInfo
from profiles.models import Profile


def signup_view(request):

    profile_id = request.session.get("ref_profile")
    print("profile_id", profile_id)

    user = User
    if request.user.is_authenticated:
        return redirect("profile")
    else:

        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)

            if form.is_valid():

                if profile_id is not None:
                    recommended_by_profile = Profile.objects.get(id=profile_id)

                    user = form.save(commit=False)
                    user.is_active = False
                    user = form.save()

                    registered_user = User.objects.get(id=user.id)
                    registered_profile = Profile.objects.get(user=registered_user)
                    registered_profile.recommended_by = recommended_by_profile.user
                    registered_profile.save()

                    try:

                        current_site = get_current_site(request)
                        subject = "'Activate Your SizExpress Account"
                        email_body = {
                            "user": user,
                            "domain": current_site.domain,
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "token": account_activation_token.make_token(user),
                        }

                        link = reverse(
                            "activate",
                            kwargs={
                                "uidb64": email_body["uid"],
                                "token": email_body["token"],
                            },
                        )

                        activate_url = "http://" + current_site.domain + link
                        email_from = settings.EMAIL_HOST_USER

                        email = EmailMessage(
                            subject,
                            "Hi "
                            + user.first_name
                            + ", Clik the link below to activate your SizExpress account \n"
                            + activate_url,
                            email_from,
                            [user.email],
                        )
                        email.send(fail_silently=False)
                        messages.success(
                            request,
                            (
                                "Please activate your account to login, Activation link was sent to your email.(Check Spam)"
                            ),
                        )
                    except:

                        messages.error(
                            request,
                            "Activation email wasn't sent to your email, Go ahead and login",
                        )

                    firstname = form.cleaned_data.get("first_name")

                    messages.success(
                        request, "Account was created for" + " " + firstname
                    )
                    return redirect("login")
                else:

                    user = form.save(commit=False)
                    user.is_active = False
                    user = form.save()

                    current_site = get_current_site(request)
                    subject = "'Activate Your SizExpress Account"
                    email_body = {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    }

                    link = reverse(
                        "activate",
                        kwargs={
                            "uidb64": email_body["uid"],
                            "token": email_body["token"],
                        },
                    )

                    activate_url = "http://" + current_site.domain + link
                    email_from = settings.EMAIL_HOST_USER

                    email = EmailMessage(
                        subject,
                        "Hi "
                        + user.first_name
                        + ", Clik the link below to activate your SizExpress account \n"
                        + activate_url,
                        email_from,
                        [user.email],
                    )
                    email.send(fail_silently=False)
                    messages.success(
                        request,
                        (
                            "Please activate your account to login, Activation link was sent to your email.(Check Spam)"
                        ),
                    )

                    firstname = form.cleaned_data.get("first_name")

                    messages.success(
                        request, "Account was created for" + " " + firstname
                    )
                    return redirect("login")

        context = {"form": form}
        return render(request, "register.html", context)


def main_view(request, *args, **kwargs):

    code = str(kwargs.get("ref_code"))
    try:
        profile = Profile.objects.get(affiliate_code=code)
        request.session["ref_profile"] = profile.id
        print("id", profile.id)
    except:
        pass
    print(request.session.get_expiry_age())
    return render(request, "home.html", {})


# Function to logout user from the website
def logoutPage(request):
    logout(request)
    return redirect("/")


# This is the function to display the users account page
@login_required(login_url="login")
def profile(request):

    profile = Profile.objects.get(user=request.user)
    my_recs = profile.get_recommened_profiles()
    index = 0
    for p in my_recs:
        index = index + 1
    index = index
    current_user = request.user

    earnings = profile.earnings

    Transit = profile.InTransit

    Ready = profile.packages_ready

    Tier = profile.tier

    Context = {
        "Profiles": Profile.objects.get(id=current_user.id),
        "my_recs": index,
        "earnings": earnings,
        "Transit": Transit,
        "Ready": Ready,
        "Tier": Tier,
    }

    return render(request, "profile.html", Context)


def rates(request):
    return render(request, "rates.html")


@login_required(login_url="login")
def profileInfo(request):

    if request.user.is_authenticated:
        if request.user.userprofile.user_confirm == True:
            return redirect("profile")

        e_P_F = Editprofileform()
        if request.method == "POST":
            e_P_F = Editprofileform(request.POST, instance=request.user.userprofile)

            if e_P_F.is_valid():
                request.user.userprofile.user_confirm = True
                request.user.save
                e_P_F.save()
                messages.success(request, "Account has been updated")
                return redirect("login")

        e_P_F = Editprofileform(instance=request.user.userprofile)
        context = {"e_P_F": e_P_F}
        return render(request, "profileinfo.html", context)


# Fuction to log in User into the website
def loginPage(request):

    if request.user.is_authenticated:

        if request.user.userprofile.user_confirm == False:
            return redirect("profileinfo")
        else:
            return redirect("profile")
    else:

        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if user is not None:

                # user.confirm_email.email_confirmed = True
                # print(user.confirm_email.email_confirmed)
                user.save()
                print("Person was logged in ")
                if user.is_active == True:

                    # if user.confirm_email.email_confirmed == True:
                    print("User is valid, active and authenticated")
                    login(request, user)
                    if request.user.userprofile.user_confirm == False:
                        return redirect("profileinfo")
                    else:
                        return redirect("profile")
                else:
                    print("The password is valid, but the account has been disabled!")
                    messages.info(
                        request,
                        mark_safe(
                            "Please activate your account to login, Activation link was sent to your email(Check Spam).  ",
                            # If u don't see activation email, Click link to Re-send Email <a href='resend_activation_email/'>CLICK HERE</a>
                        ),
                    )
            else:
                messages.info(request, "Incorrect Email or Password")

        context = {}
        return render(request, "login.html", context)


from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.generic import View, UpdateView


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            # user.confirm_email.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ("Your account have been confirmed."))
            return redirect("profile")
        else:
            messages.warning(
                request,
                (
                    "The confirmation link was invalid, possibly because it has already been used."
                ),
            )
            return redirect("home")

@login_required(login_url="login")
def Affiliate_account(request):
    profile = Profile.objects.get(user=request.user)

    bankname = profile.bankname
    branchname = profile.branchname
    accountname = profile.nameonbankaccount
    accountnumber = profile.accountnumber
    earnings = profile.earnings
    Context = {
        "bankname": bankname,
        "branchname": branchname,
        "accountname": accountname,
        "accountnumber": accountnumber,
        "earnings": earnings,
    }

    return render(request, "Affiliate_account.html", Context)

@login_required(login_url="login")
def Bank_account_update(request):

    if request.user.is_authenticated:

        Bank_info = EditBankInfo()
        if request.method == "POST":
            Bank_info = EditBankInfo(request.POST, instance=request.user.userprofile)

            if Bank_info.is_valid():

                request.user.save
                Bank_info.save()
                messages.success(request, "Account has been updated")
                return redirect("Affiliate_account")

        Bank_info = EditBankInfo(instance=request.user.userprofile)
        context = {"Bank_info": Bank_info}
        return render(request, "Bankupdate.html", context)
    else:
        return redirect("login")


# def resendmail(request):

#     user = User

#     if request.method == "POST":

#         current_site = get_current_site(request)
#         subject = "'Activate Your SizExpress Account"
#         email_body = {
#             "user": user,
#             "domain": current_site.domain,
#             "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#             "token": account_activation_token.make_token(user),
#         }

#         link = reverse(
#             "activate",
#             kwargs={
#                 "uidb64": email_body["uid"],
#                 "token": email_body["token"],
#             },
#         )

#         activate_url = "http://" + current_site.domain + link
#         email_from = settings.EMAIL_HOST_USER

#         email = EmailMessage(
#             subject,
#             "Hi "
#             + user.first_name
#             + ",Clik the link below to activate your SizExpress account \n"
#             + activate_url,
#             email_from,
#             [user.email],
#         )
#         email.send(fail_silently=False)
#         messages.success(
#             request,
#             (
#                 "Please activate your account to login, Activation link was sent to your email.(Check Spam)"
#             ),
#         )

#         messages.error(
#             request,
#             "Activation email wasn't sent to your email, Go ahead and login",
#         )

#         messages.success()
#         return redirect("resendmail")
#     return render(request, "resend_activation_email.html")

@login_required(login_url="login")
def withdrawalmail(request):

    user = request.user
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        pass

    else:
        try:
            subject = "Affilate Withdrawl Request"

            email_body = {
                "user": user,
            }

            email_from = settings.EMAIL_HOST_USER

            email = EmailMessage(
                subject,
                "Hey Admin"
                + " "
                + str(user.email)
                + " "
                + "Need Withdrawal of "
                + " "
                + "$"
                + str(profile.earnings),
                email_from,
                [email_from],
            )
            email.send(fail_silently=False)
            messages.success(
                request,
                ("Request sent!! please wait up to 24 to 36 hours for transfer"),
            )

            return redirect("Affiliate_account")
        except:
            messages.success(
                request,
                ("Request Not sent!! Please Contact SizExpress"),
            )
            return redirect("Affiliate_account")
    return render(request, "withdrawmail.html")