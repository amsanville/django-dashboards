import requests
from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.core.forms import CreateDashboardForm, EditDashboardForm, CreatePanelForm, AddPanelForm, EditPanelForm
from apps.core.models import Panel, Dashboard
from apps.core.helper import gen_panel_data

# Create your views here.
def home(request):
    '''
    View for the homepage
    '''
    context = {
        'title' : 'Home',
    }
    return render(request, 'core/home.html', context)

def all_dashboards(request):
    '''
    View all the dashboards on the site
    '''
    context = {
        'title' : 'All Dashboards',
        'all_dashboards' : Dashboard.objects.all(),
    }
    return render(request, 'core/all_dashboards.html', context)

###############################################################################
# DASHBOARD ###################################################################
###############################################################################
def view_dashboard(request, dashboard_id):
    # Get the dashboard
    curr_dashboard = Dashboard.objects.get(id=dashboard_id)
    
    # Process the panels
    panel_list = curr_dashboard.panels.all()
    print(panel_list)
    all_panels = gen_panel_data(panel_list, request.user)
    context = {
        'title' : curr_dashboard.title,
        'is_owner' : curr_dashboard.owner==request.user,
        'dashboard' : dashboard_id,
        'all_panels' : all_panels,
    }
    return render(request, 'core/view_dashboard.html', context)

@login_required
def create_dashboard(request):
    '''
    Create a new dashboard on the site
    '''
    # Process the form
    if request.method == 'POST':
        form = CreateDashboardForm(request.POST)
        # Validate the form
        if form.is_valid():
            # Populate the owner field
            dashboard = form.save(commit=False)
            dashboard.owner = request.user
            dashboard.save()

            messages.success(request, 'Dashboard created successfully, welcome to your new dashboard!')
            return redirect('view_dashboard', dashboard_id=dashboard.id)
    else:
        form = CreateDashboardForm()
    context = {
        'title' : 'Create New Dashboard',
        'form' : form,
    }
    return render(request, 'core/create_dashboard.html', context)

@login_required
def edit_dashboard(request, dashboard_id):
    '''
    Edit the dashboard
    '''
    # Retrieve the dashboard from the database
    curr_dashboard = Dashboard.objects.get(id=dashboard_id)
    
    # Set the initial context
    context = {
        'title' : 'Edit Dashboard',
        'is_owner' : False,
    }

    # Verify the user owns the dashboard
    if(curr_dashboard.owner == request.user):
        context['is_owner'] = True

        # Form Validation idiom
        if request.method == 'POST':
            form = EditDashboardForm(request.POST, instance=curr_dashboard)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully edited dashboard')
                
                # Since the form was validated, redirect back
                return redirect('view_dashboard', dashboard_id=dashboard_id)
        else:
            form = EditDashboardForm(instance=curr_dashboard)
        context['form'] = form
    return render(request, 'core/edit_dashboard.html', context)
    

@login_required
def delete_dashboard(request, dashboard_id):
    '''
    Delete the specified dashboard
    '''
    # Initialize the context
    context = {
        'title' : 'Delete Panel',
        'is_owner' : False,
    }

    # Load the panel
    curr_dashboard = Dashboard.objects.get(id=dashboard_id)
    # Verify that the user is the owner of the panel
    if(request.user == curr_dashboard.owner):
        context['is_owner'] = True

        # Process the form
        if request.method == 'POST':
            # Delete the panel
            if request.POST['action'] == 'Yes':
                curr_dashboard.delete()
            messages.warning(request, 'Dashboard deleted.')

            # Redirect back to where they were
            return redirect('view_profile', user_id=request.user.id)
    return render(request, 'core/delete_dashboard.html', context)

@login_required
def remove_panel(request, dashboard_id, panel_id):
    '''
    Removes a panel from a specific dashboard
    '''
    # Initialize the context
    context = {
        'title' : 'Remove Panel from Dashboard',
        'is_owner' : False,
    }

    # Get the panel and the dashboard
    curr_dashboard = Dashboard.objects.get(id=dashboard_id)
    curr_panel = Panel.objects.get(id=panel_id)

    # Verify that the user is the owner of the dashboard
    if(request.user == curr_dashboard.owner):
        context['is_owner'] = True
        # Process the modal
        if request.method == 'POST':
            # Remove the dashboard
            if request.POST['action'] == 'Yes':
                curr_panel.dashboards.remove(curr_dashboard)
            # Redirect back to the dashboard
            return redirect('view_dashboard', dashboard_id=curr_dashboard.id)
        
    return render(request, 'core/remove_panel.html', context)

###############################################################################
# PANEL #######################################################################
###############################################################################
@login_required
def create_panel(request):
    '''
    Creates a new panel for the user
    '''
    # Validate the form
    if request.method == 'POST':
        form = CreatePanelForm(request.POST, user=request.user)
        if form.is_valid():
            # Add the owner to the panel
            panel = form.save(commit=False)
            panel.owner = request.user
            panel.save()
            # Save many-to-many data for the form
            form.save_m2m()

            # Message for the user and redirect to profile
            messages.success(request, 'New panel created!')
            return redirect('view_profile', user_id=request.user.id)
    else:
        form = CreatePanelForm(user=request.user)
    
    # Set the context
    context = {
        'title' : 'Create Panel',
        'form' : form,
    }
    return render(request, 'core/create_panel.html', context)

@login_required
def add_panel(request, panel_id):
    '''
    Add panel to the specified dashboard.
    '''
    # Set the redirect
    if request.session.get('where_from', None) is None:
        request.session['where_from'] = request.META.get('HTTP_REFERER', '/')

    # Loads the instance of the panel panel
    curr_panel = Panel.objects.get(id=panel_id)
    
    # Validate the form
    if request.method == 'POST':
        form = AddPanelForm(request.POST, user=request.user, instance=curr_panel)
        if form.is_valid():
            # Save and message the user
            form.save()
            messages.success(request, 'Check the dashboard for changes.')
            
            # Return to the previous page
            temp = request.session['where_from']
            request.session['where_from'] = None
            return HttpResponseRedirect(temp)
    else:
        form = AddPanelForm(request.POST, user=request.user, instance=curr_panel)
    
    # Set the context
    context = {
        'title' : 'Add Panel',
        'form' : form,
    }
    return render(request, 'core/add_panel.html', context)

@login_required
def edit_panel(request, panel_id):
    '''
    Edit the panel specified.
    '''
    # Set the redirect
    if request.session.get('where_from', None) is None:
        request.session['where_from'] = request.META.get('HTTP_REFERER', '/')

    # Validate that the person editing the panel owns the panel
    context = {
        'title' : 'Edit Panel',
    }
    curr_panel = Panel.objects.get(id=panel_id)
    if request.user == curr_panel.owner:
        context['is_owner'] = True
        if request.method == 'POST':
            form = EditPanelForm(request.POST, instance=curr_panel)
            if form.is_valid():
                # Overwrite the
                form.save()
                messages.success(request, 'Successfully edited the panel.')
                # Return to the previous page
                temp = request.session['where_from']
                request.session['where_from'] = None
                return HttpResponseRedirect(temp)
        else:
            form = EditPanelForm(instance=curr_panel)
        context['form'] = form
    else:
        context['is_owner'] = False
    return render(request, 'core/edit_panel.html', context)

@login_required
def delete_panel(request, panel_id):
    '''
    Delete the specified panel
    '''
    # Set the redirect

    if request.session.get('where_from', None) is None:
        request.session['where_from'] = request.META.get('HTTP_REFERER', '/')

    # Initialize the context
    context = {
        'title' : 'Delete Panel',
        'is_owner' : False,
    }

    # Load the panel
    curr_panel = Panel.objects.get(id=panel_id)
    # Verify that the user is the owner of the panel
    if(request.user == curr_panel.owner):
        context['is_owner'] = True

        # Process the form
        if request.method == 'POST':
            # Delete the panel
            if request.POST['action'] == 'Yes':
                curr_panel.delete()
            messages.warning(request, 'Panel deleted.')

            # Redirect back to where they were
            temp = request.session['where_from']
            request.session['where_from'] = None
            return HttpResponseRedirect(temp)
    return render(request, 'core/delete_panel.html', context)