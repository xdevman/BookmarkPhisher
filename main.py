import json
import os


# Path to Chrome's Bookmarks file
bookmark_path = os.path.expanduser('~') + '/AppData/Local/Google/Chrome/User Data/Default/Bookmarks'
config_path = 'config.json'


# Function to read bookmarks
def read_bookmarks():
    with open(bookmark_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to write bookmarks
def write_bookmarks(bookmarks):
    with open(bookmark_path, 'w', encoding='utf-8') as file:
        json.dump(bookmarks, file, indent=4, ensure_ascii=False)

# Function to read config
def read_config():
    with open(config_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Function to find and replace URLs
def replace_url(bookmarks, replacements):
    changes = []
    
    def replace(bookmark, old_url, new_url):
        if old_url in bookmark.get('url', ''):
            original_url = bookmark['url']
            bookmark['url'] = new_url
            changes.append((bookmark['name'], original_url, new_url))
    
    def recursive_replace(children, old_url, new_url):
        for child in children:
            if 'children' in child:
                recursive_replace(child['children'], old_url, new_url)
            else:
                replace(child, old_url, new_url)

    for replacement in replacements:
        old_url = replacement['old_url']
        new_url = replacement['new_url']
        for root in bookmarks['roots'].values():
            if 'children' in root:
                recursive_replace(root['children'], old_url, new_url)

    return changes

# Main script execution
if os.path.exists(bookmark_path):
    bookmarks = read_bookmarks()
    config = read_config()
    
    # Print bookmarks before changes
    print("Bookmarks before changes:")
    for root in bookmarks['roots'].values():
        if 'children' in root:
            for child in root['children']:
                if 'url' in child:
                    print(f"{child['name']} - {child['url']}")
    
    # Replace URLs
    changes = replace_url(bookmarks, config['replacements'])
    
    # Write changes to the bookmarks file
    write_bookmarks(bookmarks)
    
    # Print changes
    if changes:
        print("\nChanges made:")
        for name, old_url, new_url in changes:
            print(f"{name}: {old_url} -> {new_url}")
    else:
        print("\nNo changes made.")
else:
    print('Bookmarks file not found.')
