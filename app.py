# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect
from textblob import TextBlob
import random
import os
import json

app = Flask(__name__)


def make_pos_dict(text):
    blob = TextBlob(text)
    pos_words = dict(blob.pos_tags)
    return pos_words


def get_nouns(posword_dict):
    nouns = [str(k) for k, v in posword_dict.iteritems() if (
        v == u'NNP' or v == u'NN' or v == u'NNS' or v == u'NNPS')]
    return nouns


def get_adjs(posword_dict):
    adjs = [k for k, v in posword_dict.iteritems() if (
        v == u'JJ' or v == u'JJR' or v == u'JJS')]
    return adjs


def get_verbs(posword_dict):
    verbs = [k for k, v in posword_dict.iteritems() if (
        v == u'VB' or v == u'VBD' or v == u'VBG' or v == u'VBN' or v == u'VBP' or v == u'VBZ')]
    return verbs


def get_indices(larger_list, smaller_list):
    '''returns a list of where items in the smaller list
    appear in the larger list'''
    indices = []
    for i in larger_list:
        if i in smaller_list:
            indices.append(larger_list.index(i))
    return indices


def get_parts(text, parts_to_shuffle):
    '''(str, list) -> list of words with requested parts of speech'''
    pos_text = make_pos_dict(text)
    if 'nouns' in parts_to_shuffle:
        nouns = get_nouns(pos_text)
    else:
        nouns = []
    if 'verbs' in parts_to_shuffle:
        verbs = get_verbs(pos_text)
    else:
        verbs = []
    if 'adjs' in parts_to_shuffle:
        adjs = get_adjs(pos_text)
    else:
        adjs = []
    return nouns + verbs + adjs


def shuffle_words(text, wordlist):
    '''wordlist is list words in text be moved around the text'''
    blob = TextBlob(text)
    tokens = list(blob.words)
    indices = get_indices(tokens, wordlist)
    extras = wordlist[:]
    random.shuffle(wordlist)
    random.shuffle(extras)
    for index in indices:
        if wordlist:
            tokens[index] = wordlist[random.randint(0, len(wordlist) - 1)]
        elif extras:
            tokens[index] = extras[random.randint(0, len(wordlist) - 1)]
    return (' '.join(tokens)).lower()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/result', methods=['POST'])
def make_text():
    user_text = request.form['user_text']
    selected = request.form['pos']
    parts = get_parts(user_text, selected)
    new_text = shuffle_words(user_text, parts)
    return json.dumps({'shuffled': new_text})


if __name__ == '__main__':
    app.run(debug=True)
    #port = int(os.environ.get('PORT', 5000))
    #app.run(host='0.0.0.0', port=port)
