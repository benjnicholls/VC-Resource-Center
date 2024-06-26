from flask import Flask, render_template, request, redirect, send_from_directory
from datetime import datetime, date
from extensions import db, mod_email, links
from utils import email_message, init_login
from flask_admin import Admin
from models import User, Post, SponsorClick
from views import UserView, EventView, CustomIndexView, LogoutView, ClickView
from config import Config
from sqlalchemy import asc

application = Flask(__name__)
application.config.from_object(Config)
init_login(application)
db.init_app(application)


# renders the landing page with the event's data. It will exclude all events that precede the current date.
@application.route('/')
def landing():
    return render_template(
        template_name_or_list="home.html",
        current_year=date.today().year,
    )


@application.route('/events')
def events():
    return render_template(
        template_name_or_list="events.html",
        current_year=date.today().year,
        events=Post.query.order_by(asc(Post.date)).all(),
        today=datetime.now()
    )


# gets the post selected data and displays it as a full page
@application.route('/post')
def get_full_post():
    id_num = int(request.args["id"])
    post_data = db.get_or_404(Post, id_num)

    return render_template(
        template_name_or_list='full-post.html',
        post_data=post_data,
        current_year=date.today().year
    )


@application.route('/donate')
def get_donation_page():
    return render_template(
        template_name_or_list='donations.html',
        current_year=date.today().year
    )


# a route for the footer on any html page to go to in order to send a notification that someone has signed up for the
# newsletter.
@application.route('/sign-up', methods=['POST'])
def newsletter_signup():
    name = request.form['name']
    email = request.form['email']

    email_message(name, email)
    email_message(name, email, to_email=mod_email)
    return redirect('/')


@application.route('/paid-advertisers')
def paid_advertisers_page():
    return render_template('advertisers.html')


@application.route('/about-us')
def about_us():
    return render_template(
        template_name_or_list="about.html",
        current_year=date.today().year
    )


@application.route('/contact-us')
def get_contact_page():
    return render_template(
        template_name_or_list="contact.html",
        current_year=date.today().year
    )


# Adds string stating the contact form sending was successful (since I don't know JS yet)
@application.route('/contact-success')
def get_contact_success_page():
    return render_template(
        template_name_or_list='contact-success.html',
        current_year=date.today().year
    )


# Takes in contact form data from contact.html to send to administrator's email
@application.route('/submit', methods=['POST'])
def get_form_sent():
    if request.method == 'POST':
        contact_name = request.form['contact-name']
        contact_email = request.form['contact-email']
        category = request.form['category']
        message = request.form['message']
        email_message(contact_name, contact_email, message, category)
        email_message(contact_name, contact_email, message, category, to_email=mod_email)
    return application.redirect('/contact-success')


@application.get('/advertisers-tracking')
def advertisers_tracking():
    href = links[request.args["name"]]
    sponsor_click = SponsorClick(sponsor_link=href)
    db.session.add(sponsor_click)
    db.session.commit()

    return redirect(href)


@application.route('/sitemap.xml')
def root_files():
    return send_from_directory(
        directory=f"{application.static_folder}/root-files", path='sitemap.xml'
    )


admin = Admin(
        app=application,
        index_view=CustomIndexView()
    )

admin.add_view(UserView(User, db.session))
admin.add_view(EventView(Post, db.session))
admin.add_view(ClickView(SponsorClick, db.session))
admin.add_view(LogoutView(name='Logout', endpoint='logout'))

if __name__ == "__main__":
    with application.app_context():
        db.create_all()
    application.run()
