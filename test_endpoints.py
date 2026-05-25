import requests
import os

BASE_URL = "http://localhost:8000"
RESUME_PATH = "/home/adityagautam/Desktop/Projects/resume-builder/Aditya_Gautam_Machine_Learning_Resume.pdf"
TEST_JD = "Looking for a Machine Learning Engineer with PyTorch, NLP, and LLM experience."

def test_parse_resume():
    print("Testing /parse-resume/ ...")
    with open(RESUME_PATH, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/parse-resume/",
            files={"file": ("resume.pdf", f, "application/pdf")}
        )
    print("Status:", response.status_code)
    try:
        print("Response JSON keys:", response.json().keys())
    except Exception as e:
        print("Response:", response.text)

def test_job_description():
    print("\nTesting /job-description/ ...")
    response = requests.post(
        f"{BASE_URL}/job-description/",
        data={"jd": TEST_JD}
    )
    print("Status:", response.status_code)
    print("Response:", response.text)

def test_tailored_resume():
    print("\nTesting /tailored-resume/ ...")
    with open(RESUME_PATH, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/tailored-resume/",
            files={"resume": ("resume.pdf", f, "application/pdf")},
            data={"jd": TEST_JD, "pages": 1, "template_name": "classic"}
        )
    print("Status:", response.status_code)
    print("Headers:", response.headers)
    if response.status_code == 200:
        print("Generated PDF size:", len(response.content), "bytes")
        with open("test_output.pdf", "wb") as out:
            out.write(response.content)
            print("Saved as test_output.pdf")
    else:
        print("Response:", response.text)

if __name__ == "__main__":
    import time
    time.sleep(2)  # wait for server to start
    test_parse_resume()
    test_job_description()
    test_tailored_resume()
