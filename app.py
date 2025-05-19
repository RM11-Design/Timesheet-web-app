from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from docxtpl import DocxTemplate
from datetime import datetime
from sqlalchemy.sql import func
import time
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    def __repr__(self):
        return f'<Job {self.department}>'
    
@app.route('/')
def index():
    jobs = Job.query.all()
    return render_template('index.html', jobs=jobs)

@app.route('/<int:job_id>/')
def job(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('job.html', job=job)

@app.route('/', methods=['GET', 'POST'])
def UCC_login_in():

# Set variables to zero, otherwise the web app crashes
    total_salary = 0
    week_one_date = week_two_date = week_three_date = week_four_date = week_five_date = None
    two_months = None
    today_date = None
    week_one_hours = week_two_hours = week_three_hours = week_four_hours = week_five_hours = 0

    if request.method == 'POST':
        week_one_date = request.form.get("prothom_shopta")
        week_two_date = request.form.get("second_shopta")
        week_three_date = request.form.get("third_shopta")
        week_four_date = request.form.get("fourth_shopta")
        week_five_date = request.form.get("fifth_shopta")

        today_date = datetime.today().strftime("%d-%b-%y")


        try:
            week_one_hours = float(request.form.get("week_hours_one"))
            week_two_hours = float(request.form.get("week_hours_two"))
            week_three_hours = float(request.form.get("week_hours_three"))
            week_four_hours = float(request.form.get("week_hours_four"))
            week_five_hours = float(request.form.get("week_hours_five"))

            two_months = request.form.get("dui_mash")
            print(two_months)

            # Calculate total hours and salary
            total_hours = week_one_hours + week_two_hours + week_three_hours + week_four_hours + week_five_hours
            wage_and_hours = 13.50 * total_hours
            holiday_pay = wage_and_hours * 0.08
            total_salary = wage_and_hours + holiday_pay

            print(total_salary)

            time.sleep(4)

            # Load the template

            doc = DocxTemplate("C:\\Users\\tmrom\\OneDrive\\Desktop\\Python\\PushingTheBoundaries\\UCC_automated_web_app\\Hourly Timesheet template (business edition).docx")

            today_date = datetime.today().strftime("%d %b, %y")

            # Information to populate the Word template
            all_info = {
                "two_months": two_months,
                "w1": week_one_date,
                "w2": week_two_date,
                "w3": week_three_date,
                "w4": week_four_date,
                "w5": week_five_date,
                "week_one": week_one_hours,
                "week_two": week_two_hours,
                "week_three": week_three_hours,
                "week_four": week_four_hours,
                "week_five": week_five_hours,
                "hrs": total_hours,
                "wage_and_hours": round(wage_and_hours, 2),
                "holiday_pay": round(holiday_pay, 2),
                "total_salary": round(total_salary, 2),
                "today_date": today_date
            }

            # Render and save the document
            doc.render(all_info)
            doc.save(f"C:\\Users\\tmrom\\OneDrive\\Desktop\\Python\\PushingTheBoundaries\\UCC_automated_web_app\\Hourly Timesheet template {two_months}.docx")
        
        except ValueError:
            print("Invalid")
        
    return render_template('user_portal.html',
                                two_months=two_months,
                                today_date=today_date,
                                week_one_date=week_one_date,
                                week_two_date=week_two_date,
                                week_three_date=week_three_date,
                                week_four_date=week_four_date,
                                week_five_date=week_five_date,
                                week_one_hours=week_one_hours,
                                week_two_hours=week_two_hours,
                                week_three_hours=week_three_hours,
                                week_four_hours=week_four_hours,
                                week_five_hours=week_five_hours,
                                total_salary=total_salary)

if __name__ == '__main__':
    app.run(debug=True)
