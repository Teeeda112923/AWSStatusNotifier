# AWS Status Notifier

AWSの障害発生を自動検知し、メール・Slack・LINE に通知する軽量モニタリングツールです。  
障害がない場合も「正常です」の定期通知を送るため、常時監視状態を可視化できます。

---

## 機能概要

- AWS公式ステータスRSS（全リージョン）を1時間ごとにチェック
- 新たな障害が見つかれば即座に通知
- 障害がない場合でも「正常通知」を送信（オプションで間引きも可能）
- 通知先：メール（SMTP） / Slack / LINE Notify に対応
- GitHub Actions でもローカル実行でもOK
- 通知済みエントリは `.json` に記録して重複防止

---

## GitHub Actions で使う場合

### 1. 必要な Secrets を設定

| Name               | 内容                                 |
|--------------------|--------------------------------------|
| SMTP_USER          | メール送信元アドレス（Gmail等）        |
| SMTP_PASS          | SMTPパスワード（アプリパスワード推奨） |
| MAIL_TO            | メール送信先アドレス                  |
| SLACK_WEBHOOK_URL  | SlackのWebhook URL（任意）            |
| LINE_NOTIFY_TOKEN  | LINE Notify トークン（任意）          |

### 2. 実行タイミングの変更（必要なら）

`.github/workflows/aws-check.yml` の `cron` を編集：

```yaml
schedule:
  - cron: '0 * * * *'  # 毎時0分に実行（UTC）

---

### 3.ローカルで使う場合

git clone https://github.com/yourname/aws-status-notifier.git
cd aws-status-notifier
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 自分用の環境変数設定
python aws_status_checker.py

---

### 4.通知文例

#### ✅ 正常稼働通知（障害が検出されなかった場合）

"件名: 【AWS稼働確認】異常は検出されませんでした（2025/04/22 13:00 時点）"

"本文:
現在 2025/04/22 13:00 時点で、
AWSステータスに新たな障害は報告されていません。

引き続き監視を継続します。"

※ Slack／LINE でも同内容が通知されます。

---



#### 🚨 障害検知時の通知メッセージ
"件名: 【AWS障害検知】[RESOLVED] Connectivity Issues – US-WEST-2 Region"

"本文:
[RESOLVED] Connectivity Issues – US-WEST-2 Region

Between 1:02 PM and 2:45 PM PDT, we experienced elevated error rates for EC2 and ELB in the US-WEST-2 Region.

詳細: https://status.aws.amazon.com/"

※ Slack／LINE でも同内容が通知されます。


---


### .env の設定例（ローカル用）

SMTP_USER=your_gmail@gmail.com
SMTP_PASS=your_app_password
MAIL_TO=destination@example.com

SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/yyy/zzz
LINE_NOTIFY_TOKEN=your_line_notify_token


---


## 必要パッケージ

feedparser
pytz
requests

---



## LICENSE
基本的には自由に利用可能です。個人・企業で利用ください。
改変される場合は、以下問い合わせフォームから一報ください。
（あくまでも連絡ほしいだけなので、改変および拡張は基本OKです。よろしければ当方運営サイトで紹介します。）

URL：https://www.cybernote.click/contact/ 
題名に「AWSStatusNotifier改変の件」と記載してください。

---



## 貢献・拡張歓迎！
- 正常通知を1日1回に間引く機能
- Slack の Block Kit 対応
- Discord, Telegram 連携
- AWS Health API（有料API）対応
- ブラウザプッシュ通知対応（Pushover など）

Pull Request / Issue 大歓迎です！


