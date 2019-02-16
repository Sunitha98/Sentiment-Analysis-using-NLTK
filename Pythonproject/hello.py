from __future__ import print_function
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer  
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize   
from flask import Flask, render_template,request
app = Flask(__name__,template_folder='templates')
@app.route('/')
def home():
    return render_template('index.html')  

def preprocessing(sentence):
    sentence=sentence.lower()
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence) 
    filtered_sentence = [w for w in word_tokens if not w in stop_words or w=='not']
    filtered_sentence= " ".join(filtered_sentence)
    tagged_sentence = nltk.tag.pos_tag(filtered_sentence.split())
    edited_sentence = [word for word,tag in tagged_sentence if tag != 'NNP' and tag != 'NNPS' and tag!='NN' and tag!='NNS']
    return (' '.join(edited_sentence))
     

@app.route('/actionPage', methods = ['POST'])
def actionPage():
    input_sentence=request.form.get('sentence')
    sent=preprocessing(input_sentence)
    sid = SentimentIntensityAnalyzer()
    ss = sid.polarity_scores(sent)
    if sent==' ':
                return render_template('neutral.html')
    mx=0.0
    vals=''
    for k in ss:
        if(mx<ss[k]):
            mx=ss[k]
            vals=k
    if(vals=='pos'):
        return render_template('positive.html')
    elif(vals=='neg'):
        return render_template('negative.html')
    else:
        return render_template('neutral.html')
                                 
if __name__ == '__main__':
    app.run(debug=True)       
       