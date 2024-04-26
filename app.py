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
   
    answer =  db.Column(db.String)
    assessmentid =  db.Column(db.String)



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

@app.route('/view-progress')
def progress():  
    studentdata = studentData.query.all()  
    # inner join answwerscriptData with students to get the correspoding grades
    print(studentdata)
    return render_template('preview.html',data =studentdata)
    
@app.route('/create-evaluation')
def facinput():  
    return render_template('facultyinput.html')


@app.route('/create-new-evaluation',methods=['POST','GET'])
def createnew():    
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        assessmentdata =assessmentData(question = question , answer = answer)
        db.session.add(assessmentdata)
        db.session.commit()
        with open("answerkeys.txt", "w") as file:
            file.write(answer)
    return render_template('upload.html')
    

@app.route('/upload',methods=['POST','GET'])
def upload():    
    if request.method == 'POST':
        # Get the uploaded file
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
        studdata = studentData(name = name,register_number = register_number,mark_scored = mark_scored)
        db.session.add(studdata)
        db.session.commit()
        return render_template('success.html',keys=mark_scored)
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)

