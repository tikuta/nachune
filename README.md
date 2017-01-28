# nachune

## これはなに
nasne で重複した番組を chinachu で録画するツール

普通は素直に nasne を買い増すのがよいと思われます．

## Installation and Usage
* python >= 3.6

0. `pip3 install -r requirements.txt`
0. `cp nachune.ini.sample nachune.ini` and edit `nachune.ini`
0. `crontab -e`

## ダメそうなところ
* 複数台 nasne での動作
* BS/CS を chinachu で録画する際の動作
* 予約が 3 件以上重なった際の動作
