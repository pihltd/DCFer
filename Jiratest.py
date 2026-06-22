import requests
import os
import urllib.parse
import pandas as pd
import sys

def lister(listfield, item):
    finallist = []
    for entry in listfield:
        finallist.append(entry[item])
    return finallist

def issueParser(jsonobj, key1, key2=None):
    if key2 == None:
        if key1 in jsonobj.keys():
            return jsonobj[key1]
    elif key2 is not None:
        if key1 in jsonobj.keys():
            print(f"Key1: {key1}\tKey2: {key2}\nJSONOBject:\n{jsonobj[key1]}\n")
            if key2 in jsonobj[key1].keys():
                return jsonobj[key1][key2]
        else:
            return 'None'
    else:
        return 'None'

def trackerAPIReq():
    apitoken = os.getenv('JIRAAPI')
    headers = {"accept": "application/json", "Authorization": f"Bearer {apitoken}"}
    
    baseurl = 'https://tracker.nci.nih.gov/'
    
    getterms = 'rest/api/2/terminology/entries/sprint'
    
    getboard = 'rest/agile/1.0/board'
    
    crdcdhboard = 1177
    getsprints = f"/rest/agile/1.0/board/{crdcdhboard}/sprint"
    
    getactivesprint = f"/rest/agile/1.0/board/{crdcdhboard}/sprint?state=active"
    getfuturessprints = f"/rest/agile/1.0/board/{crdcdhboard}/sprint?state=future"
    
    sprintid = 8582
    getissues = f"/rest/agile/1.0/sprint/{sprintid}/issue"
    
    #url = urllib.parse.quote_plus(f"{baseurl}{getboard}")
    #url = f"{baseurl}{getactivesprint}"
    url = f"{baseurl}{getfuturessprints}"
    res = requests.get(url=url, headers=headers)
    res = res.json()
    print(res)
    sprint_df = pd.DataFrame(res['values'])
    print(sprint_df)
    
    sys.exit(0)
    
    
    url2 = f"{baseurl}{getissues}"
    res2 = requests.get(url=url2, headers=headers)
    res2 = res2.json()
    issue_df = pd.DataFrame(res2['issues'])
    
    issuelist = issue_df['id'].unique().tolist()
   
    issuereport = []
    for issueid in issuelist:
        singleissueurl = f"/rest/api/2/issue/{issueid}"
        singleurl = f"{baseurl}{singleissueurl}"
        res3 = requests.get(url=singleurl, headers=headers)
        res3 = res3.json()
        '''
        # res['id'] = issue ID, res['key'] = ticket name
        # Useful stuff in res['fields']
            # Useful fields under res['fields'] 
            # resolution/name - status of the ticket
            # asignee/name - person assigned the ticket
            # displaName - full name of person
            # subtasks
            # issuetype/name - the kind of task (Task, etc.)
            # status/name - open, closed, etc
            # creator/name - person who created the ticket
            # creator/displayname - see above
            # components - list of dictionary of impacted systems, 'name' key in each list item.  Backend, frontend, etc.
            # reporter name/displayname - similar to creator?
            # description - description of the ticket
            # comment/comments - list of dictionary of the comments. In each dictionary, author/name has name, body has comment text
            # fixVersions list of dictionary and  'name' - release ticet is assigned to
            # versions looks the same of fixVersions
            
        '''
        fields = res3['fields']
        ticketstuff = {}
        ticketstuff['ticket'] = issueParser(res3, 'key')
        ticketstuff['ticketID'] = issueParser(res3, 'id')
        ticketstuff['assignee'] = issueParser(fields, 'assignee', 'displayName')
        ticketstuff['issueType'] = issueParser(fields, 'issuetype', 'name')
        ticketstuff['status'] = issueParser(fields, 'status', 'name')
        ticketstuff['reporter'] = issueParser(fields, 'reporter', 'displayName')
        ticketstuff['description'] = issueParser(fields, 'description')
        ticketstuff['story_points'] = issueParser(fields, 'customfield_10042')
        #ticketstuff = {
            #"ticket":  res3['key'],
            #"ticketID": res3['id'],
            #"ticketstatus": fields['resolution']['name'],
            #"assignee": fields['assignee']['displayName'],
            #"issueType": fields['issuetype']['name'],
            #"status": fields['status']['name'],
            #"reporter": fields['reporter']['displayName'],
            #"description": fields['description'],
            #"story_points": fields['customfield_10042']
        #}
        
        ticketstuff['components'] = lister(fields['components'], 'name')
        ticketstuff['comments'] = lister(fields['comment']['comments'], 'body')
        ticketstuff['release'] = lister(fields['fixVersions'], 'name')
        
        issuereport.append(ticketstuff)
        
    final_df = pd.DataFrame(issuereport)
    print(final_df)

trackerAPIReq()