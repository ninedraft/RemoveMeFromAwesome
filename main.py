import argparse

import jinja2
import yaml
from socks import SOCKS5
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest


class ListEntry():

    def __init__(self, url, title, description, subscribers,
                 pinned=None, tags=None):
        self.url = url
        self.title = title
        self.description = description
        self.subscribers = subscribers
        self.pinned = pinned
        self.tags = tags if tags else ['unsorted']


class WikiMaker():

    def load_list(self, path):
        with open(path, 'r') as stream:
            return yaml.safe_load(stream)

    def fill_list(self, api_id, api_hash, data, proxy=None):
        entries = {}

        client = TelegramClient('anon', api_id, api_hash, proxy=proxy)
        client.start()

        for category in data['entries']:
            entries[category] = {}
            for entry in data['entries'][category]:
                channel_request = GetFullChannelRequest(channel=entry['link'])
                channel = client(channel_request)
                description = channel.full_chat.about.replace('\n', '  \n    ')
                pinned = False if 'pinned' not in entry else entry['pinned']
                tags = None if 'tags' not in entry else entry['tags']
                entry = ListEntry(url=entry['link'], title=channel.chats[0].title, description=description,
                                  subscribers=channel.full_chat.participants_count, pinned=pinned, tags=tags)
                for tag in entry.tags:
                    tagname = tag if tag not in data['tags'] else data['tags'][tag]['title']
                    if tagname not in entries[category]:
                        entries[category][tagname] = []
                    entries[category][tagname].append(entry)

        return entries

    def render_markdown(self, path, data):
        templateLoader = jinja2.FileSystemLoader(searchpath="./")
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(path)

        return template.render(categories=data)

    def save_file(self, data, path):
        with open(path, 'w') as stream:
            stream.write(data)


def main():
    proxy = None

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--proxy', type=str, default=None, help='socks5 proxy')
    parser.add_argument('-id', '--telegram_api_id', type=int, required=True, help='api_id from telegram')
    parser.add_argument('-hash', '--telegram_api_hash', type=str, required=True, help='api_hash from telegram')
    parser.add_argument('-c', '--channels', type=str, default='list.yml', help='path to file with list of channels')
    parser.add_argument('-i', '--input', type=str, required=True, help='path to file with Jinja2 template')
    parser.add_argument('-o', '--output', type=str, required=True, help='path to file with Jinja2 templategenerated file')
    args = parser.parse_args()


    if args.proxy:
        proxy_host, proxy_port = args.proxy.split(':')
        proxy = (SOCKS5, proxy_host, int(proxy_port))

    maker = WikiMaker()

    raw_data = maker.load_list(args.channels)
    template_data = maker.fill_list(api_id=args.telegram_api_id,
                                   api_hash=args.telegram_api_hash,
                                   data=raw_data,
                                   proxy=proxy)
    md_data = maker.render_markdown(path=args.input,
                                   data=template_data)

    maker.save_file(md_data, args.output)

if __name__ == '__main__':
    main()
