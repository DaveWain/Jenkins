import requests

def enable_job(jenkins_url, job_name, user, api_token):
    # Construct the URL to enable the job
    enable_url = f"{jenkins_url}/job/{job_name}/enable"
    
    # Make the POST request to enable the job
    response = requests.post(enable_url, auth=(user, api_token), verify=False)
    
    if response.status_code == 200:
        print(f"Successfully enabled job: {job_name}")
    else:
        print(f"Failed to enable job: {job_name}. Response: {response.text}")

if __name__ == "__main__":
    TARGET_JENKINS_URL = "https://your-jenkins-url"
    USER = "user@email.com"
    API_TOKEN = "123456"

    with open("enable.txt", "r") as file:
        jobs_to_enable = [line.strip() for line in file]

    for job in jobs_to_enable:
        enable_job(TARGET_JENKINS_URL, job, USER, API_TOKEN)
