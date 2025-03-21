from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Notification(models.Model):
    """Modèle pour gérer les notifications des utilisateurs."""
    
    NOTIFICATION_TYPES = (
        ('project', _('Projet')),
        ('forum', _('Forum')),
        ('event', _('Événement')),
        ('resource', _('Ressource')),
        ('system', _('Système')),
    )

    PRIORITY_LEVELS = (
        ('low', _('Basse')),
        ('medium', _('Moyenne')),
        ('high', _('Haute')),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_('Destinataire')
    )
    
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        verbose_name=_('Type de notification')
    )
    
    title = models.CharField(
        max_length=255,
        verbose_name=_('Titre')
    )
    
    message = models.TextField(
        verbose_name=_('Message')
    )
    
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_LEVELS,
        default='medium',
        verbose_name=_('Priorité')
    )
    
    link = models.URLField(
        blank=True,
        null=True,
        verbose_name=_('Lien')
    )
    
    is_read = models.BooleanField(
        default=False,
        verbose_name=_('Lu')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Créé le')
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.title}"

    def mark_as_read(self):
        """Marquer la notification comme lue."""
        if not self.is_read:
            self.is_read = True
            self.save()
