import re
import string

REGEX_FILTERS = {
    re.compile('RT @\w+'): '',  # retweet (filter before removing mentions)
    re.compile('https?://\S+'): '',  # uri
    re.compile('#\w*'): '',  # hashtag
    re.compile('@\w*'): '',  # mention
    # re.compile('\d+'): '',  # number
    # re.compile('[{chars}]'.format(chars=string.punctuation + '¿¡')): '',
    re.compile('\s'): ' ',  # whitespace [ \t\n\r\f\v]
}
# TODO remove punctuation and numbers before parsing for POS etc.?
# TODO option to remove emoji, env var?


SPACES_REGEX = re.compile('  +')


def prep_text(text: str):
    ''' preprocess text, removing content irrelevant for entity recognition or topic selection'''
    for regex, replacement in REGEX_FILTERS.items():
        text = regex.sub(replacement, text)

    # replace multiple whitespaces last to catch those created by substitions above
    return SPACES_REGEX.sub(' ', text)
