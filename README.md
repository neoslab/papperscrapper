# Server Setup

## Update/upgrade machine

```bash
sudo apt -y update && sudo apt -y upgrade && sudo apt -y dist-upgrade
sudo apt -y remove && sudo apt -y autoremove
sudo apt -y clean && sudo apt -y autoclean
```

## Install Python Packages

```bash
sudo apt install -y python3 python3-bs4 python3-cryptography python3-dateutil \
python3-dev python3-django python3-flask python3-ipython python3-jinja2 python3-lxml \
python3-matplotlib python3-numpy python3-pandas python3-pip python3-pyqt5 \
python3-requests python3-scipy python3-setuptools python3-sklearn python3-venv
sudo ln -s /usr/bin/python3 /usr/local/bin/python
sudo ln -s /usr/bin/pip3 /usr/local/bin/pip
python --version
pip --version
```

## Clone Project Repository

```bash
cd $HOME
git clone https://github.com/neoslab/papindex
cd $HOME/papindex
python3 -m venv papindex
source papindex/bin/activate
python -m pip install -r requirements.txt
```

## Launch the scrapper

```bash
nohup python handler.py > output-handler.log 2>&1 &
```

* * *

## Windows PyCharm Setup

# Upgrade PIP if needed

```bash
C:\<DIRECTORY\FULLPATH>\papdex\.venv\Scripts\python.exe -m pip install --upgrade pip
```

# Install requirements

```bash
C:\<DIRECTORY\FULLPATH>\papdex\.venv\Scripts\python.exe -m pip install -r C:\<DIRECTORY\FULLPATH>\papdex\.venv\requirements.txt
```

* * *

# ChromeDriver

## Grab the correct version of ChromeDriver

Once downloaded, place the `chromedriver` file in the root directory of the project.

```bash
https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json
```

## License

This script is open source under the [MIT License](LICENSE).