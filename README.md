# mail2slack
Python Script wich scans a IMAP Inbox and post every Mail to a Slack Channel
Need Python > 3.6

Setup: 

```shell
git clone https://github.com/corgan2222/mail2slack
cd mail2slack
cp mail2slack.conf.sample mail2slack.conf
//edit mail2slack.conf and put your data in
pip3 install -r requirements.txt
python3.6 mail2slack.py
```

prepared for PM3

just run 
```shell
pm2 start ecosystem.config.js 
```

https://github.com/corgan2222/mail2slack/wiki
