# mail2slack
Python Script wich scans a IMAP Inbox and post every Mail to a Slack Channel
Needs Python > 3.6

## Setup python: 

```shell
git clone https://github.com/corgan2222/mail2slack
cd mail2slack
cp mail2slack.conf.sample mail2slack.conf
nano mail2slack.conf 
pip3 install -r requirements.txt
python mail2slack.py
```

### run with PM3

just run 
```shell
pm2 start ecosystem.config.js 
```

# Or run with docker-compose: 

- create a folder
- download docker-compose.yml
- change the settings in the docker-compose.yml
- run

```shell
mkdir mail2slack
curl -o docker-compose.yml https://raw.githubusercontent.com/corgan2222/mail2slack/master/docker-compose.yml.sample
nano docker-compose.yml
docker-compose up -d
```

# Or run with docker-run: 

- dont forget to change the settings!

```shell
docker run -d --restart unless-stopped  --name mail2slack \
  -e SLACK_END_POINT="https://hooks.slack.com/services/xxxxxxxxxxxxxxxxxx" \
  -e SLACK_SLACK_SENDER="Mailparser" \
  -e SLACK_ICON_URL="https://raw.githubusercontent.com/corgan2222/mail2slack/master/docs/logo.png" \
  -e SLACK_SLACK_FALLBACK="FALLBACK_MESSAGE" \
  -e SLACK_CHANNEL="xxxx" \
  -e SLACK_TOKEN="xoxp-xxxxxxxx-xxxxxxxxxxx-xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxx" \
  -e MAIL_MAILSERVER="mail.server.com" \
  -e MAIL_MAIL_LOGIN="mail@server.com" \
  -e MAIL_MAIL_PW="xxxyyyyy" \
  -e MAIL_FOLDER="Inbox" \
  -e MAIL_AUTHOR_LINK="https://github.com/corgan2222/mail2slack" \
  -e MAIL_TITLE_LINK="https://github.com/corgan2222/mail2slack" \
  -e MAIL_FOOTER="xxx@yyyy.com" \
  -e MAIL_FOOTER_ICON="https://raw.githubusercontent.com/corgan2222/mail2slack/master/docs/logo.png" \
  -e GENERAL_LOG_LEVEL="INFO" \
  stefanknaak/mail2slack:latest
```

https://github.com/corgan2222/mail2slack/wiki
