import requests
from django.core.cache import cache

# Extra helper functions
def gen_panel_data(query_set, panel_viewer):
    '''
    Takes a query set of panels and pre-processes them for rendering. The panel_viewer is who is viewing the panels for the purpose of checking if the person viewing them also owns them.
    '''
    all_panels = []
    for panel in query_set:
        if panel.panel_type == 'pie':
            # Make the pie panel
            title = f'{panel.user_name}/{panel.repo_name}'
            repo_url = f'https://github.com/{panel.user_name}/{panel.repo_name}'
            snippet = 'snippets/pie.html'
            api_url = f'https://api.github.com/repos/{panel.user_name}/{panel.repo_name}/languages'
        elif panel.panel_type == 'bar':
            # Make the bar panel
            title = f'{panel.user_name}/{panel.repo_name}'
            repo_url = f'https://github.com/{panel.user_name}/{panel.repo_name}'
            snippet = 'snippets/bar.html'
            api_url = f'https://api.github.com/repos/{panel.user_name}/{panel.repo_name}/languages'
        elif panel.panel_type == 'all':
            # Make the list of repos
            title = f'Table of repos for {panel.user_name}'
            repo_url = f'https://github.com/{panel.user_name}?tab=repositories'
            snippet = 'snippets/all_repos.html'
            api_url = f'https://api.github.com/users/{panel.user_name}/repos'
        elif panel.panel_type == 'star':
            # Make the list of repos
            title = f'Table of starred repos for {panel.user_name}'
            repo_url = f'https://github.com/{panel.user_name}?tab=repositories'
            snippet = 'snippets/starred_repos.html'
            api_url = f'https://api.github.com/users/{panel.user_name}/repos'
        
        # Check if cached
        cached_data = cache.get(str(panel.id))
        if cached_data:
            # Load from cache
            found = cached_data[0]
            data = cached_data[1]
        else:
            # Make API request
            response = requests.get(api_url)
            if response.status_code == 200:
                found = True
                data = response.json()
            else:
                data = None
            # Cache the data
            cache.set(str(panel.id), (found, data))
        
        all_panels.append({
            'is_owner' : panel.owner==panel_viewer,
            'id' : panel.id,
            'title' : title,
            'found' : found,
            'url' : repo_url,
            'snippet' : snippet,
            'data' : data,
            'size' : panel.size,
        })
        
    return all_panels

