from flask import Flask, request, jsonify
from data_loader import read_data
from database import DocumentBase

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def upload_excel():
    try:
        file = request.files["file"]
        if file.filename.endswith(".xlsx"):
            df1, df2, df3 = read_data(file)
            db = DocumentBase(
                "neo4j+s://4c66c8b1.databases.neo4j.io",
                "neo4j",
                "y8-ueDTOtmpUbjkZcZxjgNzlRUpTK_QPxg2s10de7tc",
            )
            db.add_authors(df1)
            db.add_sections(df2)
            db.add_section_refs(df3)

            return jsonify({"message": "Data uploaded to Neo4j successfully"})
        return jsonify({"error": f"Error: {str(e)}"})
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"})
