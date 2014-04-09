from web import app, config
from web.routes import AGENCY_ROOT_PATH
from flask import flash, request, redirect, render_template, url_for

import os, time,re

from agency_tools.streamhub_app_generator import Generator, get_versions

@app.route(AGENCY_ROOT_PATH)
@app.route(AGENCY_ROOT_PATH + "/")
def agency_root():
	return "Something!"

@app.route(os.path.join(AGENCY_ROOT_PATH, "tools", "generate-app/"), methods=["GET"])
def generate_app():
    return render_template("generate-app.html")

@app.route(os.path.join(AGENCY_ROOT_PATH, "tools", "generate-app-submit/"), methods=["POST"])
def generate_app_submit():
    output_dir = config["generate_app"]["output_dir"]
    client = request.form.get("client").replace(" ", "_")
    project = request.form.get("project").replace(" ", "_")
    timestamp = str(int(time.time()))
    filename =  client + "_" + project + "_"+ timestamp + ".html"
    wall_ids = []
    list_ids = []
    view_type_regex = re.compile("viewType(\d+)")

    for item in request.form:
        result = view_type_regex.search(item)
        if result:
            if request.form.get(item) == "wall":
                
                wall_ids.append(request.form.get("articleId" + result.groups()[0]))
            elif request.form.get(item) == "feed":
                list_ids.append(request.form.get("articleId" + result.groups()[0]))

    # TODO: 
    # The get_version method expects these params and then adds the
    # versions into the dict based upon what ids are provided. Until
    # I make get_versions accept params and return shit... I have to
    # do this stupid hack job.
    versions = {
        "wall_version": "",
        "sdk_version": "",
        "wall_article_ids": wall_ids,
        "list_article_ids": list_ids
    }
    get_versions(versions)

    generator = Generator(
        network=request.form.get("network"),
        site_id=request.form.get("siteId"),
        wall_article_ids=wall_ids,
        list_article_ids=list_ids,
        sdk_version=versions["sdk_version"],
        wall_version=versions["wall_version"],
        filename=os.path.join(output_dir, filename)
    )
    generator.generate_html()

    flash(filename)
    return redirect(url_for("generate_app"))