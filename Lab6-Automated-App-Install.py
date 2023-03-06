import requests
import re
import hashlib
import os
import subprocess

def main():

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256()

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer()

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)

        # Delete the VLC installer from disk
        delete_installer(installer_path)

def get_expected_sha256():
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe.sha256'
    resp_msg = requests.get(file_url)

    if resp_msg.status_code == requests.codes.ok:
        file_content = resp_msg.text
        hash_regex = r'^([0-9a-fA-F]{64})\s'
        sha256 = re.match(hash_regex, file_content)
        if sha256:
            return sha256.group(1)
    return

def download_installer():
    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe'
    resp_msg = requests.get(file_url)

    if resp_msg.status_code == requests.codes.ok:
        file_content = resp_msg.content     
    return file_content

def installer_ok(installer_data, expected_sha256):
    installer_hash = hashlib.sha256(installer_data).hexdigest()
    installer = False
    
    if installer_hash == expected_sha256:
        installer = True
    return installer

def save_installer(installer_data):
    temp_dir = os.getenv('TEMP')
    file_name = 'vlc_installer.exe'
    saved_file_path = os.path.join(temp_dir, file_name)

    with open(saved_file_path,'wb') as file:
        file.write(installer_data)
        
    return saved_file_path

def run_installer(installer_path):
    subprocess.run([installer_path, '/L=1033', '/S'])
    return
    
def delete_installer(installer_path):
    os.remove(installer_path)
    return

if __name__ == '__main__':
    main()