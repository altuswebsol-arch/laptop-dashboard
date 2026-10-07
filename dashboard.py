"""
Asif Bhai's Laptop Dashboard — Web version
Koi Telegram nahi, koi token nahi!
Bas chalao aur browser mein kholo: http://localhost:5000
"""
from flask import Flask, render_template_string, request, send_file
import webbrowser
import io

app = Flask(__name__)

# Bara aur saaf design (Asif Bhai ke liye!)
PAGE = """
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Asif Bhai ka Bot</title>
<style>
body{font-family:Arial;background:#0a0f24;color:#fff;text-align:center;padding:30px;margin:0}
h1{font-size:36px;color:#10B3FE}
.btn{display:block;width:90%;max-width:400px;margin:15px auto;padding:25px;
font-size:26px;font-weight:bold;color:#04121f;background:#10B3FE;
border:none;border-radius:15px;cursor:pointer;text-decoration:none}
.btn:active{transform:scale(0.97)}
input{width:85%;max-width:380px;padding:18px;font-size:22px;border-radius:12px;
border:2px solid #10B3FE;background:#111832;color:#fff;margin:10px}
.msg{font-size:22px;color:#7CFC00;margin:15px;min-height:30px}
img{max-width:95%;border-radius:10px;margin-top:15px;border:2px solid #10B3FE}
</style></head><body>
<h1>🤖 Asif Bhai ka Bot</h1>
<div class="msg">{{msg}}</div>
<a class="btn" href="/shot">📸 Screenshot Lo</a>
<form action="/open" method="post">
<input type="text" name="url" placeholder="Website likho... misal: google.com">
<br><button class="btn" type="submit">🌐 Website Kholo</button>
</form>
{% if show_img %}
<img src="/screen.png">
{% endif %}
<hr style="border:1px solid #1a2a5a;margin:30px 0">
<a class="btn" href="/graphics" style="background:#c9a227">🎨 Designer</a>
</body></html>
"""

GRAPHICS_PAGE = """
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Designer</title>
<style>
body{font-family:Arial;background:#0a0f24;color:#fff;text-align:center;padding:30px;margin:0}
h1{font-size:36px;color:#c9a227}
.btn{display:block;width:90%;max-width:400px;margin:15px auto;padding:25px;
font-size:26px;font-weight:bold;color:#04121f;background:#c9a227;
border:none;border-radius:15px;cursor:pointer}
textarea{width:90%;max-width:500px;padding:18px;font-size:20px;border-radius:12px;
border:2px solid #c9a227;background:#111832;color:#fff;margin:10px;height:100px}
.msg{font-size:22px;color:#7CFC00;margin:15px;min-height:30px}
img{max-width:95%;border-radius:10px;margin-top:15px;border:2px solid #c9a227}
.back{color:#10B3FE;font-size:20px;text-decoration:none}
.style-btn{display:inline-block;margin:8px;padding:12px 20px;font-size:18px;background:#1a2a5a;
color:#fff;border:2px solid #c9a227;border-radius:10px;cursor:pointer}
</style></head><body>
<h1>🎨 Designer</h1>
<div class="msg">{{msg}}</div>
<form action="/generate" method="post">
<textarea name="prompt" placeholder="Kya banana hai? Misal: Diwali sale poster for horse riding shop, dark green and gold"></textarea><br>
<div>
<button type="button" class="style-btn" onclick="setStyle('equestrian luxury, dark green and gold, premium')">🐴 Equestrian</button>
<button type="button" class="style-btn" onclick="setStyle('modern tech, blue and dark, futuristic')">💻 Tech</button>
<button type="button" class="style-btn" onclick="setStyle('festive, colorful, celebration')">🎉 Festive</button>
</div><br>
<button class="btn" type="submit">✨ Graphic Banao</button>
</form>
{% if img_url %}
<img src="{{img_url}}">
<br><a class="btn" href="{{img_url}}" download="graphic.png" style="background:#10B3FE">⬇️ Download Karo</a>
{% endif %}
<br><a class="back" href="/">← Wapis Bot par jao</a>
<script>
function setStyle(s){document.querySelector('textarea').value += ' '+s;}
</script>
</body></html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE, msg="", show_img=False)

@app.route("/shot")
def shot():
    try:
        from mss import mss
        with mss() as sct:
            sct.shot(output="screen.png")
        return render_template_string(PAGE, msg="✅ Screenshot le liya!", show_img=True)
    except Exception as e:
        return render_template_string(PAGE, msg=f"❌ Masla: {e}", show_img=False)

@app.route("/screen.png")
def screen():
    return send_file("screen.png", mimetype="image/png")

@app.route("/open", methods=["POST"])
def open_url():
    url = request.form.get("url", "").strip()
    if not url:
        return render_template_string(PAGE, msg="❌ Pehle website likho!", show_img=False)
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return render_template_string(PAGE, msg=f"✅ Khol diya: {url}", show_img=False)

@app.route("/graphics")
def graphics():
    return render_template_string(GRAPHICS_PAGE, msg="", img_url=None)


@app.route("/generate", methods=["POST"])
def generate():
    import urllib.parse
    prompt = request.form.get("prompt", "").strip()
    if not prompt:
        return render_template_string(GRAPHICS_PAGE, msg="❌ Pehle likho kya banana hai!", img_url=None)
    # Free AI image API - koi login nahi!
    full_prompt = f"professional marketing graphic, {prompt}, high quality, detailed"
    encoded = urllib.parse.quote(full_prompt)
    img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1080&nologo=true"
    return render_template_string(GRAPHICS_PAGE, msg="✅ Graphic ban gaya!", img_url=img_url)


if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Bot chal raha hai!")
    print("Browser mein kholo: http://localhost:5000")
    print("Band karne ke liye Ctrl+C dabao")
    print("=" * 50)
    # Browser khud khol do
    webbrowser.open("http://localhost:5000")
    app.run(port=5000)
