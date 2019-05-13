import jinja2
import socks
import yaml
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
    API_ID = 0
    API_HASH = ''
    LIST_YAML_FILE = 'list.yml'
    MARKDOWN_TEMPLATE_FILE = 'template.md'

    DEFAULT_ENTRY = {
        'url': None,
        'title': None,
        'description': None,
        'subscribers': 0,
        # 'start_from': None,
        'pinned': False,
        'tags': ['unsorted']
    }

    def __init__(self, proxy=None):
        self.proxy = proxy

    def run(self):
        raw_data = self.load_list(self.LIST_YAML_FILE)
        template_data = self.fill_list(api_id=self.API_ID,
                                       api_hash=self.API_HASH,
                                       data=raw_data,
                                       proxy=self.proxy)
        md_data = self.render_markdown(path=self.MARKDOWN_TEMPLATE_FILE,
                                       data=template_data)

        self.save_file(md_data, 'README.MD')

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
                tags = ['unsorted'] if 'tags' not in entry else entry['tags']
                entry = ListEntry(url=entry['link'], title=channel.chats[0].title, description=description,
                                  subscribers=channel.full_chat.participants_count, pinned=pinned, tags=tags)
                for tag in tags:
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
    proxy = (socks.SOCKS5, '127.0.0.1', 9050)
    maker = WikiMaker(proxy=proxy)
    maker.run()


if __name__ == '__main__':
    main()
