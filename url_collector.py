import os
import time
from slackclient import SlackClient
import re
import mysql.connector
import config
# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "do"
URL_REGEXP = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def contains_url(text):
    urls = re.findall(URL_REGEXP, text)
    if len(urls):
        return urls
    return None

def store_data(url):
    # store url
    cursor = cnx.cursor()
    data = [url[:-1],time.strftime('%Y-%m-%d %H:%M:%S')]
    data_log = tuple(data)
    update_log=("INSERT INTO urls (url,shared_at) VALUES (%s,%s)")
    cursor.execute(update_log, data_log)
    cnx.commit()
    print ("data stored")
    cursor.close()

def message_from_resource_channel(slack_rtm_output):
    """
        This parsing function returns the message text if the rtm output is
        a message sent from the resource channel
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                response = slack_client.api_call('channels.info',
                                        channel=output['channel'])
                if response['channel']['name'] == "url_collector_test":
                    return output['text']

    return None


if __name__ == "__main__":
    cnx = mysql.connector.connect(**config.db_info) # connect to database
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        # keep listening to notifications
        while True:
            slack_rtm_output = slack_client.rtm_read()
            text = message_from_resource_channel(slack_rtm_output)
            if text:
                urls = contains_url(text)
                if urls:
                    for url in urls:
                        store_data(url)

            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
