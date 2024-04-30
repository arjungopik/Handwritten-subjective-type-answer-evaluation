from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import subprocess
import os
from pdf2image import convert_from_path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:user@localhost:5432/evaluation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class studentData(db.Model):
    __tablename__ = 'studentdata'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    register_number = db.Column(db.String)
    mark_scored =  db.Column(db.String)
    assessmentid =  db.Column(db.String)





class answerscriptData(db.Model):
    __tablename__ = 'answerscripts'  
    id = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.Integer)
    assessmentid =  db.Column(db.String)
    answer =  db.Column(db.String)
    mark_scored = db.Column(db.String)



class assessmentData(db.Model):
    __tablename__ = 'assessment'  
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer =  db.Column(db.String)
    




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login',methods=['POST','GET'])
def login():    
    if request.method == 'POST':
        return render_template('choose.html')

@app.route('/view-progress',methods = ['POST'])
def progress():
    if request.method == 'POST':
        id = request.form.get('question')
        result = studentData.query.filter_by(assessmentid=id).all()
        return render_template('preview.html',data = result)
    
@app.route('/create-evaluation')
def facinput():  
    return render_template('facultyinput.html')

@app.route('/answer-evaluation')
def anseval():  
    questions = assessmentData.query.all()  

    return render_template('questionselection.html',datas=questions)

@app.route('/choose-question')
def choosequestion():  
    questions = assessmentData.query.all()  
    return render_template('assessmentselection.html',datas=questions)


@app.route('/process_question',methods =['POST'] )
def questionselection():
    if request.method == 'POST':
        id = request.form.get('question')
    return render_template('upload.html',data = id)



@app.route('/create-new-evaluation',methods=['POST','GET'])
def createnew():    
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        # sentance transformer

        assessmentdata =assessmentData(question = question , answer = answer)
        db.session.add(assessmentdata)
        db.session.commit()
        
    return render_template('choose.html')
    

@app.route('/view/<studid>/<assessid>',methods=['POST','GET'])
def view(studid,assessid):

    result = answerscriptData.query.filter_by(assessmentid=assessid, studentid=studid).with_entities(answerscriptData.answer).all()
    result = str(*result.pop(0))
    return render_template('view.html',data = result)

@app.route('/upload/<id>',methods=['POST','GET'])
def upload(id):
    if request.method == 'POST':
       
        result = assessmentData.query.filter_by(id=id).with_entities(assessmentData.answer).all()
        with open("answerkeys.txt", 'w') as file:
            file.write(str(*result.pop(0)))

        uploaded_file = request.files['file']


        newfilename = "answerscript.pdf"
        # Save the file to the current directory
        file_path = os.path.join(os.getcwd(), newfilename)
        uploaded_file.save(file_path)
        name = request.form['name']
        register_number = request.form['register_number']
        
        # pdf converter
        images = convert_from_path ('answerscript.pdf',500,poppler_path = "C:\\Program Files\\poppler-24.02.0\\Library\\bin")                
        for i in range(len(images)):
            images[i].save('data/page/page'+str(i)+'.png')

        subprocess.run(["python", "main.py"], check=True)
        with open("mark.txt", "r") as file:
            mark_scored = file.read()
        studdata = studentData(name = name,register_number = register_number,mark_scored = mark_scored,assessmentid = id)
        
        with open("output.txt", "r") as file:
            answer = file.read()
        db.session.add(studdata)
        db.session.commit()
        studid = studdata.id
        print(studid)
        answerscript = answerscriptData(studentid = studid,assessmentid= id ,answer = answer ,mark_scored = mark_scored)
        db.session.add(answerscript)
        
        db.session.commit()
        return render_template('success.html',keys=mark_scored)
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)

