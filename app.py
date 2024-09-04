from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Veritabanı Modeli tanımlama
class UserScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)

# Veritabanını oluşturma
with app.app_context():
    db.create_all()

# Anasayfa
@app.route('/')
def index():
    highest_score = db.session.query(db.func.max(UserScore.score)).scalar()
    return render_template('index.html', highest_score=highest_score)

# Sonuçları Gösterme
@app.route('/submit', methods=['POST'])
def submit():
    # Soruların yanıtlarını al ve karşılaştırma için lower fonksiyonuna tabi tut
    answers = {
        1: request.form.get('questions[1]').strip().lower(),
        2: request.form.get('questions[2]').strip().lower(),
        3: request.form.get('questions[3]').strip().lower(),
        4: request.form.get('questions[4]').strip().lower()
    }

    # Doğru cevaplar
    correct_answers = {
        1: 'görüntü verileri',
        2: 'opencv',
        3: 'derin öğrenme',
        4: 'cnn'
    }

    # Puan hesaplaması
    score = sum(25 for i in range(1, 5) if answers[i] == correct_answers.get(i))

    # Puanı veritabanına kaydet
    new_score = UserScore(score=score)
    db.session.add(new_score)
    db.session.commit()

    # En yüksek puanı bulma işlemi
    highest_score = db.session.query(db.func.max(UserScore.score)).scalar()

    return render_template('result.html', score=score, highest_score=highest_score)

if __name__ == '__main__':
    app.run(debug=True)
