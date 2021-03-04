from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code


# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile"
    )

    user_confirm = models.BooleanField(
        default=False,
    )

    affiliate_code = models.CharField(max_length=6, blank=True)

    recommended_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="ref_by"
    )

    packages_ready = models.IntegerField(blank=True, null=True)

    InTransit = models.IntegerField(blank=True, null=True)

    earnings = models.IntegerField(blank=True, null=True)

    signees = models.IntegerField(blank=True, null=True)

    address = models.CharField(
        max_length=100,
        null=True,
    )

    parish = models.CharField(
        max_length=100,
        null=True,
    )
    # trnnumber = models.CharField(max_length=100, null=True)
    mobilenumber = models.CharField(max_length=100, null=True)
    tier = models.CharField(max_length=100, default="Tier1")
    bankname = models.CharField(max_length=100, null=True)
    branchname = models.CharField(max_length=100, null=True)
    nameonbankaccount = models.CharField(max_length=100, null=True)
    accountnumber = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.user.username}-{self.affiliate_code}"

    def get_recommened_profiles(self):
        qs = Profile.objects.all()
        # my_recs = [p for p in qs if p.recommended_by == self.user]

        my_recs = []
        for profile in qs:
            if profile.recommended_by == self.user:
                my_recs.append(profile)
        return my_recs

    def save(self, *args, **kwargs):
        if self.affiliate_code == "":
            code = generate_ref_code()
            self.affiliate_code = code
        super().save(*args, **kwargs)
