from flask import Flask, render_template, request
from datetime import date, datetime
from smtplib import SMTP
import os
import requests
from dotenv import load_dotenv

application = Flask(__name__)
application.secret_key = os.urandom(12).hex()

year = date.today().year
today = date.today()
events_json = requests.get('https://api.npoint.io/a0fbacdbf8f5e6a731a3').json()

load_dotenv()


def email_message(name, contact_email, body='New Sign up for the newsletter', category='Newsletter'):
    sending_email = os.environ.get('MOD_EMAIL')
    sending_password = os.environ.get('MOD_EMAIL_PASSWORD')
    recipient_email = os.environ.get('RECIPIENT_EMAIL')
    with SMTP('smtp.gmail.com') as connection:
        connection.starttls()
        connection.login(user=sending_email, password=sending_password)
        connection.sendmail(
            from_addr=sending_email,
            to_addrs=recipient_email,
            msg=f'Subject:Contact Form Submission\n\nFrom: {name} at {contact_email}\n'
                f'Category: {category}\n'
                f'Message: {body}',
        )


@application.route('/')
def landing():
    for x in range(len(events_json)):
        my_date = events_json[x]["date"]
        date_object = datetime.strptime(my_date, '%Y-%m-%d').date()
        events_json[x]["date"] = date_object
    return render_template("index.html", current_year=year, events=events_json, today=today)


@application.route('/about-us')
def about_us():
    return render_template("about.html", current_year=year)


@application.route('/contact-us')
def get_contact_page():
    return render_template("contact.html", current_year=year)


@application.route('/contact-success')
def get_contact_success_page():
    return render_template('contact-success.html')


@application.route('/submit', methods=['POST'])
def get_form_sent():
    if request.method == 'POST':
        contact_name = request.form['contact-name']
        contact_email = request.form['contact-email']
        category = request.form['category']
        message = request.form['message']
        email_message(contact_name, contact_email, category, message)
    return application.redirect('/contact-success')


@application.route('/sign-up', methods=['POST', 'GET'])
def newsletter_signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        email_message(name, email)
    return render_template('redirect.html')


@application.route('/post')
def get_full_post():
    id_num = int(request.args["id_num"])
    post_data: dict = {}
    for post in events_json:
        if id_num == post["id"]:
            post_data = post
    return render_template('full-post.html', post_data=post_data)


if __name__ == "__main__":
    application.run(debug=True)