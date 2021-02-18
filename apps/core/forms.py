from django import forms
from django.forms import ModelForm
from apps.core.models import Panel, Dashboard
from django.contrib.auth import get_user_model

###############################################################################
# DASHBOARD ###################################################################
###############################################################################
# Form for creating a dashboard
class CreateDashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ['title']

class EditDashboardForm(forms.ModelForm):
    class Meta:
        model = Dashboard
        fields = ['title']

###############################################################################
# PANEL #######################################################################
###############################################################################

# Form for creating a panel
class CreatePanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ['panel_type', 'user_name', 'repo_name', 'size', 'dashboards',]

    # Modify the initialization to take a user to give dashboard options
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['dashboards'].queryset = Dashboard.objects.filter(owner=user)

# Form for adding a panel to a dashboard
class AddPanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ['dashboards',]

    # Modify the initialization to take a user to give dashboard options
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['dashboards'].queryset = Dashboard.objects.filter(owner=user)

# Form for editing a panel to a dashboard 
class EditPanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ['panel_type', 'user_name', 'repo_name', 'size']