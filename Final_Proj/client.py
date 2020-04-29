import argparse
import requests
import json
import datetime


def get_messages(user):
    # MODIFY URL TO AMAZON VIRTUAL SERVER ADDRESS
    url = 'http://localhost/?user={}'.format(user)
    r = requests.get(url)
    last_refresh = datetime.datetime.now()
    json_response = json.loads(r.text)
    messages = json_response["response"]["messages"]
    print("Your messages: ")
    for m in messages:
        print('({}) {}'.format(m["sender"], m["value"]))
    return last_refresh


def refresh_messages(user, last_refresh):
    # MODIFY URL TO AMAZON VIRTUAL SERVER ADDRESS
    url = 'http://localhost/?user={}'.format(user)
    r = requests.get(url)
    new_refresh = datetime.datetime.now()
    json_response = json.loads(r.text)
    messages = json_response["response"]["messages"]
    for m in messages:
        temp_time = datetime.datetime.strptime(m["sendTime"], '%m/%d/%y %H:%M:%S')
        if temp_time > last_refresh:
            print('({}) {}'.format(m["sender"], m["value"]))
    return new_refresh


def send_message(user, command):
    receiver = command.split(':')[1]
    message = command.split(':')[2]
    cur_time = datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')
    request_body = {
        "sender": user,
        "receiver": receiver,
        "message": message,
        "sendTime": cur_time
    }
    # MODIFY URL TO AMAZON VIRTUAL SERVER ADDRESS
    url = 'http://localhost/'
    requests.post(url, json=request_body)
    print("Message sent")
    return


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user')
    user = parser.parse_args().user
    last_refresh = get_messages(user)
    while True:
        command = input("Please input an action (refresh, send:<to_user>:<msg>, quit): ")
        action = command.split(':')[0].lower()
        if action == 'refresh':
            last_refresh = refresh_messages(user, last_refresh)
        elif action == 'send':
            send_message(user, command)
        elif action == 'quit':
            break
        else:
            print("Please input a valid command!")


if __name__ == '__main__':
    main()
