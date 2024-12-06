# DonarHouseBot
Donar House uchun buyurtmalar telegram boti


- `cd tgbot`

- `python -m aiogram_i18n multiple-extract -i "." -o ".\\locales\\" -cm -ek startup -k "i18n" -k "L" -k "I18NFormat" --locales "en"  --locales "uz" --locales "ru" `


# Deploy Bot
- `nano /etc/systemd/system/donarbot.service`

```shell
[Unit]
Description=Donar House Bot Description

[Service]
Type=simple
ExecStart=/var/www/DonarHouseBot/venv/bin/python  /var/www/DonarHouseBot/manage.py runbot

[Install]
WantedBy=multi-user.target
```

service ni yozib bo'lgandan so'ng uni ishga tushirib qo'yamiz:

`sudo systemctl daemon-reload`

`sudo systemctl enable donarbot.service`

`sudo systemctl start donarbot.service`

`sudo systemctl status donarbot.service`

# get backup from sqlite
`sqlite3 db.sqlite3 .dump > backup.sql`

# restore backup file
`psql -U db_user db_name < backup.sql`



#

### Django'da loaddata buyrug'i orqali fixturalarni bazaga yuklash mumkin.
`python manage.py loaddata initial_data.json`


### Agar mavjud ma'lumotlar asosida fixtura yaratmoqchi bo'lsangiz, dumpdata buyrug'idan foydalaning:
`python manage.py dumpdata tgbot.About tgbot.Branch --indent 4 > tgbot/fixtures/initial_data.json`
