# TCPをフィルタリングするだけ．パフォーマンスは察しのとおり．
netfilterくんがSRHでカプセル化した中身のパケットを見てくれないので，scapyでフィルタリングする．
実験用に使用．


## Install.
sudoで実行するので，インストールもsudo.
```
sudo apt install -y libnetfilter-queue-dev
sudo pip3 install -r requirements.txt
```


## Run.

```
sudo python3 filter.py
```
