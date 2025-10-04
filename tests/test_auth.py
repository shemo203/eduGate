from main import app, db, Student, Admin
import requests
import time
from datetime import datetime
import threading

def single_login_test(student_num, base_url, results_list):
    session = requests.Session()
    start_time = time.time()
    
    try:
        response = session.post(f'{base_url}/login', data={
            'username': f'student{student_num}',
            'password': f'pass{student_num}'
        })

        login_time = time.time() - start_time
        success = response.status_code in [200, 302]

        results_list.append({
            'student' : student_num,
            'success' : success,
            'time' : login_time,
            'status': response.status_code
        })


    except Exception as e:
        results_list.append({
            'student': student_num,
            'success' : False,
            'error' : str(e),
            'time' : time.time() - start_time
        })

def test_30_concurrent_logins():
    base_url = "http://192.168.0.54:8080"
    results = []
    threads = []
    print("Testing 30 concurrent users")
    for i in range(1, 30):
        thread = threading.Thread(target=single_login_test, args = (i, base_url, results))
        threads.append(thread)
    
    start_time = time.time()
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()

    total_time = time.time() - start_time
    successful = [r for r in results if r['success']]
    
    print(f"Results: {len(successful)}/30 successful logins")
    print(f"Total time: {total_time:.2f} seconds")
    
    if len(successful) >= 27:  # 90% success rate
        print("PASS: App can handle classroom load")
    else:
        print("FAIL: Too many login failures")

if __name__ == "__main__":
    test_30_concurrent_logins()

