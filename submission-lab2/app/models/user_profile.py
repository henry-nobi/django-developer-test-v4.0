from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from app.models.user import User
from app.models.company import Company

class UserProfile(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='profiles'
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='user_profiles')
    display_name = models.CharField(_('display name'), max_length=255)
    avatar = models.CharField(_('avatar'), max_length=255, blank=True, null=True)
    default_language = models.CharField(_('default language'), max_length=10, default='en')
    is_primary = models.BooleanField(_('is primary'), default=False)
    created_at = models.DateTimeField(_('created at'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    is_active = models.BooleanField(_('is active'), default=True)

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        unique_together = ['user', 'company']

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Ensure only one primary profile per user
            UserProfile.objects.filter(
                user=self.user, 
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        
        # If this is the user's first profile, make it primary
        if not self.pk and not UserProfile.objects.filter(user=self.user).exists():
            self.is_primary = True
            
        super().save(*args, **kwargs)

    def activate(self):
        """
        Activate this profile and deactivate others
        """
        self.user.profile.all().update(is_active=False)
        self.is_active = True
        self.save()
