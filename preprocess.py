import re
import string

REGEX_FILTERS = {
    re.compile('https?://\S+'): '',  # uri
    re.compile('#\w*'): '',  # hashtag
    re.compile('@\w*'): '',  # mention
    re.compile('\d+'): '',  # number
    re.compile('(RT) \@'): '',  # retweet # TODO why is @ escaped?
    re.compile('[{chars}]'.format(chars=string.punctuation)): '',  # punctuation  TODO add other languages' punctuation
    re.compile('\s'): ' ',  # whitespace [ \t\n\r\f\v]
}
# TODO option to remove emoji, env var?

SPACES_REGEX = re.compile('  +')


def prep_text(text: str):
    ''' preprocess text, removing content irrelevant for entity recognition or topic selection'''
    for regex, replacement in REGEX_FILTERS.items():
        text = regex.sub(replacement, text)

    # replace multiple whitespaces last to catch those created by substitions above
    return SPACES_REGEX.sub(' ', text)
