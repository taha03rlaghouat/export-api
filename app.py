from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

@app.route("/")
def index():
    return "✅ API شغال! جرّب زيارة /export للحصول على LaTeX"

@app.route("/export")
def export():
    conn = pymysql.connect(
        host='sql213.infinityfree.com',
        user='if0_38641180',
        password='Jo9hWNjcxFiZf',
        database='if0_38641180_udemy_db',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with conn.cursor() as cursor:
        cursor.execute("SELECT lemma, translation, pronunciation FROM tokens WHERE translation IS NOT NULL AND pronunciation IS NOT NULL")
        rows = cursor.fetchall()

    latex = render_template("vocab_template.tex.j2", rows=rows)
    return latex  # فقط يعرض LaTeX في المتصفح
