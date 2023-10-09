
import sys
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
MW = 10



def traverse_tree(tree, path):
    result = subprocess.run(['git', 'ls-tree', tree], capture_output=True, text=True)
    for leaf in result.stdout.splitlines():
        _, type_, hash_, *name_parts = leaf.split()
        name = " ".join(name_parts)
        
        if not subprocess.run(['git', 'cat-file', '-e', hash_], capture_output=True).returncode == 0:
            print(f"[-] Failed to read object {hash_}")
            continue
        
        if type_ == "blob":
            print(f"[+] Found file: {path}/{name}")
            with open(f"{path}/{name}", "wb") as file:
                subprocess.run(['git', 'cat-file', '-p', hash_], stdout=file)
        else:
            print(f"[+] Found folder: {path}/{name}")
            os.makedirs(f"{path}/{name}", exist_ok=True)
            traverse_tree(hash_, f"{path}/{name}")

def handle_object(base, object_):
    result = subprocess.run(['git', 'cat-file', '-t', object_], capture_output=True, text=True)
    type_ = result.stdout.strip()
    
    if type_ == "commit":
        print(f"[+] Found commit: {object_}")
        path = f"{base}/{object_}"
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/commit-meta.txt", "wb") as file:
            subprocess.run(['git', 'cat-file', '-p', object_], stdout=file)
        traverse_tree(object_, path)


def main():
# Check for command line arguments    
    if len(sys.argv) == 4:                
        git_dir = sys.argv[1]
        dest_dir = sys.argv[2]
        MW = sys.argv[3]
    else:
        git_dir = input("Please enter the path to the git directory: ")
        dest_dir = input("Please enter the path to the destination directory: ")
        MW = input("Please enter threads num: ")

# Existing main function content (will be added below)

    os.chdir(git_dir)
    
# Correcting the object extraction process
    object_paths = subprocess.run(['find', '.git/objects', '-type', 'f', '!', '-path', '*.git/objects/pack/*'], capture_output=True, text=True).stdout.splitlines()
    objects = [path.replace(".git/objects/", "").replace("/", "") for path in object_paths]

    print(f"[+] Found {len(objects)} objects to process.")
    
    with ThreadPoolExecutor(max_workers=int(MW)) as executor:
        for object_ in objects:
            executor.submit(handle_object, dest_dir, object_)
    
# Placeholder for test
#main("/tmp/nep", "/tmp/nepo")
main()

