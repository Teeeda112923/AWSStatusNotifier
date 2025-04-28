import feedparser
import os
import smtplib
import requests
import json
from email.message import EmailMessage
from datetime import datetime, timedelta
import pytz

# === 設定 ===
RSS_URL = "https://status.aws.amazon.com/rss/all.rss"
STATE_FILE = "aws_status_posted.json"
JST = pytz.timezone("Asia/Tokyo")

# === 環境変数 ===
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
MAIL_TO   = os.getenv("MAIL_TO")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

# === メール通知 ===
def send_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = MAIL_TO
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

# === Slack通知 ===
def send_slack(message):
    if not SLACK_WEBHOOK_URL:
        return
    payload = {"text": message}
    res = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if res.status_code != 200:
        raise Exception(f"Slack通知失敗: {res.status_code} {res.text}")

# === LINE Notify通知 ===
def send_line_notify(message):
    if not LINE_NOTIFY_TOKEN:
        return
    headers = {
        "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"
    }
    data = {
        "message": message
    }
    res = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)
    if res.status_code != 200:
        raise Exception(f"LINE通知失敗: {res.status_code} {res.text}")

# === 共通通知関数 ===
def notify(subject, body):
    print(f"📣 通知開始: {subject}")
    try:
        if SMTP_USER and SMTP_PASS and MAIL_TO:
            send_email(subject, body)
            print("✅ メール送信成功")
    except Exception as e:
        print(f"❌ メール通知エラー: {e}")

    try:
        if SLACK_WEBHOOK_URL:
            send_slack(f"{subject}\n{body}")
            print("✅ Slack送信成功")
    except Exception as e:
        print(f"❌ Slack通知エラー: {e}")

    try:
        if LINE_NOTIFY_TOKEN:
            send_line_notify(f"{subject}\n{body}")
            print("✅ LINE送信成功")
    except Exception as e:
        print(f"❌ LINE通知エラー: {e}")

# === 通知済みID管理 ===
def get_notified_ids():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f).get("notified_ids", [])
    return []

def add_notified_id(entry_id):
    ids = get_notified_ids()
    if entry_id not in ids:
        ids.append(entry_id)
        with open(STATE_FILE, "w") as f:
            json.dump({"notified_ids": ids}, f, indent=2)

# === メイン処理 ===
def main():
    print("🚨 AWS障害チェック開始")
    feed = feedparser.parse(RSS_URL)
    notified_ids = get_notified_ids()
    now = datetime.now(JST)

    found = False

    for entry in feed.entries:
        published = datetime(*entry.published_parsed[:6], tzinfo=pytz.utc).astimezone(JST)

        if (now - published) < timedelta(hours=1) and entry.id not in notified_ids:
            subject = f"【AWS障害検知】{entry.title}"
            body = f"{entry.title}\n\n{entry.summary}\n\n詳細: {entry.link}"
            notify(subject, body)
            add_notified_id(entry.id)
            found = True
            break

    if not found:
        subject = f"【AWS稼働確認】異常は検出されませんでした（{now.strftime('%Y/%m/%d %H:%M')} 時点）"
        body = (
            f"現在 {now.strftime('%Y/%m/%d %H:%M')} 時点で、"
            "AWSステータスに新たな障害は報告されていません。"
        )
        notify(subject, body)

if __name__ == "__main__":
    main()
