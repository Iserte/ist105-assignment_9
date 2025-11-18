from django.shortcuts import render
from dnac_config import DNAC
import requests
from requests.auth import HTTPBasicAuth
import urllib3
from .models import InteractionLog

urllib3.disable_warnings()

class DNAC_Manager:
    def __init__(self):
        self.token = None

    def get_auth_token(self):
        try:
            url = f"https://{DNAC['host']}:{DNAC['port']}/dna/system/api/v1/auth/token"
            response = requests.post(
                url,
                auth=HTTPBasicAuth(DNAC['username'], DNAC['password']),
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            self.token = response.json()['Token']
            InteractionLog.objects.create(action="auth", result="success")
            return self.token
        except Exception as e:
            InteractionLog.objects.create(action="auth", result=f"failure: {str(e)}")
            return None

    def get_network_devices(self):
        if not self.token:
            return []
        try:
            url = f"https://{DNAC['host']}:{DNAC['port']}/api/v1/network-device"
            headers = {"X-Auth-Token": self.token}
            response = requests.get(url, headers=headers, verify=False, timeout=10)
            response.raise_for_status()
            devices = response.json().get('response', [])
            InteractionLog.objects.create(action="devices", result="success")
            return devices
        except Exception as e:
            InteractionLog.objects.create(action="devices", result=f"failure: {str(e)}")
            return []

    def get_device_interfaces(self, device_ip):
        if not self.token:
            return []
        try:
            devices = self.get_network_devices()
            device = next((d for d in devices if d.get('managementIpAddress') == device_ip), None)
            if not device:
                return []
            url = f"https://{DNAC['host']}:{DNAC['port']}/api/v1/interface"
            headers = {"X-Auth-Token": self.token}
            params = {"deviceId": device.get('id') or device.get('instanceUuid')}
            response = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
            response.raise_for_status()
            interfaces = response.json().get('response', [])
            InteractionLog.objects.create(action="interfaces", device_ip=device.get('managementIpAddress'), result="success")
            return interfaces
        except Exception as e:
            InteractionLog.objects.create(action="interfaces", device_ip=device_ip, result=f"failure: {str(e)}")
            return []

# Django views
def show_token(request):
    dnac = DNAC_Manager()
    token = dnac.get_auth_token()
    return render(request, "token.html", {"token": token})

def list_devices(request):
    dnac = DNAC_Manager()
    dnac.get_auth_token()
    devices = dnac.get_network_devices()
    return render(request, "devices.html", {"devices": devices})

def show_interfaces(request):
    dnac = DNAC_Manager()
    dnac.get_auth_token()
    device_ip = request.GET.get("ip")
    interfaces = dnac.get_device_interfaces(device_ip)
    return render(request, "interfaces.html", {"interfaces": interfaces, "device_ip": device_ip})