# === Import libraries ===
import json
import os
import csv
import time
import random
import re

# === Import packages ===
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# === Define 'postalcodes' ===
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
postalcodes = config.get("postalcodes", [])

# === Define 'linksfile' ===
linksfile = "linksfile.txt"

# === Define 'csvfile' ===
csvfile = "companies.csv"

# === Define 'baselink' ===
baselink = "https://www.pappers.fr"

# === Define 'getlinks' ===
getlinks = []

# === Define 'basefields' ===
basefields = [
    "URL", "Name", "Alias", "SIREN", "Status", "Address", "Activity",
    "Effectif", "Creation Date", "Dirigeant Name", "Dirigeant Age",
    "SIRET", "Legal Form", "VAT", "Capital", "RCS", "APE", "Domain",
    "Closure Date", "RCS Update", "RNE Update", "INSEE Update"
]

# === Clean-up ===
if os.path.exists(linksfile):
    os.remove(linksfile)
if os.path.exists(csvfile):
    os.remove(csvfile)

# === Setup Selenium ===
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/122.0.0.0 Safari/537.36")

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)


# === Function 'convertnbr' ===
def convertnbr(valsize):
    """
    This function standardizes and converts shorthand numerical strings representing monetary or quantity values
    into full integer string representations. It handles common suffixes such as 'K', 'M', and 'B', which stand for
    thousand, million, and billion respectively. This function is particularly useful for normalizing data extracted
    from user inputs, financial documents, or scraped websites where such formats are often used.

    Parameters:
    - valsize (str): A string representing a numeric value, potentially with a 'K', 'M', or 'B' suffix and including
      symbols such as spaces, commas, or the euro sign (€).

    Returns:
    - str: A string representation of the integer after conversion. If the input cannot be parsed or converted,
      it returns the cleaned original string without suffix interpretation.
    """
    valsize = valsize.replace(" ", "").replace("€", "").replace(",", ".")
    multiplier = 1
    if valsize.endswith("K"):
        multiplier = 1_000
        valsize = valsize[:-1]
    elif valsize.endswith("M"):
        multiplier = 1_000_000
        valsize = valsize[:-1]
    elif valsize.endswith("B"):
        multiplier = 1_000_000_000
        valsize = valsize[:-1]
    try:
        return str(int(float(valsize) * multiplier))
    except (ValueError, TypeError):
        return valsize


# === Function 'formatheader' ===
def formatheader(col):
    """
    This function is responsible for converting French-language financial column headers into their English-language
    equivalents. It supports an optional suffix pattern for years (e.g., "_2023") and appends the year to the translated
    header where applicable. It is commonly used in data transformation pipelines for rendering financial reports,
    dashboards, or CSV exports in a more internationally readable format.

    Parameters:
    - col (str): A string representing the original French column name, optionally suffixed with a 4-digit year (e.g., "Chiffre d'affaires (€)_2022").

    Returns:
    - str: A translated English version of the column name, optionally appended with the year if it was present in the original.
           If no translation is found or the input does not match expected patterns, the original string is returned unchanged.
    """
    translations = {
        "Autonomie financière (%)": "Financial Autonomy (%)",
        "BFR (j de CA)": "Working Capital Requirement (Days of Revenue)",
        "BFR (€)": "Working Capital Requirement (€)",
        "BFR exploitation (j de CA)": "Operating WCR (Days of Revenue)",
        "BFR exploitation (€)": "Operating WCR (€)",
        "BFR hors exploitation (j de CA)": "Non-Operating WCR (Days of Revenue)",
        "BFR hors exploitation (€)": "Non-Operating WCR (€)",
        "Capacité d'autofinancement (€)": "Self-Financing Capacity (€)",
        "Capacité d'autofinancement / CA (%)": "Self-Financing / Revenue (%)",
        "Capacité de remboursement": "Repayment Capacity",
        "Chiffre d'affaires (€)": "Revenue (€)",
        "Chiffre d'affaires à l'export (€)": "Export Revenue (€)",
        "Couverture des dettes": "Debt Coverage",
        "Couverture du BFR": "WCR Coverage",
        "Dettes financières (€)": "Financial Debt (€)",
        "Délai de paiement clients (j)": "Customer Payment Delay (Days)",
        "Délai de paiement fournisseurs (j)": "Supplier Payment Delay (Days)",
        "EBITDA - EBE (€)": "EBITDA (€)",
        "Fonds de roulement net global (€)": "Net Working Capital (€)",
        "Fonds propres (€)": "Equity (€)",
        "Impôts et taxes (€)": "Taxes (€)",
        "Liquidité générale": "General Liquidity",
        "Marge brute (€)": "Gross Margin (€)",
        "Marge nette (%)": "Net Margin (%)",
        "Ratio d'endettement (Gearing)": "Gearing Ratio",
        "Ratio des stocks / CA (j)": "Inventory / Revenue Ratio (Days)",
        "Rentabilité sur fonds propres (%)": "Return on Equity (%)",
        "Rentabilité économique (%)": "Return on Assets (%)",
        "Résultat d'exploitation (€)": "Operating Income (€)",
        "Résultat net (€)": "Net Income (€)",
        "Salaires / CA (%)": "Wages / Revenue (%)",
        "Salaires et charges sociales (€)": "Wages and Social Charges (€)",
        "Taux de croissance du CA (%)": "Revenue Growth Rate (%)",
        "Taux de levier (DFN/EBITDA)": "Leverage Ratio (Net Debt/EBITDA)",
        "Taux de marge brute (%)": "Gross Margin (%)",
        "Taux de marge d'EBITDA (%)": "EBITDA Margin (%)",
        "Taux de marge opérationnelle (%)": "Operating Margin (%)",
        "Trésorerie (€)": "Cash (€)",
        "Valeur ajoutée (€)": "Value Added (€)",
        "Valeur ajoutée / CA (%)": "Value Added / Revenue (%)",
        "État des dettes à 1 an au plus (€)": "Short-Term Debt (€)"
    }

    matchcol = re.match(r"^(.*)_([0-9]{4})$", col)
    if matchcol:
        group = matchcol.group(1).strip()
        period = matchcol.group(2)
        trans = translations.get(group, group).strip()
        return f"{trans} - {period}"
    return col


# === Loop callback ===
for postalcode in postalcodes:
    print(f"\nSearching in postal code: {postalcode}")
    baseurl = "https://www.pappers.fr/recherche"
    params = (
        f"?en_activite=true&&resultat_min=100000&resultat_max=10000000"
        f"&effectifs_min=3&effectifs_max=250"
        f"&age_dirigeant_min=50&age_dirigeant_max=100"
        f"&ville={postalcode}"
    )

    driver.get(baseurl + params)
    time.sleep(1)

    pagenbr = 1
    maxpage = 20
    while pagenbr <= maxpage:
        print(f"[{postalcode}] PAGE {pagenbr}")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        pagelinks = [baselink + a["href"] for a in soup.find_all("a", href=True)
                      if a["href"].startswith("/entreprise/")]

        getlinks.extend(pagelinks)
        try:
            nextbtn = driver.find_element(By.CLASS_NAME, "pagination-image-right")
            time.sleep(random.uniform(1, 2))
            nextbtn.click()
            time.sleep(1)
            pagenbr += 1
        except NoSuchElementException:
            break

# === Save links ===
uniqlinks = sorted(set(getlinks))
with open(linksfile, "w", encoding="utf-8") as f:
    for link in uniqlinks:
        f.write(link + "\n")

# === Process links ===
allrows = []
print("\r")
for idx, url in enumerate(uniqlinks, 1):
    print(f"[{idx}/{len(uniqlinks)}] Scraping: {url}")
    data = {field: "" for field in basefields}
    data["URL"] = url

    try:
        driver.get(url)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        h1 = soup.select_one("h1.big-text")
        if h1:
            parts = h1.get_text(strip=True).split("(")
            data["Name"] = parts[0].strip()
            if len(parts) > 1:
                data["Alias"] = parts[1].replace(")", "").strip()

        data["SIREN"] = soup.select_one("a.siren-to-copy").text.strip() if soup.select_one("a.siren-to-copy") else ""
        data["Status"] = "Active" if soup.select_one(".status .actif") else "Inactive"

        if data["Status"] != "Active":
            continue

        table = soup.select_one("#resume table")
        if table:
            for row in table.select("tr"):
                key = row.select_one("th").get_text(strip=True)
                value = row.select_one("td").get_text(strip=True)
                if key == "Adresse :":
                    data["Address"] = value
                elif key == "Activité :":
                    data["Activity"] = value
                elif key == "Effectif :":
                    match = re.search(r"(\d+)\s*et\s*(\d+)", value)
                    if match:
                        data["Effectif"] = f"{match.group(1)}-{match.group(2)}"
                elif key == "Création :":
                    data["Creation Date"] = value

        ownership = soup.select_one("#dirigeants .dirigeant")
        if ownership:
            nametag = ownership.select_one(".nom a")
            if nametag:
                nametext = nametag.get_text(strip=True)
                nametext = re.sub(r"\s*\(.*?\)", "", nametext)
                data["Dirigeant Name"] = nametext if nametext else "ND"
            else:
                data["Dirigeant Name"] = "ND"

            agetag = ownership.select_one(".age-siren span")
            if agetag:
                agetext = agetag.get_text(strip=True)
                match = re.match(r"^(\d+)\s+ans", agetext)
                if match:
                    data["Dirigeant Age"] = match.group(1)
                else:
                    data["Dirigeant Age"] = "ND"
            else:
                data["Dirigeant Age"] = "ND"
        else:
            data["Dirigeant Name"] = "ND"
            data["Dirigeant Age"] = "ND"

        legal = soup.select_one("#informations table")
        if legal:
            for row in legal.select("tr"):
                key = row.select_one("th").get_text(strip=True)
                value = row.select_one("td").get_text(strip=True)
                if "SIRET" in key:
                    data["SIRET"] = value
                elif "Forme juridique" in key:
                    data["Legal Form"] = value.split(",")[0].strip()
                elif "TVA" in key:
                    match = re.search(r"(FR\d+)", value)
                    if match:
                        data["VAT"] = match.group(1)
                elif "Capital social" in key:
                    data["Capital"] = value
                elif "Numéro RCS" in key:
                    match = re.search(r"(\d{3} ?\d{3} ?\d{3})", value)
                    if match:
                        data["RCS"] = match.group(1).replace(" ", "")

        activity = soup.select_one("#activite table")
        if activity:
            for row in activity.select("tr"):
                key = row.select_one("th").get_text(strip=True)
                value = row.select_one("td").get_text(strip=True)
                if "Code NAF" in key:
                    match = re.search(r"([\d\\.A-Z]+)", value)
                    if match:
                        data["APE"] = match.group(1).replace(".", "")
                elif "Domaine" in key:
                    data["Domain"] = value
                elif "clôture" in key:
                    data["Closure Date"] = value

        for span in soup.select(".date-maj span"):
            txt = span.get_text(strip=True)
            datematch = re.search(r"(\d{2}/\d{2}/\d{4})", txt)
            clean_date = datematch.group(1) if datematch else ""
            if "RCS" in txt:
                data["RCS Update"] = clean_date
            elif "RNE" in txt:
                data["RNE Update"] = clean_date
            elif "INSEE" in txt:
                data["INSEE Update"] = clean_date

        ecotable = soup.select_one("#finances .ratios table")
        if ecotable:
            headers = ecotable.select("tr.tr-header th")[1:]
            target_years = ["2023", "2022", "2021", "2020"]
            available_years = [th.get_text(strip=True) for th in headers]
            years = [y for y in target_years if y in available_years]
            ecodata = {year: {} for year in years}

            rows = ecotable.select("tr:not(.tr-header)")
            for row in rows:
                cols = row.select("th, td")
                if not cols or len(cols) < 2:
                    continue
                label = cols[0].get_text(strip=True)
                for i, year in enumerate(years):
                    if i + 1 >= len(cols):
                        continue
                    val = cols[i + 1].get_text(strip=True).replace("\xa0", " ")
                    val = convertnbr(val)
                    ecodata[year][label] = val if val else "ND"

            for year in target_years:
                if year in ecodata:
                    for label, value in ecodata[year].items():
                        colname = f"{label}_{year}"
                        data[colname] = value

        allrows.append(data)

    except Exception as e:
        print(f"[ERROR] {url}: {e}")
        allrows.append(data)
    time.sleep(random.uniform(1, 2))

driver.quit()

# === Reorder columns ===
finalheader = [col for col in basefields]
seen = set(finalheader)
year_order = ["2023", "2022", "2021", "2020"]
year_columns_by_year = {y: [] for y in year_order}

for row in allrows:
    for key in row:
        if key not in seen:
            matched = False
            for y in year_order:
                if key.endswith(f"_{y}"):
                    year_columns_by_year[y].append(key)
                    matched = True
                    break
            if not matched:
                finalheader.append(key)
            seen.add(key)

for y in year_order:
    finalheader.extend(sorted(set(year_columns_by_year[y]), key=lambda x: x.lower()))

# === Write to CSV ===
formatted_header = [formatheader(col) for col in finalheader]
with open(csvfile, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=finalheader)
    writer.writerow(dict(zip(finalheader, formatted_header)))
    for row in allrows:
        writer.writerow(row)

print(f"\nDone - Links saved into '{linksfile}' > Data saved into '{csvfile}'")