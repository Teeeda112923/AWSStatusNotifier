# 📡 AWS Status Notifier

AWSの障害発生を自動検知し、  
**メール・Slack** へ通知する軽量モニタリングツールです。  
障害がない場合も「正常確認通知」を定期送信できます。

---

## 🛠 機能一覧

- AWS公式ステータスRSSを1時間ごとにチェック
- 新たな障害が検出されれば即時通知
- 障害がない場合も正常通知を送信
- 通知先：メール（SMTP） / Slack（任意）
- GitHub Actions / ローカル実行どちらにも対応
- 通知済みエントリをJSONで管理し、重複防止

---

## 🚀 セットアップ方法

### 1. 必要なSecrets設定（GitHub Actions用）

| Name               | 内容                              |
|--------------------|-----------------------------------|
| SMTP_USER          | メール送信元アドレス（例: Gmail）   |
| SMTP_PASS          | SMTPアプリパスワード              |
| MAIL_TO            | メール送信先アドレス               |
| SLACK_WEBHOOK_URL  | Slack Incoming Webhook URL（任意） |

※ SMTP_USERとMAIL_TOは同じでもOKです。

※ SMTP_USERとSMTP_PASSは同じアカウントで行ってください。

 （おすすめはGmailです）

※ SMTP_PASSの生成はこちらから🔗(2段階認証の設定が必須です)

  https://myaccount.google.com/apppasswords

### 2. 実行スケジュール設定（cron）

`.github/workflows/aws-check.yml` を編集して実行間隔を変更できます。

schedule:
  - cron: '0 * * * *'  # 毎時0分に実行（UTC）

### 通知メッセージ

### ✅ 正常時

件名:
【AWS稼働確認】異常は検出されませんでした（2025/04/22 13:00 時点）

本文:
現在 2025/04/22 13:00 時点で、AWSステータスに新たな障害は報告されていません。
引き続き監視を継続します。

Slackやでは以下のように通知されます：
【AWS稼働確認】異常は検出されませんでした（2025/04/22 13:00 時点）
現在AWSステータスに新たな障害は報告されていません。

---

### 🚨 障害発生時

件名:
【AWS障害検知】[RESOLVED] Connectivity Issues – US-WEST-2 Region

本文:
[RESOLVED] Connectivity Issues – US-WEST-2 Region
Between 1:02 PM and 2:45 PM PDT, elevated error rates for EC2 and ELB were observed.
詳細: https://status.aws.amazon.com/

Slackやでは以下のように通知されます：
【AWS障害検知】[RESOLVED] Connectivity Issues – US-WEST-2 Region
Between 1:02 PM and 2:45 PM PDT, elevated error rates for EC2 and ELB were observed.
詳細: https://status.aws.amazon.com/

---

## 📋 必要パッケージ

feedparser
pytz
requests

※ pip install -r requirements.txt で自動インストールできます。

---

## 📄 ライセンス

本ツールは、企業・個人の利用はフリーで利用いただけますが、商用利用はNGです。
改変・拡張する場合は以下URLから一報ください。
（基本的にはNGを出しません。共有OKであれば本サイトで紹介します。）

URL：https://www.cybernote.click/contact/

（題名に「AWS Status Notifier改変・拡張の件」と記載して、メッセージ本文に改変内容を明記してください）

---

## 🤝 貢献・拡張歓迎！

- 正常通知を1日1回に間引くオプション
- Slack Block Kit対応
- Discord・Telegram通知対応
- AWS Health API対応（有料版拡張）
- GitHub Actionsのバッジ対応

Pull Request / Issue 大歓迎です！

---

## 🔥 特記事項

- メール通知（SMTP設定）は必須ですが、Slackとは任意設定です。
- Slackやの設定が未登録の場合は自動スキップされます。
- `.env.example` を参考に `.env` ファイルを作成してください。







