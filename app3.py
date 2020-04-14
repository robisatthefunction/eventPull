import requests, argparse, csv, time

#get number of experiments in project
def event_pull():
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="paste your Optimizely v2 REST API token as the second argument")
    args = parser.parse_args()
    token = args.token

# add filewriter lines
    with open('Fox_Events.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#        project_list = requests.get("https://api.optimizely.com/v2/projects", headers={'Authorization': 'Bearer %s' % token})
        metrics = []
        project_count = 100
        project_page = 1
        while (project_count == 100):
            project_object = requests.get("https://api.optimizely.com/v2/projects?per_page=100&page=%s" % project_page, headers={'Authorization': 'Bearer %s' % token})
            project_object = project_object.json()
            project_count = len(project_object)
            project_page += 1
            for project in project_object:
                if project["status"] == "active":
                    print("Project Name: ", project["name"]) # helps keep status of script
                    filewriter.writerow(["Project Name:", project["name"]])
                    filewriter.writerow(["Project Platform:",project["platform"]])
                    filewriter.writerow(["Project ID:",project["id"]])
                    filewriter.writerow(["Event Name", "Event Type", "Event ID", "Event Status"])
                    exp_count = 100
                    exp_page = 1
                    while (exp_count == 100):
                        experiment_list = requests.get("https://api.optimizely.com/v2/experiments?project_id=%s&per_page=100&page=%s" % (project["id"],exp_page), headers={'Authorization': 'Bearer %s' % token})
                        if experiment_list.status_code == 200:
                            experiment_list = experiment_list.json()
                            exp_count = len(experiment_list)
                            exp_page += 1
                            for experiment in experiment_list:
                                last_modified = experiment["last_modified"].split("T")[0]
                                days_ago = "2020-01-01"
                                modified_timestamp = time.mktime(time.strptime(last_modified, '%Y-%m-%d'))
                                days_ago_timestamp = time.mktime(time.strptime(days_ago, '%Y-%m-%d'))
                                if (modified_timestamp > days_ago_timestamp):
                                   for x in range(len(experiment["metrics"])):
                                      if type(experiment["metrics"]) is list:
                                            event_id = experiment["metrics"][x].get("event_id")
                                            if event_id != None:
                                                metrics.append(event_id)
                                   if project["platform"] == "web":
                                       pages = experiment.get("page_ids")
                                       if pages != None:
                                           for x in range(len(pages)):
                                               if type(pages) is list:
                                                   event_id = pages[x]
                                                   metrics.append(event_id)
                    active_events = list(dict.fromkeys(metrics))
                    event_count = 100
                    event_page = 1
                    while (event_count == 100):
                        event_list = requests.get("https://api.optimizely.com/v2/events?project_id=%s&per_page=100&page=%s" % (project["id"],event_page), headers={'Authorization': 'Bearer %s' % token})
                        event_list = event_list.json()
                        event_count = len(event_list)
                        event_page += 1
                        for event in event_list:
                            if event["id"] in active_events:
                                filewriter.writerow([event["name"], event["event_type"], event["id"], "Active"])
                            else:
                                filewriter.writerow([event["name"], event["event_type"], event["id"], "Inactive"])
                    metrics = []
    #                                        if event_id != None:
    #                                            event = requests.get("https://api.optimizely.com/v2/events/%s" % event_id, headers={'Authorization': 'Bearer %s' % token})
    #                                            event = event.json()
    #                                            filewriter.writerow(["Event Name", event["name"]])
    #                                            filewriter.writerow(["Event Key", event["key"]])
    #                                            filewriter.writerow(["Event Type", event["event_type"]])
    #                                            filewriter.writerow(["Event ID", event["id"]])
#                event_list = requests.get("https://api.optimizely.com/v2/events?project_id=%s" % project["id"], headers={'Authorization': 'Bearer %s' % token})
#                if event_list.status_code == 200:
#                    event_list = event_list.json()
#                    for event in event_list:
#                        filewriter.writerow([event["name"], event["key"], event["event_type"], event["id"]])

event_pull()
