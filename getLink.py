import requests
from bs4 import BeautifulSoup

VERSION_FILE = "version.ini"

def get_latest_version_link():
    # Define the URL and headers for the request
    url = "https://www.minecraft.net/en-us/download/server/bedrock"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    # Request the Minecraft Bedrock server download page
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the latest version download link
    download_link = ""
    for link in soup.find_all("a", href=True):
        if "bin-win" in link["href"]:  # Typical identifier for Windows server link
            download_link = link["href"]
            break

    # Store in a variable
    latest_version_link = f"{download_link}" if download_link else "Link not found"

    current_version = read_version_from_file()
    latest_version = latest_version_link.split("/")[-1]
    update_needed = current_version != latest_version
        
    print("> Current version:", current_version)
    print("> Latest  version:", latest_version)
    print("> Update needed:", update_needed)    
    print ( "-" * 80)
    if update_needed:
        print(">> Latest version download link:", latest_version_link)
        store_version_to_file(latest_version_link.split("/")[-1])
        return latest_version_link
    else:
        return None
    # store_version_to_file(latest_version_link.split("/")[-1])

def read_version_from_file():
    with open(VERSION_FILE, "r") as file:
        return file.read()

def store_version_to_file(version):
    with open(VERSION_FILE, "w") as file:
        file.write(version)

if __name__ == "__main__":
    print(get_latest_version_link())

