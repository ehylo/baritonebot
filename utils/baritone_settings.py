import re

import requests

from utils import const


class Setting:
    def __init__(self, description: str, title: str, data_type: str, default: str, link_website: bool):

        description = description.replace(' * <p> * ', '\n')
        # adds the newline
        description = description.replace('* ', '')
        # removes the star which isn't needed
        if '<a href="' in description:
            hyperlink = re.findall(r'<a href="(?P<link>.*)">(?P<text>.*)</a>', description)[0]
            description = re.sub(r'<a href=".*">.*</a>', f'[{hyperlink[1]}]({hyperlink[0]})', description)
            # change the html hyperlink to Markdown hyperlink
        description = description.replace(' @see', '\n**See Also:**')
        # change the html `@see` to actual text

        default = default.replace('Blocks.', '')
        # remove 'Blocks.'
        default = default.replace('Color.', '')
        # remove 'Color.'
        default = default.replace('new ArrayList<>( )', '')
        # remove 'new ArrayList<>( )'
        default = default.replace('new HashMap<>()', '')
        # remove 'new HashMap<>()'
        default = default.replace('new ArrayList<>(Arrays.asList( ', '')
        # remove 'new ArrayList<>(Arrays.asList('
        default = default.replace('Item.getItemFromBlock(', '')
        # remove 'Item.GetItemFromBlock('
        default = default.replace('new Vec3i(', '')
        # remove 'new Vec3i('
        default = re.sub(r'[()]', '', default)
        # remove any ')'

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

        for setting_text in requests.get(url).content.decode('utf-8').split('/**')[2:-6]:
            cleaned_setting_text = ' '.join(re.sub(r'(?<!:)//.*\n', '', setting_text).split())
            # removes multi blank spaces, line ends, and comments
            link_website = False if url != const.VERSION_DOCS_URL else True
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
