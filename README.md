Hasten Subs
========================

Hasten or Delay your subtitle files

Installation
-----
```sh
$ pip install -r requirements.txt
```

Usage
-----
```sh
$ python hasten_subs/main.py --src "path to file/path to dir" --hasten "time"
```

Example usage
-----
The following command(s) will hasten your subtitle file(s) by 10 seconds
```sh
$ python hasten_subs/main.py --src "C:\01.srt" --hasten "-00:10"
$ python hasten_subs/main.py --src "C:\subs" --hasten "-00:10"
```