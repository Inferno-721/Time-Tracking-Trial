import requests

API_BASE = "http://localhost:8000/api"

def login(email, password):
    resp = requests.post(f"{API_BASE}/employees/login", json={"email": email, "password": password})
    if resp.status_code == 200:
        return resp.json()
    return None

def get_projects(employee_id):
    resp = requests.get(f"{API_BASE}/projects/", params={"employee_id": employee_id})
    if resp.status_code == 200:
        return resp.json()
    return []

def log_time(employee_id, task_id, start_time, end_time=None, ip=None, mac=None):
    data = {
        "employee_id": employee_id,
        "task_id": task_id,
        "start_time": start_time,
        "end_time": end_time,
        "ip": ip,
        "mac": mac
    }
    resp = requests.post(f"{API_BASE}/time/", json=data)
    return resp.ok

def upload_screenshot(employee_id, image_bytes, permission_flag=True):
    import datetime
    data = {
        "employee_id": employee_id,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "image_data": image_bytes,
        "permission_flag": permission_flag
    }
    resp = requests.post(f"{API_BASE}/screenshots/", json=data)
    return resp.ok