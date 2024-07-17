import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def delete_job(jenkins_url, job_name, user, api_token):
    # Construct the URL to delete the job
    delete_url = f"{jenkins_url}/job/{job_name}/doDelete"
    
    # Make the POST request to delete the job
    response = requests.post(delete_url, auth=(user, api_token), verify=False)
    
    if response.status_code == 200 or response.status_code == 302:  # Jenkins might redirect after deletion
        print(f"Successfully deleted job: {job_name}")
    else:
        print(f"Failed to delete job: {job_name}. Response: {response.text}")

if __name__ == "__main__":
    JENKINS_URL = "https://your-jenkins-url/"
    USER = "user"
    API_TOKEN = "123456"

    with open("jobs_to_delete.txt", "r") as file:
        jobs_to_delete = [line.strip() for line in file]

    for job in jobs_to_delete:
        delete_job(JENKINS_URL, job, USER, API_TOKEN)