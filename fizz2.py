# Interactive python 2 client for fizzbot

import json
import urllib2

domain = 'https://api.noopschallenge.com'

def print_sep(): print('----------------------------------------------------------------------')

# print server response
def print_response(dict):
    print('')
    print('message:')
    print(dict.get('message'))
    print('')
    for key in dict:
        if key != 'message':
            print('%s: %s' % (key, json.dumps(dict.get(key))))
    print('')

# try an answer and see what fizzbot thinks of it
def try_answer(question_url, answer):
    print_sep()
    body = json.dumps({ 'answer': answer })
    print('*** POST %s %s' % (question_url, body))
    try:
        req = urllib2.Request(domain + question_url, body, {'Content-Type': 'application/json'})
        res = urllib2.urlopen(req)
        response = json.load(res)
        print_response(response)
        print_sep()
        return response

    except urllib2.HTTPError as e:
        response = json.load(e)
        print_response(response)
        return response

def mkanswer(question_data):
    if 'exampleResponse' in question_data and question_data['exampleResponse']['answer'] == 'COBOL':
        return 'COBOL'
    if question_data['numbers']:
        return fizzbuzz(question_data['rules'], question_data['numbers'])
    print question_data

def fizzbuzz(rules, numbers):
    return ' '.join([fizzify(x, rules) for x in numbers])

def fizzify(x, rules):
    s = ''
    for rule in rules:
        if x % rule['number'] == 0:
            s += rule['response']
    if s:
        return s
    else:
        return str(x)

# keep trying answers until a correct one is given
def get_correct_answer(question_url, question_data):
    while True:
        answer = mkanswer(question_data)

        response = try_answer(question_url, answer)

        if (response.get('result') == 'interview complete'):
            print('congratulations!')
            exit()

        if (response.get('result') == 'correct'):
            raw_input('press enter to continue')
            return response.get('nextQuestion')

# do the next question
def do_question(domain, question_url):
    print_sep()
    print('*** GET %s' % question_url)

    question_data = json.load(urllib2.urlopen( ('%s%s' % (domain, question_url)) ))
    print_response(question_data)
    print_sep()

    next_question = question_data.get('nextQuestion')

    if next_question: return next_question
    return get_correct_answer(question_url, question_data)


def main():
    question_url = '/fizzbot'
    while question_url:
        question_url = do_question(domain, question_url)

if __name__ == '__main__': main()
