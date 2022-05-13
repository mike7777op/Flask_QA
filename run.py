from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, RadioField
from wtforms.validators import InputRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'xxx'

# 設置資料庫URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Aa0975117911@127.0.0.1:3306/flask_test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 60


# 使用app作為參數實例化一個SQLALCHEMY類的對象
db = SQLAlchemy(app)

class Answer(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    fA = db.Column(db.Integer, default=0)
    sA = db.Column(db.Integer, default=0)
    tA = db.Column(db.Integer, default=0)
    forA = db.Column(db.Integer, default=0)
    fivA = db.Column(db.Integer, default=0)
    sixA = db.Column(db.Integer, default=0)
    sevA = db.Column(db.Integer, default=0)
    eigA = db.Column(db.Integer, default=0)
    ninA = db.Column(db.Integer, default=0)

    def __init__(self, fA, sA, tA, forA, fivA, sixA, sevA, eigA, ninA):
        self.fA = fA
        self.sA = sA
        self.tA = tA
        self.forA = forA
        self.fivA = fivA
        self.sixA = sixA
        self.sevA = sevA
        self.eigA = eigA
        self.ninA = ninA

# 創建資料庫
db.create_all()

class QAForm(FlaskForm):
    FQ = RadioField(label='自在', coerce=int, choices=[(1,'有'),(-1,'沒有')], validators=[InputRequired()])
    SQ = RadioField(label='安全感', coerce=int, choices=[(1,'有'),(-1,'沒有')], validators=[InputRequired()])
    TQ = RadioField(label='整潔(內心感受)', coerce=int, choices=[(1,'有'),(-1,'沒有')], validators=[InputRequired()])
    ForQ = RadioField(label='開心', coerce=int, choices=[(1,'有'),(-1,'沒有')], validators=[InputRequired()])
    FivQ = RadioField(label='努力', coerce=int, choices=[(1,'有'),(-1,'沒有')], validators=[InputRequired()])
    SixQ = RadioField(label='體貼', coerce=int, choices=[(1,'有'),(-1,'沒有')], validators=[InputRequired()])
    SevQ = RadioField(label='浪漫', coerce=int, choices=[(1,'有'),(-1,'沒有')], validators=[InputRequired()])
    EigQ = RadioField(label='不切實際', coerce=int, choices=[(1,'有'),(-1,'沒有')], validators=[InputRequired()])
    NinQ = RadioField(label='失望', coerce=int, choices=[(1,'有'),(-1,'沒有')], validators=[InputRequired()])

    submit = SubmitField(label='送出資料')

@app.route('/', methods =['GET','POST'])
def login():
    error = None
    if request.method == "POST":
        if request.form['username'] != 'garypu445' or request.form['password'] != '1234':
            error = 'Invailed account'
        else:
            flash('Login successfully')
            return redirect(url_for('index'))
        
    return render_template('login.html', error=error)

@app.route('/index', methods=['GET','POST'])
def index():
    form = QAForm()
    if request.method == "POST":
        if form.validate_on_submit():
            FA = int(request.form.get('FQ'))
            SA = int(request.form.get('SQ'))
            TA = int(request.form.get('TQ'))
            ForA = int(request.form.get('ForQ'))
            FivA = int(request.form.get('FivQ'))
            SixA = int(request.form.get('SixQ'))
            SevA = int(request.form.get('SevQ'))
            EigA = int(request.form.get('EigQ'))
            NinA = int(request.form.get('NinQ'))

            # 取得資料庫數據
            ans = Answer.query.filter_by(id=1).first()

            # 更新分數
            ans.fA = FA + ans.fA
            ans.sA = SA + ans.sA
            ans.tA = TA + ans.tA
            ans.forA = ForA + ans.forA
            ans.fivA = FivA + ans.fivA
            ans.sixA = SixA + ans.sixA
            ans.sevA = SevA + ans.sevA
            ans.eigA = EigA + ans.eigA
            ans.ninA = NinA + ans.ninA

            # 題交數據
            db.session.commit()
            return redirect(url_for('result'))
            
        else:
            print('error')

    return render_template('index.html', form=form)

@app.route('/result', methods=['GET','POST'])
def result():
    ans_info = Answer.query.filter_by(id=1).first()
    fA = ans_info.fA
    fA_str = str(abs(ans_info.fA)*3.33)+'%'

    sA = ans_info.sA
    sA_str = str(abs(ans_info.sA)*3.33)+'%'

    tA = ans_info.tA
    tA_str = str(abs(ans_info.tA)*3.33)+'%'

    forA = ans_info.forA
    forA_str = str(abs(ans_info.forA)*3.33)+'%'

    fivA = ans_info.fivA
    fivA_str = str(abs(ans_info.fivA)*3.33)+'%'

    sixA = ans_info.sixA
    sixA_str = str(abs(ans_info.sixA)*3.33)+'%'

    sevA = ans_info.sevA
    sevA_str = str(abs(ans_info.sevA)*3.33)+'%'

    eigA = ans_info.eigA
    eigA_str = str(abs(ans_info.eigA)*3.33)+'%'

    ninA = ans_info.ninA
    ninA_str = str(abs(ans_info.ninA)*3.33)+'%'

    return render_template('result.html', fA=fA, fA_str= fA_str, sA=sA, sA_str=sA_str, tA=tA, tA_str=tA_str, forA=forA, forA_str=forA_str,fivA=fivA, fivA_str=fivA_str, sixA=sixA, sixA_str=sixA_str, sevA=sevA, sevA_str=sevA_str, eigA=eigA, eigA_str=eigA_str, ninA=ninA, ninA_str=ninA_str)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True)
