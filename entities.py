import argparse
import json
import sys

import googleapiclient.discovery

import analyze


def analyze_entities(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding,
    }

    service = googleapiclient.discovery.build('language', 'v1')
    request = service.documents().analyzeEntities(body=body)
    response = request.execute()

    return response

# Analyzed syntax for VERB
def analyze_syntax(text, encoding='UTF32'):
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'encoding_type': encoding
    }

    service = googleapiclient.discovery.build('language', 'v1')

    request = service.documents().analyzeSyntax(body=body)
    response = request.execute()

    return response


def form_db_queries(text):
    result = analyze_syntax(text)
    assert len(result['tokens'])
    verb_list = []
    obj_list = get_entity_list(text)
    previous_token = ['', '']

    db_queries = []
    for token in result['tokens']:
        #VERBS
        if (token['partOfSpeech']['tag'] == 'VERB'):
            tempVerb = token['text']['content']
            if ('ing' in tempVerb):
                tempVerb = tempVerb.replace('ing','')
                verb_list.append(tempVerb)
            verb_list.append(token['text']['content'])

        # NOUNS
        if (token['partOfSpeech']['tag'] == 'NOUN'):
            obj_list.append(token['text']['content'])
            if (previous_token[1] == "ADJ"):
                temp = previous_token[0] + " " + token['text']['content']
                obj_list.append(temp)

        # previous token is reset
        previous_token[0] = token['text']['content']
        previous_token[1] = token['partOfSpeech']['tag']

        print(token['text']['content'])

    if (len(verb_list) >= 2):
        verb_list.pop(0)

    obj_list = list(set(obj_list))

    for verb in verb_list:
        for obj in obj_list:
            temp = verb + " " + obj
            db_queries.append(temp)

    print(db_queries[0])
    return db_queries




# List of entities
def get_entity_list(text):
    result = analyze_entities(text)
    assert result['language'] == 'en'
    entities = result['entities']
    assert len(entities)
    entity_list = []
    for entity in entities:
        entity_list.append(entity['name'])
        #print(entity['name'])
    print(json.dumps(result, indent=2))
    return entity_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('text')
    args = parser.parse_args()
    form_db_queries(args.text)
