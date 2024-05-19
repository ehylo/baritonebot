import re
import enum
import logging

import requests

from utils import VERSION_DOCS_URL, VERSION_12_URL, VERSION_LATEST_URL, VERSION_MASTER_URL

log = logging.getLogger('utils.baritone_settings')


class Setting:
    def __init__(self, description: str, title: str, data_type: str, default: str, link_website: bool):

        # adds the newline
        description = description.replace(' * <p> * ', '\n')

        # removes the star which isn't needed
        description = description.replace(' * ', '\n')

        # prevent _ in descriptions ruining the formatting
        description = description.replace('_', r'\_')

        # make the code blocks work
        description = description.replace('<pre>', '```')
        description = description.replace('</pre>', '```')

        log.info('checking for html hyperlinks and converting them to discord markdown hyperlinks')
        if '<a href="' in description:
            hyperlink = re.findall(r'<a href="(?P<link>.*)">(?P<text>.*)</a>', description)[0]
            description = re.sub(r'<a href=".*">.*</a>', f'[{hyperlink[1]}]({hyperlink[0]})', description)
            # change the html hyperlink to Markdown hyperlink
        description = description.replace(' @see', '\n**See Also:**')
        # change the html `@see` to actual text

        log.info('removing all java types from documentation')

        # remove 'Blocks.'
        default = default.replace('Blocks.', '')

        # remove 'Color.'
        default = default.replace('Color.', '')

        # remove 'new ArrayList<>( )'
        default = default.replace('new ArrayList<>( )', '')

        # remove 'new HashMap<>()'
        default = default.replace('new HashMap<>()', '')

        # remove 'new ArrayList<>(Arrays.asList('
        default = default.replace('new ArrayList<>(Arrays.asList( ', '')

        # remove 'Item.GetItemFromBlock('
        default = default.replace('Item.getItemFromBlock(', '')

        # remove 'new Vec3i('
        default = default.replace('new Vec3i(', '')

        # remove '.asItem'
        default = default.replace('.asItem', '')

        # remove any ')'
        default = re.sub(r'[()]', '', default)

        self.description = description
        self.title = title
        self.data_type = data_type
        self.default = default if default != '' else 'None'
        if link_website:
            self.combined = f'**[{title}](https://baritone.leijurv.com/baritone/api/Settings.html#{title})**'
        else:
            self.combined = f'**{title}**'
        self.combined += f' | __{self.data_type}__ | *Default:* `{self.default}`\n{self.description}\n\n'


class VersionSettings:
    def __init__(self, url: str):
        self.settings = []

        log.info(f'generating VersionSetting object from url: {url}')
        for setting_text in requests.get(url).content.decode().split('/**')[2:-6]:

            # skip settings that the user can't use
            if '@JavaOnly' in setting_text:
                continue

            # removes multi blank spaces, line ends, and comments
            cleaned_setting_text = ' '.join(re.sub(r'(?<!:)//.*\n', '', setting_text).split())

            link_website = False if url != VERSION_DOCS_URL else True

            self.settings.append(Setting(
                re.findall(r'^\* (?P<description>.*) \*/', cleaned_setting_text)[0],
                re.findall(r'Setting<.*> (?P<title>.*) = ', cleaned_setting_text)[0],
                re.findall(r'Setting<(?P<data_type>.*)> ', cleaned_setting_text)[0],
                re.findall(r'<>\((?P<default>.*)\);', cleaned_setting_text)[0],
                link_website
            ))

    def search(self, search_term: str):
        pages = ['']
        matched_settings = []
        for setting in self.settings:
            if re.search(search_term.lower(), setting.title.lower()) is not None:
                matched_settings.append(setting)
        if len(matched_settings) > 0:
            page_index = 0
            for match in matched_settings:
                if len(match.combined) + len(pages[page_index]) <= 2048:
                    pages[page_index] += match.combined
                else:
                    page_index += 1
                    pages.append(match.combined)
        return pages


baritone_settings_master = VersionSettings(VERSION_MASTER_URL)
baritone_settings_v2 = VersionSettings(VERSION_12_URL)
baritone_settings_latest = VersionSettings(VERSION_LATEST_URL)
log.info('all baritone setting objects have been created')

baritone_settings_matcher = [
    ('master', baritone_settings_master),
    ('1.2', baritone_settings_v2),
    ('1.10', baritone_settings_latest),
]
baritone_settings_versions = enum.Enum(value='version', names=baritone_settings_matcher)
