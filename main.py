
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.message import EmailMessage
import datetime
import os
import openai
import random
import sqlite3
from better_profanity import profanity

custom_badwords = ['bite', 'baisable,', 'baise', 'baiser', 'bander', 'branler', 'branlette', 'bordel', 'burnes', 'chatte', 'chiant', 'chiasse', 'chier', 'chiottes', 'con', 'conne', 'connerie', 'coucougnettes', 'couilles', 'couillu', 'cul', 'déconner', 'déconneur', 'emmerder', 'emmerdant', 'emmerdeur', 'empapaouter', 'enculer', 'entuber', 'faire chier', 'faire une pipe', 'foutoir', 'foutre', 'foutre le camp', 'foutu', 'gueule', 'gueuler', 'merde', 'merder', 'merdier', 'merdique', 'niquer', 'nique ta mère', 'pisser', 'putain', 'pute', 'roubignoles', 'roupettes', 'roustons', 'se démerder', 's’emmerder', 'se faire chier', 'se faire sauter', 'sucer', 'ta gueule !', 'tirer un coup', 'turlutte', 'zigounette', 'zob',
                   'alboche', 'boche', 'chleuh', 'doryphore', 'fridolin', 'frisé', 'frisou', 'fritz', 'prussien', 'schleu', 'teuton', 'vert-de-gris', "amerlo", 'amerloque', 'ricain', 'yankee', 'angliche', 'rosbif', 'arbi', 'bic', 'bicot', 'bougnoul', 'bougnoule', 'bronzé', 'crouillat', 'crouille', 'gris', 'melon', 'raton', 'sidi', 'bridé', 'chinetoque', 'bohémien', 'manouche', 'nomade', 'renard à deux pattes', 'rom', 'romanichel', 'romano', 'tsigane', 'tzigane', 'macaroni', 'rital', 'youd', 'youpin', 'youtre', 'bamboula', 'banania', 'black', 'blackos', 'bronzé', 'moricaud', 'nègre', 'négresse', 'négro', 'polack', 'polaque', 'niakoué', 'niaque']

openai.api_key = os.environ["GPT_API"]
model = os.environ["MODEL_ADA"]
model2 = os.environ["MODEL_CURIE"]
my_email = os.environ["MAIL_NAME"]
my_pass = os.environ["MAIL_MDP"]
pr = " \n\n###\n\n"
card_styles = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light']
songs = []

app = Flask(__name__)

## CREATE DATABASE
uri = os.environ.get("DATABASE_URL", "sqlite:///songs-collection.db")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///songs-collection.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///songs-collection.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    text = db.Column(db.String, nullable=False)
    avis = db.Column(db.String(250), nullable=False)
    note = db.Column(db.Integer, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Song {self.title}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(40), nullable=False)
    comment = db.Column(db.String, nullable=False)
    emotion = db.Column(db.String(40), nullable=False)
    date = db.Column(db.String(40), nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Comment {self.nick}>'

db.create_all()

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == "POST":
        text = music_generator(request.form["theme"], int(request.form["longeur"]))
        nom = nom_generator(text)
        content_filter(text)
        txt = text.split("\n")
        new_song = {
            "nom": nom,
            "text": text,
            "avis": '',
            'note': ''
        }
        songs.append(new_song)
        style = random.choice(card_styles)
        # if int(content_filter(text)) == 2:
        #   txt = "Désolé, la chanson générée par l'algorithme contient des elements inappropriés.\n Veuillez essayer à nouveau s'il vous plaît."
        return render_template("index.html", music=txt, nom=nom, date=datetime.date.today().year, style=style, gena=True)
    return render_template("index.html", date=datetime.date.today().year, gena=False)

@app.route('/comments', methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        nick = request.form['nick']
        emotion = request.form['emotion']
        comment = request.form['comment']
        day, month, year = str(datetime.date.today().day), str(datetime.date.today().month), str(datetime.date.today().year)
        new_comment = Comment(nick=nick, comment=comment, emotion=emotion, date=f"{day}/{month}/{year}")
        db.session.add(new_comment)
        db.session.commit()

        all_comments = db.session.query(Comment).all()
        all_comments.reverse()
        return render_template("comments.html", comments=all_comments, len=len(all_comments), date=datetime.date.today().year)
    all_comments = db.session.query(Comment).all()
    all_comments.reverse()
    return render_template("comments.html", comments=all_comments, len=len(all_comments), date=datetime.date.today().year)

@app.route('/songs', methods=['GET', 'POST'])
def get_songs():
    if request.method == 'POST':
        songs[-1]['avis'] = request.form['avis']
        songs[-1]['note'] = int(request.form['note'])
        new_song = Song(title=songs[-1]['nom'], text=songs[-1]['text'], avis=songs[-1]['avis'], note=songs[-1]['note'])
        db.session.add(new_song)
        db.session.commit()

        all_songs = db.session.query(Song).all()
        all_songs.reverse()
        return render_template('songs.html', songs=all_songs, len=len(all_songs))
    all_songs = db.session.query(Song).all()
    all_songs.reverse()
    return render_template("songs.html", songs=all_songs, len=len(all_songs), date=datetime.date.today().year)

@app.route('/song/<int:id_song>', methods=['GET', 'POST'])
def get_song(id_song):
    song = Song.query.filter_by(id=id_song).first()
    text = song.text
    txt = text.split("\n")
    style = random.choice(card_styles)
    return render_template("song.html", song=song, text=txt, style=style, date=datetime.date.today().year)

@app.route('/contact', methods=['GET', 'POST'])
def get_contact():
    if request.method == "POST":
        data = request.form
        try:
            send_email(data["name"], data["email"], data["message"])
            return render_template("msgsent.html", date=datetime.date.today().year, send=True)
        except:
            return render_template("msgsent.html", date=datetime.date.today().year, send=False)
            pass
    return render_template("contact.html", date=datetime.date.today().year)

@app.route('/about')
def get_about():
    return render_template('about.html', date=datetime.date.today().year)

@app.route('/lucky-777-page-111-admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        return render_template('admin.html', done="done")
    return render_template('admin.html', done="")

@app.route('/lucky-777-page-111-admin-as')
def admin_songs():
    all_songs = db.session.query(Song).all()
    all_songs.reverse()
    return render_template("admin_songs.html", songs=all_songs)

@app.route('/lucky-777-page-111-admin-as/<int:id_song>', methods=["POST"])
def delete_song(id_song):
    song_to_delete = Song.query.get(id_song)
    db.session.delete(song_to_delete)
    db.session.commit()
    all_songs = db.session.query(Song).all()
    all_songs.reverse()
    return render_template("admin_songs.html", songs=all_songs)

@app.route('/lucky-777-page-111-admin-ac')
def admin_comments():
    all_comments = db.session.query(Comment).all()
    all_comments.reverse()
    return render_template("admin_comments.html", comments=all_comments)

@app.route('/lucky-777-page-111-admin-ac/<int:id_comment>', methods=['POST'])
def delete_comment(id_comment):
    comment_to_delete = Comment.query.get(id_comment)
    db.session.delete(comment_to_delete)
    db.session.commit()
    all_comments = db.session.query(Comment).all()
    all_comments.reverse()
    return render_template("admin_comments.html", comments=all_comments)

@app.route('/pc', methods=['POST'])
def delete_all_comments():
    db.session.query(Comment).delete()
    db.session.commit()
    return render_template('admin.html', done="DELETED ALL COMMENTS")

@app.route('/ps', methods=['POST'])
def delete_all_songs():
    db.session.query(Song).delete()
    db.session.commit()
    return render_template('admin.html', done="DELETED ALL SONGS")

def nom_generator(text):
    response = openai.Completion.create(
        model=model,
        prompt=f"{text}{pr}",
        stop=" END",
        temperature=1,
        user="uniqueID"
    )
    nom = response['choices'][0]['text']
    return nom

def music_generator(prompt, longeur):
    profanity.add_censor_words(custom_badwords)
    prompt = profanity.censor(prompt)
    response = openai.Completion.create(
        model=model2,
        prompt=prompt,
        stop=" END",
        top_p=1,
        temperature=0.9,
        frequency_penalty=random.choice([0, 0.5]),
        max_tokens=longeur,
        echo=True,
        user="uniqueID"
    )
    text = response['choices'][0]['text']
    return text

def content_filter(text):
    content_to_classify = text

    response = openai.Completion.create(
        engine="content-filter-alpha",
        prompt="<|endoftext|>" + content_to_classify + "\n--\nLabel:",
        temperature=0,
        max_tokens=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        logprobs=10,
        user="uniqueID"
    )

    output_label = response["choices"][0]["text"]
    print(f"output_label1 is {output_label}")
    # This is the probability at which we evaluate that a "2" is likely real
    # vs. should be discarded as a false positive
    toxic_threshold = -0.355

    if output_label == "2":
        # If the model returns "2", return its confidence in 2 or other output-labels
        logprobs = response["choices"][0]["logprobs"]["top_logprobs"][0]

        # If the model is not sufficiently confident in "2",
        # choose the most probable of "0" or "1"
        # Guaranteed to have a confidence for 2 since this was the selected token.
        if logprobs["2"] < toxic_threshold:
            logprob_0 = logprobs.get("0", None)
            logprob_1 = logprobs.get("1", None)

            # If both "0" and "1" have probabilities, set the output label
            # to whichever is most probable
            if logprob_0 is not None and logprob_1 is not None:
                if logprob_0 >= logprob_1:
                    output_label = "0"
                else:
                    output_label = "1"
            # If only one of them is found, set output label to that one
            elif logprob_0 is not None:
                output_label = "0"
            elif logprob_1 is not None:
                output_label = "1"

            # If neither "0" or "1" are available, stick with "2"
            # by leaving output_label unchanged.

    # if the most probable token is none of "0", "1", or "2"
    # this should be set as unsafe
    if output_label not in ["0", "1", "2"]:
        output_label = "2"

    print(f"output_label2 is {output_label}")
    return output_label

def send_email(name, email, message):
    msg = EmailMessage()
    msg['From'] = my_email
    msg['To'] = my_email
    msg['Subject'] = "MusiqueIA email"
    msg.set_content(f"Name: {name}\nEmail: {email}\nMessage: \n{message}")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_pass)
        connection.send_message(msg)
"""
def send_email(name, email, message):
    email_message = f"Name: {name}\nEmail: {email}\nMessage: \n{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(my_email, my_pass)
        connection.sendmail(my_email, my_email, email_message)
"""
if __name__ == "__main__":
    app.run(debug=True)
