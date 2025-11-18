# Assignment 9 – Cisco DNA Center Automation with Django & MongoDB

## Student Details
- Full Name: Gustavo Iserte Bonfim
- Student ID: CT1010953
  
## Project Overview
This project integrates Cisco DNA Center APIs with a Django web application and logs interactions into a MongoDB database.  
It was developed as part of IST105 Assignment 9.

The application provides a simple web interface to:
- Authenticate and display the Cisco DNA Center token.
- List network devices.
- Show interface details for a specific device IP.
- Log all interactions (timestamp, action, device IP, result) into MongoDB.

## Requirements
- Python 3.9+
- Django 3.2.25
- Requests
- PyMongo
- MongoDB running on a separate EC2 instance
- Amazon Linux 2 EC2 instances:
  - WebServer-EC2 → Django app
  - MongoDB-EC2 → MongoDB database

## Installation
1. Clone the repository:
   `git clone https://github.com/Iserte/ist105-assignment_9`
   `cd ist105-assignment_9`

2. Install dependencies:
   `pip3 install -r requirements.txt`

3. Configure Cisco DNA Center credentials in dnac_config.py:
   ```json
   DNAC = {
       "host": "sandboxdnac.cisco.com",
       "port": 443,
       "username": "devnetuser",
       "password": "Cisco123!"
   }
   ```

4. Configure MongoDB connection in `settings.py`.  
   Ensure MongoDB is running on your MongoDB-EC2 instance and accessible from the WebServer.

## Running the Application
Start the Django server:
   `python3 manage.py runserver 0.0.0.0:8000`

Access in browser:
   `http://<WebServer-EC2-Public-IP>:8000/`

## Application Routes
- `/token/` → Authenticate and show token
- `/devices/` → List network devices
- `/interfaces/?ip=<device-ip>` → Show interfaces for a device

## License
This project is for educational purposes only as part of IST105 coursework.