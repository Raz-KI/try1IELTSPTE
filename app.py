from flask import Flask, render_template, request, jsonify, redirect, url_for,session
import json
from groq import Groq
import os

app = Flask(__name__)


app.secret_key = os.urandom(24)

# Initialize your groqAI client (replace with your actual API key)
client = Groq(
    api_key="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"
)

# session["exam_type"]=""
# session["ielts_section"]=""
default_prompt="""
You are an intelligent assistant designed to help students prepare for the IELTS / CELLPIP exam. Your goal is to provide accurate, clear, and helpful guidance. 

                    When responding to students, always ensure that your tone is friendly, supportive, and motivating. Provide explanations, examples, and detailed feedback when needed. Avoid overwhelming the student with too much information at once, and try to keep responses simple and easy to understand.
                    Be proactive in offering helpful resources like practice exercises, links to useful materials, or suggesting areas to focus on for improvement.
                    
                    Right now you want the user to choose between IELTS or CELLPIP (there are two buttona on the webpage, one for ielts and one for cellpip, ask the user to select one)

                    """



def answer_rater(user_message):
    system_content = """
                    You are an online IELTS writing test checker who will assess the candidate's answer and will give the overall band, strengths and areas of improvements, tips to score more.
                    """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_message}
        ],
        model="llama3-8b-8192"
    )

    return chat_completion.choices[0].message.content

def AMAI_assistant(user_message,sys_prompt):
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_message}
        ],
        model="llama3-8b-8192"
    )
    return chat_completion.choices[0].message.content

@app.route('/')
def home():
    return render_template('home.html',firstquestion="Hello fellow student I am AM.AI, your personal language exam assistant. I will be with you all along your Language exams prep. So lets begin, choose an exam you want to excel in ;).")

@app.route('/ielts')
def ielts():
    session["exam_type"]="ielts"
    session["ielts_section"]=""
    return render_template('ielts.html')

@app.route('/inprogress')
def inprogress():
    return render_template('inprogress.html')



@app.route('/general')
def general():
    return render_template('general.html')

@app.route('/academic')
def academic():
    return render_template('academic.html')

@app.route('/academic/reading')
def reading():
    return render_template('reading.html')

@app.route('/academic/writing')
def writing():
    return render_template('writing.html')

@app.route('/academic/listening')
def listening():
    return render_template('listening.html')

@app.route('/academic/speaking')
def speaking():
    return render_template('speaking.html')

@app.route('/get_assistance', methods=['POST'])
def get_assistance():
    
    examtype=session.get("exam_type")
    sys_prompt=default_prompt
    if examtype=="ielts":
        sys_prompt="""
                    You are an intelligent assistant designed to help students prepare for the IELTS exam. Your goal is to provide accurate, clear, and helpful guidance. 

                    When responding to students, always ensure that your tone is friendly, supportive, and motivating. Provide explanations, examples, and detailed feedback when needed. Avoid overwhelming the student with too much information at once, and try to keep responses simple and easy to understand.
                    Be proactive in offering helpful resources like practice exercises, links to useful materials, or suggesting areas to focus on for improvement.
                   """
        print("ye baat")
    user_message = request.json['user_input']
    navigation = request.json['navigation']

    question =AMAI_assistant(user_message or navigation,sys_prompt)
    
    return jsonify({"question": question})
    


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_answer = request.json['answer']
    # Get the rating from the answer_rater function
    rating = answer_rater(user_answer)
    # Pass the rating to the rating page directly
    return render_template('rating.html', rating=rating)

@app.route('/rating')
def rating():
    # Just render the rating page; no need to handle rating here
    return render_template('rating.html')

if __name__ == '__main__':
    app.run(debug=True)

