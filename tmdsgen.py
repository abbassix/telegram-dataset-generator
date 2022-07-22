from bs4 import BeautifulSoup
import csv
import glob


def get_data(file_path):
    html_doc = open(file_path, "r")
    soup = BeautifulSoup(html_doc, 'html.parser')

    group = soup.find('div', {'class': 'text bold'}).text.strip()

    # store all messages with id and text in a dic
    all_msgs = {}
    msgs = soup.find_all("div", {'class': 'message default clearfix'})
    for msg in msgs:
        # message id
        msg_id = msg.get('id')

        # message text
        msg_text = msg.find('div', {'class': 'text'})
        # ignore the message if it has no text
        if msg_text is None:
            continue
        all_msgs[msg_id] = {'id': msg_id, 'text': msg_text.text.strip()}

        # message ref
        reply = msg.find('div', {'class': 'reply_to details'})
        if reply is not None:
            msg_ref = reply.find('a', href=True)['href'][7:]
            if msg_ref in all_msgs:
                all_msgs[msg_id]['ref'] = msg_ref

    chats = [{'question': all_msgs[value['ref']]['text'],
              'answer': value['text']}
             for value in all_msgs.values() if 'ref' in value]

    if not chats:
        return

    keys = chats[0].keys()

    with open(f'dialogue/{group}.csv', 'a', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(chats)


if __name__ == "__main__":
    files_path = glob.glob('data/*/messages*.html')
    for file_path in files_path:
        get_data(file_path)
