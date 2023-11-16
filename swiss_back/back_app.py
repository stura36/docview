from flask import Flask, request, jsonify
from data_loader import read_data
from data_driver import DocumentBase
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload_excel():
    try:
        file = request.files["file"]
        if file.filename.endswith(".xlsx"):
            df1, df2, df3 = read_data(file)
            db = DocumentBase(
                os.getenv("NEO4J_URI"),
                os.getenv("NEO4J_USER"),
                os.getenv("NEO4J_PASSWORD"),
            )
            db.add_authors(df1)
            db.add_sections(df2)
            db.add_section_refs(df3)

            return jsonify({"message": "Data uploaded to Neo4j successfully"})
        return jsonify({"error": f"Error: {str(e)}"})
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"})
