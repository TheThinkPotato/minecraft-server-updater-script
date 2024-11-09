import requests
import zipfile
import os
from getLink import get_latest_version_link
import shutil
import config

DOWNLOAD_FILE = config.DOWNLOAD_FILE
TEMP_FOLDER = config.TEMP_FOLDER
COPY_DESTINATION = config.SERVER_FOLDER

REMOVE_FILES = ["server.properties", "permissions.json", "whitelist.json, allowlist.json"]
REMOVE_FILES.append(DOWNLOAD_FILE)
zip_path = os.path.join(TEMP_FOLDER, DOWNLOAD_FILE)
VERSION = "1.0a"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

def get_link():
    # URL of the file to download
    url = get_latest_version_link()
    if url is None:
        exit()
    return url

# Create a temporary directory to store the downloaded file and extract it
# if folder exist remove it even if it not empty
def handle_folders():
    if not os.path.exists(COPY_DESTINATION):
        print( COPY_DESTINATION, "directory does not exist.")
        exit()
    if os.path.exists(TEMP_FOLDER):
        shutil.rmtree(TEMP_FOLDER)
    os.makedirs(TEMP_FOLDER, exist_ok=True)

# Path to save the downloaded zip file
def download_update(url):
    zip_path = os.path.join(TEMP_FOLDER, "downloaded_file.zip")

    # Download the file with headers
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure we notice bad responses

    # Write the content to a zip file
    with open(zip_path, "wb") as file:
        file.write(response.content)

# Download the file with headers
def download_file(url, headers, save_path):
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure we notice bad responses
    with open(save_path, "wb") as file:
        file.write(response.content)

# Extract the downloaded zip file
def extract_zip(zip_path):
    # Unzip the file to the temporary directory
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        print("> Extracting files...")
        zip_ref.extractall(TEMP_FOLDER)

# Copy files from temporary directory to server directory overwriting existing files
def copy_files():
    # Copy files from temporary directory to server directory overwriting existing files
    if not os.path.exists(COPY_DESTINATION):
        print( COPY_DESTINATION, "directory does not exist.")
        exit()

    print("> Copying files...")

    for root, dirs, files in os.walk(TEMP_FOLDER):
        # Calculate the relative path from the source to the current folder
        relative_path = os.path.relpath(root, TEMP_FOLDER)
        # Create the corresponding folder in the destination
        dest_dir = os.path.join(COPY_DESTINATION, relative_path)
        os.makedirs(dest_dir, exist_ok=True)  # Create subdirectories if they don't exist

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            shutil.copy(src_file, dest_file)
            # print(f"Copied {file} to {dest_dir}")

    # Remove the temporary directory
def remove_temp_folder():
    shutil.rmtree(TEMP_FOLDER)
    print("> Removed temporary directory")

def print_welcome():
    print("\n\n\tMinecraft Bedrock server update script", f"\t Current version: {VERSION}")
    print ("-"*80)
    print (f"Update Designation Directory:\t{COPY_DESTINATION}")
    print (f"Temporary Working Directory:\t{TEMP_FOLDER}")
    print ("-"*80)


if __name__ == "__main__":
    print_welcome()
    handle_folders()
    url = get_link()    
    download_file(url, headers, os.path.join(TEMP_FOLDER, DOWNLOAD_FILE))
    extract_zip(os.path.join(TEMP_FOLDER, DOWNLOAD_FILE))
    copy_files()
    remove_temp_folder()
    print ("-"*80)
    print("\n>> Update complete. \n\n")
