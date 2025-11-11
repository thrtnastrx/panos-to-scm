### To run the python script directly:
### Step 1: Clone the Repository

```bash
git clone https://github.com/thrtnastrx/panos-to-scm.git
cd panos-to-scm
```

### Step 2: Create a VENV and Install the Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Step 3: Executing complete_migration_gui.py for PAN-OS
- Run "complete_migration_gui.py"
- The GUI will prompt you for your SCM IAM account information and the Panorama information and will create the .yaml file in the working directory

- **Common Services IAM account**
  - **Generate Service Account** Directions -> https://docs.paloaltonetworks.com/common-services/identity-and-access-access-management/manage-identity-and-access/add-service-accounts

- Additionally add your PANOS NGFW/Panorama URL(make sure it ends in `/api/`) , Password and API Key
    - If you don't have API key for PANOS, the script will fetch API key and update config file
    - Optionally, you can ommit username/password and only apply the API key

```yaml
---
client_id: enter-username
client_secret: xxxxxxxxxxxxxxxxxxxxxx
tsg_id: enter-unique-tsg-here
palo_alto_ngfw_url: https://x.x.x.x/api/
palo_alto_password: service_account_password
palo_alto_username: service_account_name
palo_api_token: xxxxxxxxxxxxxxxxxxxxxx
```

### Currently Supported PAN-OS Migration Features:

- **External Dynamic List**
- **Custom URL Categories**
- **URL Filter Profiles**
- **Vulnerability Profiles**
- **Anti-Spyware Profiles**
- **DNS Security Profiles**
- **File Blocking Profiles**
- **Decryption Profiles**
- **Profile Groups**
- **Tags**
- **Address Objects**
- **Address Groups**
- **Service Objects**
- **Service Groups**
- **Applications**
- **Application Filters**
- **Application Groups**
- **HIP Objects**
- **HIP Profiles**
- **Security Rules**
- **NAT Rules**
- **Application Override Rules**
- **Decryption Policy Rules**

### To Use
1.  Create a folder in SCM named "Addresses" or "Services", etc. (you can clone or move anything to Global or any other folder once the migrations are complete)
2.  Select only "Addresses" first and on the Migration tab set folder name to "Addresses"
3.  Start Migration
4.  You can verify in the app and in SCM as the migration is live
5.  Create Groups in the same folder as the objects
6.  Optionally just create one folder and import everything into that folder, then move or duplicate as needed.
7.  NOTE: Do not create new folders in SCM while the migration is live, or the app will crash with "RecursionError: maximum recursion depth exceeded while calling a Python object".
8.  If the app crashes during migration of over 5000 objects, just relaunch it and it will continue from where it left off.

## Screenshots
<img width="1400" height="928" alt="Image" src="https://github.com/user-attachments/assets/785d0fef-e813-4d77-a625-917d1b5992d6" />
<img width="1453" height="1319" alt="Image" src="https://github.com/user-attachments/assets/21bea20a-b341-429b-a669-5409e8d97fa4" />
<img width="1411" height="933" alt="Image" src="https://github.com/user-attachments/assets/63ed9ed5-6860-4869-9969-16daa3bbcba8" />
<img width="1411" height="933" alt="Image" src="https://github.com/user-attachments/assets/81133281-a0a7-4a5a-8f8b-cc2c1c38a91d" />
<img width="1411" height="933" alt="Image" src="https://github.com/user-attachments/assets/a852bbff-1022-4327-9278-dc5f156c5175" />
