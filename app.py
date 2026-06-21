from flask import Flask

app = Flask(__name__)

HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Cloud Engineering Demo</title>
<style>
    body { font-family: -apple-system, Segoe UI, sans-serif; background: #0b1020; color: #eaf1ff;
            display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    .card { background: #131b3a; padding: 48px 64px; border-radius: 16px;
            box-shadow: 0 12px 40px rgba(0,0,0,.5); text-align: center; }
    h1 { font-weight: 600; margin: 0 0 8px; font-size: 28px; }
    p  { opacity: .7; margin: 0; }
</style>
</head>
<body>
<div class="card">
    <h1>Hello Naim, welcome to my cloud engineering demo.</h1>
    <p>Deployed by Sinartisis Cloud Engineer on Azure App Service.</p>
</div>
</body>
</html>"""

@app.route("/")
def home():
    return HTML

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)