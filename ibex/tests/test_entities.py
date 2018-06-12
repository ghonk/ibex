from ..preprocess import prep_text
from ..entities import get_entities


eng_doc = "President Donald Trump did disrespect my son and my daughter https://t.co/BcROQI0Jle #MAGA #Patriot #1A #2A #GOP"
span_doc = "Amlo no ¡con las manos masa Nicolás Maduro López Obrador comparten asesor económico"


def test_multi_word():
    ''' check that multi-word proper nouns are identified as entities '''
    result = get_entities(eng_doc, 'english')
    assert 'Donald Trump' in result

    result = get_entities(span_doc, 'spanish')
    assert 'Nicolás Maduro López Obrador' in result

    result = get_entities('The Eiffel Tower in Paris is very pretty.', 'english')
    assert 'The Eiffel Tower' in result and 'Paris' in result


def test_text_clean():
    ''' test text preprocessing'''

    # check that hashtags and uri's are removed by prep_text
    prep_doc = prep_text(eng_doc)
    for val in ['https://t.co/BcROQI0Jle', '#MAGA', '#Patriot', '#1A', '#2A', '#GOP']:
        assert val not in prep_doc

    # check that mentions and retweets are dropped
    doc = "RT @panekbill: @AverageHunter Thanks for the follow."
    prep_doc = prep_text(doc)
    for val in ['RT', '@panekbill:', '@AverageHunter']:
        assert val not in prep_doc

    # # check that numbers and punctuation are dropped
    # doc = "The character '&' can be traced back to 100 A.D.!"
    # prep_doc = prep_text(doc)
    # for val in ['&', '100', "'", "!"]:
    #     assert val not in prep_doc

    # prep_doc = prep_text(span_doc)
    # assert "¡" not in prep_doc


def test_exclude_words():
    ''' test that words and characters manually included in exclude_words.txt are dropped along with numbers and punctuation '''

    doc = "¿¡Can you believe This Company!?"
    result = get_entities(doc, 'english')
    for val in ['¿', '¡', 'company']:
        assert val not in result

    doc = 'The Number Five is one larger than The Number 4.'
    result = get_entities(doc, 'english')
    for val in ['Five', 'one', '4']:
        assert val not in result

    doc = "¿Hola, Qué hora es, Paul?"
    result = get_entities(doc, 'spanish')
    for val in ['¿', 'Hola', 'Qué', '?']:
        assert not any([val in ent for ent in result])
