from django.db import models
from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth import get_user_model

# Panel Model:
# Provides all data for the construction and display of individual panels
# Panel are created by users and can live on dashboards
# Discrete choices for panel type
PANEL_CHOICES = [
            ('', 'Select a type of panel'),
            ('pie', 'Pie-panel of languages used in repo'),
            ('bar', 'Bar-panel of languages used in repo'),
            ('all', 'All repos for the user'),
            ('star', 'All starred repos for the user'),
        ]

# Discrete choices for panel size
SIZE_CHOICES = [
            ('', 'Select a size'),
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large'),
        ]
class Panel(models.Model):
    # Style of panel used (see above for options)
    panel_type = models.CharField(max_length=16, choices=PANEL_CHOICES)
    # GitHub username
    user_name = models.CharField(max_length=127)
    # GitHub repo name
    repo_name = models.CharField(max_length=127, blank=True)
    # Size of the panel
    size = models.CharField(max_length=16, choices=SIZE_CHOICES)

    # When it was created
    created_at = models.DateTimeField(editable=False)
    # When it was last updated
    updated_at = models.DateTimeField()

    # Owner of the panel
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # Many to many field with panels
    dashboards = models.ManyToManyField('Dashboard',blank=True, related_name='panels')

    class Meta:
        ordering = ['-updated_at']

    # Update the save method to automatically updated created_at and upadated_at
    def save(self, *args, **kwargs):
        ''' On save, update the timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(Panel, self).save(*args, **kwargs)

# Create your models here.
class Dashboard(models.Model):
    # Title of the dashboard
    title = models.CharField(max_length=255)
    # When it was created
    created_at = models.DateTimeField(editable=False)
    # When it was last updated
    updated_at = models.DateTimeField()

    # Owner of the dashboard
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="owner")
    # Liked dashboards
    liked = models.ManyToManyField(get_user_model(), related_name='liked_dashboards', blank=True)

    class Meta:
        ordering = ['-updated_at']

    # Update the save method to automatically updated created_at and upadated_at
    def save(self, *args, **kwargs):
        ''' On save, update the timestamps '''
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title