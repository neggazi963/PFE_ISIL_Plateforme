from django.db import models
from django.utils.translation import gettext_lazy as _

class BaseModel(models.Model):
    """Modèle de base avec champs communs"""
    created_at = models.DateTimeField(_('Date de création'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Date de modification'), auto_now=True)

    class Meta:
        abstract = True

class Contact(BaseModel):
    """Modèle pour les messages de contact"""
    name = models.CharField(_('Nom'), max_length=100)
    email = models.EmailField(_('Email'))
    subject = models.CharField(_('Sujet'), max_length=200)
    message = models.TextField(_('Message'))
    is_read = models.BooleanField(_('Lu'), default=False)

    class Meta:
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Newsletter(BaseModel):
    """Modèle pour les abonnements à la newsletter"""
    email = models.EmailField(_('Email'), unique=True)
    is_active = models.BooleanField(_('Actif'), default=True)

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')
        ordering = ['-created_at']

    def __str__(self):
        return self.email
