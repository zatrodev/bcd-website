from flask import Blueprint, render_template, request, redirect, url_for, session

bp = Blueprint('views', __name__)


@bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        lrn = request.form.get("lrn")

        from .api.firebase import DatabaseService
        db = DatabaseService()

        user_info = db.get_data_with_lrn(lrn)
        if user_info:
            session["user_info"] = user_info
            return redirect(url_for("views.home", lrn=lrn))

        return render_template("login.html", invalid_display="block", lrn=lrn)

    return render_template("login.html", invalid_display="none")


@bp.route("lrn/<lrn>")
def home(lrn):
    user_info = session["user_info"]
    return render_template("home.html", user_info=user_info)
