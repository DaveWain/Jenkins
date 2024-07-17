import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def migrate_job(source_jenkins_url, target_jenkins_url, job_name, source_user, source_api_token, target_user, target_api_token):
    # Fetching the job config from source Jenkins
    source_url = f"{source_jenkins_url}/job/{job_name}/config.xml"
    response = requests.get(source_url, auth=(source_user, source_api_token), verify=False)
    
    if response.status_code != 200:
        print(f"Failed to fetch configuration for job: {job_name}")
        return
    
    config_xml = response.text

    # Creating the job in target Jenkins with the fetched config
    target_url = f"{target_jenkins_url}/createItem?name={job_name}"
    headers = {"Content-Type": "application/xml"}
    response = requests.post(target_url, headers=headers, data=config_xml, auth=(target_user, target_api_token), verify=False)
    
    if response.status_code == 200:
        print(f"Successfully migrated job: {job_name}")
    else:
        print(f"Failed to migrate job: {job_name}. Response: {response.text}")

if __name__ == "__main__":
    SOURCE_JENKINS_URL = "https://jenkins-url1/"
    TARGET_JENKINS_URL = "https://jenkins-url2/"

    SOURCE_USER = "user1"
    SOURCE_API_TOKEN = "123456"

    TARGET_USER = "user2"
    TARGET_API_TOKEN = "123456"

    with open("jenkins_migrate.txt", "r") as file:
        jobs_to_migrate = [line.strip() for line in file]

    for job in jobs_to_migrate:
        migrate_job(SOURCE_JENKINS_URL, TARGET_JENKINS_URL, job, SOURCE_USER, SOURCE_API_TOKEN, TARGET_USER, TARGET_API_TOKEN)
