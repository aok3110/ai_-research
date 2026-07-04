from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

from services.search import find_official_website
from services.crawler import crawl_website
from services.ai import analyze_company
from services.serp import find_competitors
from services.pdf_generator import generate_pdf
from flask import send_file

import os


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/research", methods=["POST"])
def research():

    data = request.get_json()
    company = data.get("company")

    website = find_official_website(company)

    text = ""
    if website:
        text = crawl_website(website)

    analysis = analyze_company(text, company)

    competitors = find_competitors(company)

    # create reports folder if not exists
    os.makedirs("reports", exist_ok=True)

    pdf_path = generate_pdf(
        company,
        website,
        analysis,
        competitors
    )

    return jsonify({
        "company": company,
        "website": website,
        "analysis": analysis,
        "competitors": competitors,
        "pdf": pdf_path
    })
@app.route("/download-pdf/<filename>")
def download_pdf(filename):
    return send_file(f"reports/{filename}", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)