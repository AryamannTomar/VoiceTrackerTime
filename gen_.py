import os
import subprocess
from datetime import datetime

def get_custom_timestamp():
    now=datetime.now()
    hour=now.strftime('%I').lstrip('0')  
    minute=now.strftime('%M')
    am_pm=now.strftime('%p')
    day=now.strftime('%a')             
    month_day=now.strftime('%b%d')     
    return f"{hour}{minute}{am_pm}_{day}_{month_day}"

def run_git_commands():
    commit_message=get_custom_timestamp()
    try:
        subprocess.run(["git","add","."],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.run(["git","commit","-m",commit_message],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        subprocess.run(["git","push"],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print("❌ An error occurred while running git commands.",e)
    print("✅ git")
    
def generate_tree(start_path, indent=""):
    tree_str = ""
    try:
        items = sorted(os.listdir(start_path), key=str.lower)

        # filter out unwanted
        filtered_items = []
        for item in items:
            if (
                item in {".git", "rg_alias", "myenv", ".env", "Images", "FW__Contracts"} 
                or item.endswith(".py")
                or item.endswith(".jpg")
            ):
                continue
            filtered_items.append(item)

        for i, item in enumerate(filtered_items):
            path = os.path.join(start_path, item)
            is_last = (i == len(filtered_items) - 1)

            tree_str += indent + ("└── " if is_last else "├── ") + item + "\n"

            if os.path.isdir(path):
                tree_str += generate_tree(path, indent + ("    " if is_last else "│   "))
    except PermissionError:
        tree_str += indent + "└── **[ACCESS DENIED]**\n"
    return tree_str

if __name__=="__main__":
    tree_structure=generate_tree('.')
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write("DADS BIRTHDAY - SEPT 07 \n")
        f.write("```python\n")
        f.write("----- DIRECTORY STRUCTURE -----\n" + tree_structure)
        f.write("```\n")
    run_git_commands()