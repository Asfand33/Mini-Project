from flask import Flask, render_template, request, redirect, url_for
import requests



app = Flask(__name__)

Programs = requests.get("https://cms.mlcs.xyz/api/view/program_sessions/all/")
Students_Data = requests.get("https://cms.mlcs.xyz/api/view/students_of/bscs-2016/all/")
Staff_Data = requests.get("https://cms.mlcs.xyz/api/view/teaching_staff/all/")
TeamMembers = []
Supervisor_Details = []



@app.route('/', methods=['GET', "POST"])
def home():
    if request.method == "POST":
        global ProgramName
        data = request.form["nm"]
        data = data.split(",")
        ProgramName = data[1][2:-1].replace("-", "_")
        return redirect(url_for("fun", name=data[1]))
    else:
        return render_template("home.html", name=Programs.json())


@app.route("/<name>", methods=["GET", "POST"])
def fun(name):
    if request.method == "POST":
        data = request.get_json()
        for i in range(3):
            splited = data[0]["Member" + str(i + 1)].split("\t")
            TeamMembers.append(splited)
        return data
    else:
        matched_data = []
        for item in Students_Data.json():
            if name[2:-1] == item["student_roll_number"][:len(name[1:-2])]:
                matched_data.append(item)
        return render_template("students.html", name=name, data=matched_data)


@app.route("/supervisor", methods=["GET", "POST"])
def supervisor():
    if request.method == "POST":
        data = request.get_json()
        splited = data["Supervisor"].split("\t")
        Supervisor_Details.append(splited)
        return data
    else:
        return render_template("supervisor.html", data=Staff_Data.json())


@app.route("/team", methods=["GET", "POST"])
def team():
    if request.method == "POST":
        Details = request.get_json()
    else:
        return render_template("team.html", SPD=Supervisor_Details, MD=TeamMembers)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
