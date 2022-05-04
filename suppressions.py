import requests

base_URL = '' #add your Dependency Track URL here ex. https://dependencytrack.internal.io/api/v1/
projectUUIDList = []
projectUUIDsWithSuppress = []


def api_headers():
    headers = {
        'Accept': 'application/json',
        'X-Api-Key': '', #add your api key here
    }
    params = {
        'excludeInactive': 'false'
    }
    return headers, params


def get_all_projects_uuids():
    try:
        headers, params = api_headers()
        response = requests.get(base_URL + 'project?page=1&limit=5000', headers=headers, params=params)
        json_array_response = response.json()
        for jsonObject in json_array_response:
            projectUUIDList.append(jsonObject['uuid'])
        return projectUUIDList
    except:
        print("Something went horribly wrong...")


def get_project_name_by_uuid(uuid):
    try:
        headers, params = api_headers()
        response = requests.get(base_URL + 'project/' + uuid, headers=headers, params=params)
        json_array_response = response.json()
        return json_array_response['name']
    except:
        print("Something went horribly wrong...")


def get_suppression_list():
    try:
        headers, params = api_headers()
        for projectUUID in projectUUIDList:
            response = requests.get(base_URL + 'finding/project/' + projectUUID + '?suppressed=true',
                                    headers=headers, params=params)
            json_array_response = response.json()
            if len(json_array_response) > 0:
                for jsonObject in json_array_response:
                    is_suppressed = jsonObject['analysis']['isSuppressed']
                    if is_suppressed:
                        component_name = jsonObject['component']['name']
                        vuln_info = jsonObject['vulnerability']['source'] + " " + jsonObject['vulnerability']['vulnId']
                        projectUUIDsWithSuppress.append(
                            'The following project ' + get_project_name_by_uuid(projectUUID) + ' for component ' +
                            component_name + ' for vulnerability ' + vuln_info + "\n")
    except:
        print("Something went horribly wrong...")


def main():
    print('|************************* - SCRIPT START - *************************|')
    print('This may take a few minutes...')
    get_all_projects_uuids()
    get_suppression_list()
    print(*projectUUIDsWithSuppress, sep=",")
    print('Total amount of vulnerabilities suppressed - ' + str(len(projectUUIDsWithSuppress)))


if __name__ == "__main__":
    main()
