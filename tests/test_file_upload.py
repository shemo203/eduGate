from main import app, db, Student, Admin
import requests
import time
import threading
def test_single_file_upload(student_num, submission_id, base_url, results_list):
    session = requests.Session()
    start_time = time.time()
    
    try: 
        files = {'file': ('test.pdf', 'application/pdf')}
        response = session.post(f"/submissions/{submission_id}, files=files", files)
        success = response.status_code(200, 300)


    except Exception as e:
        print("exception")
def test_concurrent_file_upload():
    threads = []