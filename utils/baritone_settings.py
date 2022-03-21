import re

import requests


from utils.const import VERSION_1215_URL, VERSION_163_URL, VERSION_172_URL, VERSION_182_URL


class Setting:
    def __init__(self, description, title, data_type, default, link_website):

        description.replace(' * <p> * ', '\n')
        # adds the newline
        description.replace('* ', '')
        # removes the star which isn't needed
        if '<a href="' in description:
            hyperlink = re.findall(r'<a href="(?P<link>.*)">(?P<text>.*)</a>', description)[0]
            description = re.sub(r'<a href=".*">.*</a>', f'[{hyperlink[1]}]({hyperlink[0]})', description)
            # change the html hyperlink to Markdown hyperlink
        description.replace(' @see', '\n**See Also:**')
        # change the html `@see` to actual text

        default.replace('Blocks.', '')
        # remove 'Blocks.'
        default.replace('Color.', '')
        # remove 'Color.'
        default.replace('new ArrayList<>( )', '')
        # remove 'new ArrayList<>( )'
        default.replace('new HashMap<>()', '')
        # remove 'new HashMap<>()'
        default.replace('new ArrayList<>(Arrays.asList( ', '')
        # remove 'new ArrayList<>(Arrays.asList('
        default.replace('Item.getItemFromBlock(', '')
        # remove 'Item.GetItemFromBlock('
        default.replace('new Vec3i(', '')
        # remove 'new Vec3i('
        default = re.sub(r'[()]', '', default)
        # remove any ')'

        self.description = description
        self.title = title
        self.data_type = data_type
        self.default = default
        if link_website:
            self.combined = f'**[{title}](https://baritone.leijurv.com/baritone/api/Settings.html#{title})**'
        else:
            self.combined = f'**{title}**'
        self.combined += f' | __{data_type}__ | *Default:* `{default}`\n{description}\n\n'


class VersionSettings:
    def __init__(self):
        self.v2_settings = []
        self.v6_settings = []
        self.v7_settings = []
        self.v8_settings = []
        self.versions = {
            '1.2.15': self.v2_settings,
            '1.6.3': self.v6_settings,
            '1.7.2': self.v7_settings,
            '1.8.2': self.v8_settings
        }
        self.version_urls = {
            self.v2_settings: VERSION_1215_URL,
            self.v6_settings: VERSION_163_URL,
            self.v7_settings: VERSION_172_URL,
            self.v8_settings: VERSION_182_URL
        }
        # TODO: add a temp fix for missing info (49/50 for 1.8.2 and 45/46 for 1.2.15) and 1.7.2, 1.6.3

        for version in [self.v2_settings, self.v6_settings, self.v7_settings, self.v8_settings]:
            for setting_text in requests.get(self.version_urls[version]).content.decode('utf-8').split('/**')[2:-4]:
                cleaned_setting_text = ' '.join(re.sub(r'(?<!:)//.*\n', '', setting_text).split())
                # removes multi blank spaces, line ends, and comments
                link_website = False if version != self.v2_settings else True
                version.append(Setting(
                    re.findall(r'^\* (?P<description>.*) \*/', cleaned_setting_text)[0],
                    re.findall(r'Setting<.*> (?P<title>.*) = ', cleaned_setting_text)[0],
                    re.findall(r'Setting<(?P<data_type>.*)> ', cleaned_setting_text)[0],
                    re.findall(r'<>\((?P<default>.*)\);', cleaned_setting_text)[0],
                    link_website
                ))

    def search(self, search_term: str, version: str):
        pages = ['']
        matched_settings = []
        for setting in self.versions[version]:
            if re.search(search_term, setting.title.lower()) is not None:
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
