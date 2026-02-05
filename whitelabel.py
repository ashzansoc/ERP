import os
import re

# Define replacements
REPLACEMENTS = {
    "ERPNext": "Coredge ERP",
    "ERP Next": "Coredge ERP",
    "Frappe ERP": "Coredge ERP",
    "frappe ERP": "Coredge ERP",
    "Powered by Frappe": "Powered by Coredge ERP",
    "Frappe Technologies": "Coredge Technologies"
}

# Extensions to process
EXTENSIONS = ('.html', '.js', '.vue', '.css', '.json')

# Directories to skip
SKIP_DIRS = {'node_modules', 'dist', '__pycache__'}

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Perform replacements
        for old, new in REPLACEMENTS.items():
            content = content.replace(old, new)
            
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Modified: {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

def main():
    # Base path inside the container
    base_path = "/home/frappe/frappe-bench/apps"
    
    if not os.path.exists(base_path):
        print(f"Path {base_path} does not exist. Are we in the container?")
        # Fallback for testing or different paths
        base_path = os.getcwd()
        print(f"Using current directory: {base_path}")

    print(f"Starting whitelabeling in {base_path}...")
    
    for root, dirs, files in os.walk(base_path):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        
        for file in files:
            if file.endswith(EXTENSIONS):
                process_file(os.path.join(root, file))

    print("Whitelabeling completed.")
    
    # Try to clear cache if bench is available
    if os.system("which bench > /dev/null") == 0:
        print("Clearing bench cache...")
        os.system("bench clear-cache")
    else:
        print("Bench command not found, skipping cache clear.")

if __name__ == "__main__":
    main()
