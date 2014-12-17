from flask import Flask, render_template, request, redirect
from textblob import TextBlob
from textblob.taggers import NLTKTagger
import random
import os
import nltk

nltk.data.path.append('./nltk_data/')

app = Flask(__name__)

def make_pos_dict(text):
	nltk_tagger = NLTKTagger()
	blob = TextBlob(text, pos_tagger=nltk_tagger)
	pos_words = dict(blob.pos_tags)
	return pos_words

def get_nouns(posword_dict):
	nouns = [str(k) for k, v in posword_dict.iteritems() if (v == u'NNP' or v == u'NN' or v == u'NNS' or v == u'NNPS')]
	return nouns

def get_indices(token_list, noun_list):
	indices = []
	for i in token_list:
		if i in noun_list:
			indices.append(token_list.index(i))
	return indices

def shuffle_nouns(text):
	blob = TextBlob(text)
	tokens = list(blob.words)
	pos_text = make_pos_dict(text)
	nouns = get_nouns(pos_text)
	extra_nouns = nouns[:]
	noun_indices = get_indices(tokens, nouns)
	random.shuffle(nouns)
	random.shuffle(extra_nouns)
	for index in noun_indices:
		if nouns:
			tokens[index] = nouns[random.randint(0, len(nouns) - 1)]
		elif extra_nouns:
			tokens[index] = extra_nouns[random.randint(0, len(nouns) - 1)]
	return (' '.join(tokens)).lower()

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'GET':
		return render_template('index.html')
	else:
		return redirect('/result')

@app.route('/result', methods=['POST'])
def result():
	user_text = request.form['user_text']
	new_text = shuffle_nouns(user_text) #todo: unicode errors :'(
	return render_template('index.html', shuffled=new_text)

if __name__ == '__main__':
    #app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
