from flask import Flask, send_file, make_response
import pymysql
import os
from jinja2 import Template
import subprocess

app = Flask(__name__)
DB_CONFIG = {
    "host": "sql213.infinityfree.com",
    "user": "if0_38641180",
    "password": "Jo9hWNjcxFiZf",
    "database": "if0_38641180_udemy_db",
    "charset": "utf8mb4"
}

@app.route("/preview")
def generate_pdf():
    # الاتصال بقاعدة البيانات
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT lemma, translation, pronunciation FROM tokens WHERE translation IS NOT NULL AND pronunciation IS NOT NULL")
    rows = cur.fetchall()
    conn.close()

    # تحميل قالب LaTeX
    with open("templates/vocab_template.tex.j2", encoding="utf-8") as f:
        template_str = f.read()
    template = Template(template_str)
    rendered_tex = template.render(rows=rows)

    # حفظ ملف .tex
    os.makedirs("generated", exist_ok=True)
    tex_path = "generated/vocab_export.tex"
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(rendered_tex)

    # توليد PDF
    subprocess.run([
        "xelatex", "-interaction=nonstopmode",
        "-output-directory=generated", tex_path
    ])

    pdf_path = "generated/vocab_export.pdf"
    if os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=False)
    return make_response("❌ فشل توليد PDF", 500)

if __name__ == "__main__":
    app.run()
