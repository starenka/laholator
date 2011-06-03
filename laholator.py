#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Laholator app
# 
# @author:     starenka
# @email:      'moc]tod[liamg].T.E[0aknerats'[::-1]
# @version:    1.1.1
# @since       Jun 1, 2011

import warnings
from os.path import dirname, abspath
from flask import Flask, render_template, request
from flaskext.sqlalchemy import SQLAlchemy

#Hey monkey! NLTK's NgramModel is not serializable w/ pickle.HIGHEST_PROTOCOL (2)
from werkzeug.contrib import cache
cache.HIGHEST_PROTOCOL = 1
from werkzeug.contrib.cache import SimpleCache

from BeautifulSoup import BeautifulSoup
import nltk

app = Flask(__name__)
app.config.from_object('settings')
cache = SimpleCache()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/samples.sqlite3'%abspath(dirname(__file__))
db = SQLAlchemy(app)

class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(80), unique=True)
    text = db.Column(db.String())

    def __init__(self, url, text):
        self.url = url
        self.text = text

    def __unicode__(self):
        str = unicode(BeautifulSoup(self.text,convertEntities=BeautifulSoup.HTML_ENTITIES))
        return nltk.clean_html(str)

    @classmethod
    def get_all(self):
        cached = cache.get('samples')
        if cached is None:
            cached = self.query.all()
            cache.set('samples', cached, timeout=app.config['CACHE_MINUTES'] * 60)
        return cached

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html',title=u"To tady nemáme!"), 404

@app.route('/faq')
def faq():
    return render_template('faq.html',title=u"Často kladené dotazy",samples=Sample.get_all())

@app.route('/')
def index():
    bigrams = request.args.get('bigrams',False)
    try:
        words = int(request.args.get('words',app.config['WORDS']))
    except ValueError:
        words = app.config['WORDS']

    model = _get_ngram_model(bigrams)
    starts = model.generate(100)[-2:]
    generated = model.generate(words, starts)
    out = ' '.join(generated).replace(' , ',', ').replace(' . ','. ')
    out = '%s%s&hellip;'%(out[0].upper(),out[1:])

    return render_template('generator.html',title=u"Henrykuj!",
                           text=out, words = words, bigrams = bigrams
    )

def _get_ngram_model(bigrams):
    #NLTK produces a LOT of warnings - don't mess with my error log
    warnings.simplefilter("ignore")
    cached = cache.get('ngram_model')
    if cached is None:
        samples = Sample.get_all()
        if samples:
            text = [unicode(s) for s in samples]
            tokenizer = nltk.tokenize.WordPunctTokenizer()
            tokenized = tokenizer.tokenize(' '.join(text))
            cached = nltk.NgramModel(3-int(bool(bigrams)), tokenized)
            cache.set('ngram_model', cached, timeout=app.config['CACHE_MINUTES'] * 60)
    return cached

if __name__ == '__main__':
    app.run()