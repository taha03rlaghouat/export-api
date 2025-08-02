from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)
app.config['DEBUG'] = True  # لتفعيل عرض الأخطاء أثناء التطوير

@app.route("/")
def index():
    return "✅ API شغال! جرّب زيارة /export للحصول على LaTeX"

@app.route("/export")
def export():
    try:
        # الاتصال بقاعدة البيانات
        conn = pymysql.connect(
            host='sql213.infinityfree.com',
            user='if0_38641180',
            password='Jo9hWNjcxFiZf',
            database='if0_38641180_udemy_db',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT lemma, translation, pronunciation
                FROM tokens
                WHERE translation IS NOT NULL AND pronunciation IS NOT NULL
            """)
            rows = cursor.fetchall()

        # عرض البيانات باستخدام قالب LaTeX
        latex = render_template("vocab_template.tex.j2", rows=rows)
        return latex

    except Exception as e:
        return f"❌ Error: {e}", 500
