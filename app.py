# app.py
from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# College FAQ data
college_faq = {
    "Does the college have a football team?":
        "Yes, our college has a competitive Division II football team called the Panthers. They play at the Wilson Stadium which has a capacity of 25,000 spectators. The team has won 3 regional championships in the last decade.",

    "Does it offer a Computer Science major?":
        "Yes, we offer a comprehensive Computer Science program with specializations in Artificial Intelligence, Cybersecurity, Data Science, and Software Engineering. Our CS department has 45 faculty members and maintains partnerships with major tech companies for internship opportunities.",

    "What is the in-state tuition?":
        "The in-state tuition is $9,500 per semester. This includes access to all campus facilities, library services, and basic health services. Financial aid and scholarship opportunities are available for qualifying students.",

    "Does it provide on-campus housing?":
        "Yes, we have 12 residence halls providing on-campus housing options for over 5,000 students. Housing options include traditional dormitories, suite-style living, and apartment-style accommodations. Prices range from $3,200 to $5,500 per semester depending on the type of accommodation."
}


# Routes
@app.route('/')
def index():
    # Reset the session when starting a new chat
    session.clear()
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    # Get user information on first submission
    if 'user_info' not in session:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        # Store user info in session
        session['user_info'] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email
        }

        # Start the conversation
        return render_template('chat.html',
                               user_info=session['user_info'],
                               faq_questions=list(college_faq.keys()),
                               chat_history=[])

    # Process questions after user info is collected
    else:
        question = request.form.get('question')
        chat_history = session.get('chat_history', [])

        if question in college_faq:
            answer = college_faq[question]
            chat_history.append({"question": question, "answer": answer})
            session['chat_history'] = chat_history

        # Check if all questions have been answered
        all_answered = all(q in [entry["question"] for entry in chat_history] for q in college_faq)

        return render_template('chat.html',
                               user_info=session['user_info'],
                               faq_questions=list(college_faq.keys()),
                               chat_history=chat_history,
                               all_answered=all_answered)


@app.route('/conclusion')
def conclusion():
    if 'user_info' not in session:
        return redirect(url_for('index'))

    creator_info = {
        'first_name': 'Lalith',
        'last_name': 'Venkat',
        'email': 'Lalithvenkat.samanthapudi@gmail.com'  # Replace with your school email
    }

    return render_template('conclusion.html',
                           user_info=session['user_info'],
                           creator_info=creator_info)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)