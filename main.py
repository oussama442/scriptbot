# main.py
import os
import datetime
import openai
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

content_plan = {
    "Monday": "تحدث عن مشكلة حقيقية يعاني منها العملاء عند عدم وجود موقع إلكتروني، واشرح كيف تساعدهم أنت.",
    "Tuesday": "اعطِ نصيحة بسيطة وعملية للبائعين أو أصحاب المشاريع حول كيفية تحسين مواقعهم (بصوت عربي).",
    "Wednesday": "اشرح مشهدًا مختصرًا من عملك أثناء بناء أو تصميم موقع (تخيل أنه فيديو تايم لابس).",
    "Thursday": "شارك شهادة حقيقية من عميل وما الذي استفاد منه من خدماتك.",
    "Friday": "اعرض عرضًا بصريًا (صور سريعة) لمواقع أو متاجر أنجزتها.",
    "Saturday": "وضح خطأ شائع يرتكبه العملاء عند بناء موقع، وقدم له حلاً ذكيًا ومقنعًا.",
    "Sunday": "شارك قصة شخصية عن سبب حبك لبناء مواقع إلكترونية وكيف بدأت في هذا المجال."
}

today = datetime.datetime.now().strftime("%A")
topic = content_plan.get(today, "شارك شيئًا ملهمًا عن المواقع الإلكترونية.")

def generate_script():
    prompt = f"""
    اكتب لي سكريبت فيديو قصير (60 ثانية كحد أقصى) باللهجة الجزائرية أو العربية البسيطة عن:
    "{topic}"

    ✨ يجب أن يحتوي على:
    - Hook في أول 3 ثواني لجذب الانتباه 🎯
    - محتوى مقنع وعملي ✍️
    - CTA قوي في النهاية (دعوة للعمل) 🔥
    - لا تكتب أي شيء زائد خارج السكريبت
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )

    return response.choices[0].message.content.strip()

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ تم الإرسال إلى تيليجرام.")
    else:
        print(f"❌ خطأ في الإرسال: {response.text}")

app = Flask(__name__)

@app.route("/run-script")
def run_script():
    script = generate_script()
    send_to_telegram(f"📅 موضوع اليوم ({today}):\n\n{script}")
    return jsonify({"status": "success", "script": script})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
