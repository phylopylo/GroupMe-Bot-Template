import requests
import json

"""
Get meta information about a groupme group. The access token used must be for a user who is presently a member of the group.

The group_name must be either an exact copy of the group name, or a substring of the group name specific enough not to overlap with another group's name.
"""
def get_group_info(group_name: str, token: str):
    groups_url = 'https://api.groupme.com/v3/groups?token=' + token
    r = requests.get(groups_url)
    response_as_dict = json.loads(r.text)
    grouplist = response_as_dict["response"]

    groups_identified = []
    for group in grouplist:
        if group_name in group["name"]:
            groups_identified.append(group)

    num_groups = len(groups_identified)

    if num_groups == 0:
        print('WARNING! No groups found matching name ' + group_name)
        raise Exception('Failed to retrieve group ID.')
    if num_groups > 1:
        print('WARNING! More than one group found matching name ' + group_name)
        raise Exception('Failed to retrieve group ID.')

    return groups_identified


"""
Create a bot in a groupme group.
"""
def create_bot(bot_name: str, group_name: str, token: str):
    bots_url = 'https://api.groupme.com/v3/bots?token=' + token
    try:
        group_info = get_group_info(group_name, token)
        group_id = str(group_info[0]['id'])

        headers = {'Content-Type': 'application/json'}
        
        data = {
                'bot' : {
                    'name': bot_name,
                    'group_id': group_id
                }
        }

        r = requests.post(bots_url, data=json.dumps(data), headers=headers)
        return json.loads(r.text)
    except:

"""
Use a bot to post
"""
def post_with_bot(bot_id: str, content: str):
        url = "https://api.groupme.com/v3/bots/post"
        headers = {'Content-Type': 'application/json'}

        data = {
            'bot_id': bot_id,
            'text': content
        }

        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response
            raise Exception('Failed to post.')

if __name__ == "__main__":
    # Add your token from https://dev.groupme.com/bots
    token = ''

    # Add the name of a group you are a member of
    group_name = ''

    # Name your bot. This can be arbitrary.
    bot_name = ''

    bot_info = create_bot(bot_name, group_name, token)

    bot_id = bot_info['response']['bot']['bot_id']
    bot_name = bot_info['response']['bot']['name']
    group_id = bot_info['response']['bot']['group_id']
    group_name = bot_info['response']['bot']['group_name']

    # post
    post_with_bot(bot_id, 'This is my first test message!')
