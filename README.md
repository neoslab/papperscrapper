# Papindex

![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

This Python script is a powerful, automated web scraper tailored for extracting detailed company profiles from Pappers.fr. It focuses on French companies that meet specific business criteria and are located within specified postal codes. Designed for structured financial analysis, lead generation, or compliance research, the script utilizes Selenium with BeautifulSoup, allowing it to navigate dynamic web pages and extract high-value data into a structured CSV format.

* * *

## Server Setup

### Update/upgrade machine

```bash
sudo apt -y update && sudo apt -y upgrade && sudo apt -y dist-upgrade
sudo apt -y remove && sudo apt -y autoremove
sudo apt -y clean && sudo apt -y autoclean
```

### Install Python Packages

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

### Clone Project Repository

```bash
cd $HOME
git clone https://github.com/neoslab/papindex
cd $HOME/papindex
python3 -m venv papindex
source papindex/bin/activate
python -m pip install -r requirements.txt
```

### Launch the scrapper

```bash
nohup python handler.py > output-handler.log 2>&1 &
```

* * *

### Windows PyCharm Setup

**Upgrade PIP if needed**

```bash
C:\<DIRECTORY\FULLPATH>\papindex\.venv\Scripts\python.exe -m pip install --upgrade pip
```

**Install requirements**

```bash
C:\<DIRECTORY\FULLPATH>\papindex\.venv\Scripts\python.exe -m pip install -r C:\<DIRECTORY\FULLPATH>\papindex\requirements.txt
```

* * *

## ChromeDriver

### Grab the correct version of ChromeDriver

Once downloaded, place the `chromedriver` file in the root directory of the project.

```bash
https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json
```

* * *

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit them (`git commit -m "Add your feature"`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a pull request with a clear description of your changes.

Ensure your code follows PEP 8 style guidelines and includes appropriate tests.

* * *

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

* * *

## Contact

For issues, suggestions, or questions, please open an issue on GitHub or contact the maintainer at [GitHub Issues](https://github.com/neoslab/papindex/issues).