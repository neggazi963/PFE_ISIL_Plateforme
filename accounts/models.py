from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""
    def _create_user(self,email,password,**extra_fields):
        
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_user(self,email,password,**extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,**extra_fields)
    
    def create_superuser(self,email,password,**extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        
        return self._create_user(email,password,**extra_fields)
        


class User(AbstractUser):
    """Custom User model for the Arabic NLP platform."""
    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=100)
    institution = models.CharField(_('institution'), max_length=255)
    country = models.CharField(_('country'), max_length=100)
    
    # Statut utilisateur
    is_researcher = models.BooleanField(_('researcher status'), default=False)
    is_developer = models.BooleanField(_('developer status'), default=False)
    is_student = models.BooleanField(_('student status'), default=False)
    is_verified = models.BooleanField(_('verified'), default=False)
    
    # Champs académiques
    academic_status = models.CharField(_('academic status'), max_length=100, blank=True)
    research_domains = models.JSONField(_('research domains'), default=list, blank=True)
    arabic_nlp_specialties = models.JSONField(_('Arabic NLP specialties'), default=list, blank=True)
    
    # Profil détaillé
    biography = models.TextField(_('biography'), blank=True)
    research_interests = models.TextField(_('research interests'), blank=True)
    publications = models.JSONField(_('publications'), default=list, blank=True)
    projects = models.JSONField(_('projects'), default=list, blank=True)
    
    # Préférences de langue et communication
    preferred_language = models.CharField(
        _('preferred language'),
        max_length=20,
        choices=[('ar', 'Arabic'), ('en', 'English'), ('fr', 'French')],
        default='ar'
    )
    
    # Permissions spécifiques
    can_upload_corpus = models.BooleanField(_('can upload corpus'), default=False)
    can_annotate = models.BooleanField(_('can annotate'), default=False)
    can_access_restricted_content = models.BooleanField(_('can access restricted content'), default=False)
    
    # Statistiques d'utilisation
    last_login_ip = models.GenericIPAddressField(_('last login IP'), null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_activity = models.DateTimeField(_('last activity'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'institution', 'country']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name.split()[0] if self.full_name else self.email

    def get_user_type(self):
        types = []
        if self.is_researcher:
            types.append('researcher')
        if self.is_developer:
            types.append('developer')
        if self.is_student:
            types.append('student')
        return types

    # Ajout des related_name pour résoudre les conflits
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_set',
        related_query_name='custom_user'
    )



