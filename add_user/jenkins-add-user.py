import requests
import xml.etree.ElementTree as ET
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def add_user_to_ldap_list(xml_content, new_user):
    # Parse the XML
    root = ET.fromstring(xml_content)

    # Find the specific 'hudson.model.ChoiceParameterDefinition' for 'ldapCommaSepList'
    choice_param_elem = root.find(".//hudson.model.ChoiceParameterDefinition[name='ldapCommaSepList']")
    if choice_param_elem is not None:
        choices_elem = choice_param_elem.find('.//a[@class="string-array"]/string')
        if choices_elem is not None:
            # Add the new user to the list
            ldap_list = choices_elem.text.strip() if choices_elem.text else ""
            if ldap_list:
                ldap_list += ','
            ldap_list += new_user
            choices_elem.text = ldap_list
            
            # Convert the modified XML back to a string
            return ET.tostring(root, encoding="utf-8").decode("utf-8")
    
    return None


def update_job_config(jenkins_url, job_name, user, api_token, new_config_xml):
    target_url = f"{jenkins_url}/job/{job_name}/config.xml"
    headers = {"Content-Type": "application/xml"}
    response = requests.post(target_url, headers=headers, data=new_config_xml, auth=(user, api_token))
    
    if response.status_code == 200:
        print(f"Successfully updated job: {job_name}")
    else:
        print(f"Failed to update job: {job_name}. Response: {response.text}")


def add_user_to_jobs(jenkins_url, jobs, user, api_token, new_user):
    for job_name in jobs:
        # Fetching the job config from Jenkins
        source_url = f"{jenkins_url}/job/{job_name}/config.xml"
        response = requests.get(source_url, auth=(user, api_token), verify=False)

        if response.status_code != 200:
            print(f"Failed to fetch configuration for job: {job_name}")
            continue
        
        config_xml = add_user_to_ldap_list(response.text, new_user)
        if config_xml:
            update_job_config(jenkins_url, job_name, user, api_token, config_xml)
        else:
            print(f"Failed to update the LDAP list for job: {job_name}")


if __name__ == "__main__":
    JENKINS_URL = "https://your-jenkins-url"
    USER = "user"
    API_TOKEN = "12345"
    NEW_USER = "newuser"

    # Read jobs from a text file
    with open("jenkins-jobs.txt", "r") as file:
        jobs_to_update = [line.strip() for line in file]

    add_user_to_jobs(JENKINS_URL, jobs_to_update, USER, API_TOKEN, NEW_USER)
