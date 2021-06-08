# PS5 Hunter

Checks for stock of Sony Playstation 5 at a few retailers and sends an email when it's detected.

### Usage
Install the requirements (probably in a virtual env of some sort):
```
pip3 install -r requirements.txt
```

Run it!
```
python3 run.py
```

Then enter your email credentials to log in when prompted (sender must be Gmail).
```
Enter Email credentials:
Sender email: xxxx@gmail.com
Receiver email: yyyy@zzzz.com
Password: ******
```

Can optionally provide the below flags:
```
  -h, --help           show this help message and exit
  --headless           Run Chrome in headless mode so no browser window is opened.
```

It's recommended to run with `--headless` so Chrome doesn't keep opening and closing and taking focus.
