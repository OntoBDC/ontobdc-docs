
import sys
import json
import requests
from ontobdc.run.adapter.ui import BrowserConsoleFeedbackAdapter
from ontobdc.run.domain.port.ui import UserInterfaceFeedbackPort

browser_adapter: UserInterfaceFeedbackPort = BrowserConsoleFeedbackAdapter()
# Inject the adapter as the standard system output
sys.stdout = browser_adapter
sys.stderr = browser_adapter


def load_blog_container():
    print("Fetching RO-Crate metadata...")
    base_url = browser_adapter.get_base_url()
    crate_url = f"{base_url}/.__ontobdc__/ro-crate-metadata.json"
    
    try:
        response = requests.get(crate_url)
        response.raise_for_status()
        crate_data = response.json()
        
        posts = []
        
        # Simplified logic: Find all entities that are not the dataset itself
        # In a real scenario, you would search for @type = "Article" or similar
        for item in crate_data.get('@graph', []):
            type_ = item.get('@type', '')
            id_ = item.get('@id', '')
            
            # Skip the root and the metadata file itself
            if id_ in ['./', 'ro-crate-metadata.json']:
                continue
                
            # If it is a markdown, we consider it a post
            if id_.endswith('.md'):
                # Try to extract the title (if missing, use the formatted filename)
                title = item.get('name', id_.replace('.md', '').replace('-', ' ').title())
                
                # Build the viewing URL (here you would point to your MD reader)
                # For now, just point to the static file
                post_url = f"{base_url}/{id_}"
                
                posts.append({
                    "id": id_,
                    "title": title,
                    "date": item.get('datePublished', 'Recent'),
                    "excerpt": item.get('description', f"Content of file {id_}")[:100] + "...",
                    "url": post_url
                })
        
        print(f"✅ {len(posts)} posts found in the container.")
        
        # Send the JSON list back to JavaScript to render the HTML
        browser_adapter.renderBlogPosts(json.dumps(posts))
        
    except Exception as e:
        print(f"❌ Error reading remote container: {str(e)}")

load_blog_container()
