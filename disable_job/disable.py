import requests

def disable_job(jenkins_url, job_name, user, api_token):
    # Construct the URL to disable the job
    disable_url = f"{jenkins_url}/job/{job_name}/disable"
    
    # Make the POST request to disable the job
    response = requests.post(disable_url, auth=(user, api_token), verify=False)
    
    if response.status_code == 200:
        print(f"Successfully disabled job: {job_name}")
    else:
        print(f"Failed to disable job: {job_name}. Response: {response.text}")

if __name__ == "__main__":
    TARGET_JENKINS_URL = "https://your-jenkins-url/"
    USER = "user@email.com"
    API_TOKEN = "123456"

    with open("disable.txt", "r") as file:
        jobs_to_disable = [line.strip() for line in file]

    for job in jobs_to_disable:
        disable_job(TARGET_JENKINS_URL, job, USER, API_TOKEN)
