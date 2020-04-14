import requests, argparse, csv, time

#get number of experiments in project
def event_pull():
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="paste your Optimizely v2 REST API token as the second argument")
    args = parser.parse_args()
    token = args.token

    with open('Fox_Events_ALL_040220_ToDelete.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        project_id = 0
        for row in csv_reader:
            if row[0] == "Project ID:":
                project_id = row[1]
            if row[4] == "Delete":
                event_id = row[2]
                response = requests.delete("https://api.optimizely.com/v2/projects/%s/custom_events/%s" % (project_id, event_id), headers={'Authorization': 'Bearer %s' % token})
    print("deletion complete")
event_pull()
