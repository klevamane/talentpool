from dirtyfields import DirtyFieldsMixin
from django.contrib.auth import password_validation
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin, AbstractUser,
)
from django.core import signing
from django.db import models
from django.utils.translation import gettext_lazy as _

from talentpool.utils import TimeStampMixin, AddressMixin


class UserManager(BaseUserManager):
    """
    This manager class specifies
    how objects are created or retrieved

    Using a manage is also important in
    cases where we want to implement operations
    like "soft delete", "retrieve objects disregarding
    soft deleted ones"
    """
    def create_user(self, email, password, **extrafields):
        if not email:
            ValueError("Email field is required")
        user = self.model(
            email=self.normalize_email(email),
            password=password,
            **extrafields
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        # used by the PermissionsMixin to
        # grant all permissions
        extra_fields.setdefault("is_superuser", True)

        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_staff", True)
        user = self.create_user(email, password, **extra_fields)
        user.save(using=self.db)
        return user


AUTH_PROVIDERS = {
    "twitter": "twitter",
    "google": "google",
    "facebook": "facebook",
    "github": "github",
    "linkedin": "linkedin",
    "email": "email"
}


class User(DirtyFieldsMixin, AbstractBaseUser, PermissionsMixin, TimeStampMixin, AbstractUser):
    email = models.EmailField(
        max_length=50,
        unique=True,
        error_messages={"unique": "A user with this email already exists"},
    )
    password = models.CharField(
        max_length=128, validators=[password_validation.validate_password]
    )

    image = models.ImageField(
        blank=True, null=True, upload_to="images"
    )
    # we need to replace with is_staff
    is_admin = models.BooleanField(default=False)
    verification_status = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    auth_provider = models.CharField(max_length=255, blank=False, null=False, default=AUTH_PROVIDERS.get("email"))

    # ensure this is objects and not object
    # else User.objects.all() won't work
    # it has to be Model.objects.all()
    # and most 3rd party packages depend on objects
    objects = UserManager()

    REQUIRED_FIELDS = ["password"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return "{}".format(self.email)

    # def save(self, *args, **kwargs):
    #     return super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # allows assignment property to the image value
    # from the view
    def __setitem__(self, key, value):
        self.image = value

    @property
    def token(self):
        # refresh = RefreshToken.for_user(self)
        # return {
        #     "refresh": str(refresh),
        #     "access": str(refresh.access_token)
        # }
        pass


class Track(models.Model, TimeStampMixin):
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.name)


class Talent(User, AddressMixin):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    available = models.BooleanField(max_length=True)
    gender = models.CharField(max_length=6)
    date_of_birth = models.DateField(max_length=30)
    track = models.ForeignKey(to=Track, on_delete=models.SET_NULL)
    referred_by = models.ForeignKey("self", on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{}".format(self.firstname)


class Employeer(User, AddressMixin):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    industry_type = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    postalcode = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    email = models.CharField(max_length=40)
    tag = models.CharField(max_length=30)
    type = models.CharField(max_length=30)

    def __str__(self):
        return "{}".format(self.name)

