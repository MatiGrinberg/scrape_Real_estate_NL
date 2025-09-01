import pandas as pd
import os
import re
import requests
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from urllib.parse import urljoin
from webdriver_manager.chrome import ChromeDriverManager

pd.set_option('display.max_colwidth', None)
csv_files=['funda.csv','rent_huurwoningen.csv']
BASE_URL_woningen_rent="https://www.huurwoningen.nl"
DUTCH_MONTHS = {"januari": 1, "februari": 2, "maart": 3, "april": 4,"mei": 5, "juni": 6, "juli": 7, "augustus": 8,"september": 9, "oktober": 10, "november": 11, "december": 12}
#Funda Links
r_funda=('https://www.funda.nl/zoeken/huur?price=%220-1500%22&object_type=[%22house%22,%22apartment%22]&floor_area=%2250-%22&bedrooms=%221-%22&construction_period=[%22from_1991_to_2000%22,%22from_2001_to_2010%22,%22from_2011_to_2020%22,%22after_2020%22]&sort=%22price_up%22&custom_area=wcv_%2540o%2560n_IyiKgqCouPtlBfsDnmIp%257Be%2540vgTxpNn_HePngCcwBj%257COdoQp%255ElnXuuRxtA%2560aQbhYolDxs%255EzuTjrKln%2540vec%2540%257DlDbwBgqFswg%2540%257Bf%255BfzGw%257DJgsDscIo%257Be%2540%257BpDkoF%257CSehNljFeo%255ChaDwdu%2540eaU,cmw%255Dw_s%257CHgk%255E%257BmB_mE%257BbQp%257Be%2540q%257CDj%257BM%257D~JtaBn~KwbSrhOja%2540bfI,%257D~zXsg%257B%257CHehNvuJ_~%255BfyIdeIujUhvI%257DqEtiVrlE,kniYian%257CHeuCueCexS~%257CNhvIo%257CGjrKtmCtcAogF,%257DksYcza%257CHeaVkxT%257Bh%255DtoM%2560bDvpLfzGtlIhnc%2540%257BNl%257DA%257BeO')
land=('https://www.funda.nl/zoeken/koop?price=%220-250000%22&object_type=[%22land%22]&sort=%22price_up%22&custom_area=wcv_%2540o%2560n_IyiKgqCouPtlBfsDnmI%2560aa%2540poYhkStwBePngCcwBj%257COdoQp%255ElnXuuRxtA%2560aQbhYolDxs%255EzuTjrKln%2540vec%2540%257DlDbwBgqFswg%2540%257Bf%255BfzGw%257DJgsDscIo%257Be%2540%257BpDkoF%257CSehNljFeo%255ChaDwdu%2540eaU,cmw%255Dw_s%257CHgk%255E%257BmBo%2560GstYtkUobCph%255BkxAtpYqIq%257Be%2540xcZja%2540bfI,%257D~zXsg%257B%257CHehNvuJufQokAgkSavPl%2560GynLtzl%2540r%257BT,kniYian%257CHeuCueC%257ByElv%2540_fB%2560hDjrKtmCtcAogF,%257DksYcza%257CHewBefKcyAewFkxTmjRk_Xba_%2540%2560bDvpLfzGtlIhnc%2540%257BNl%257DA%257BeO')
b_funda=('https://www.funda.nl/zoeken/koop?price=%220-325000%22&object_type=[%22house%22,%22apartment%22]&floor_area=%2250-%22&bedrooms=%221-%22&construction_period=[%22from_1991_to_2000%22,%22from_2001_to_2010%22,%22from_2011_to_2020%22,%22after_2020%22]&sort=%22price_up%22&custom_area=osu_%2540_xx~HzeMa%257DJvdu%2540tvLjdP%257BoF%2560eTwmIhvIxlBp_YjfD%257Di%2540tgB%2560iG%257C%257DIju%255BbwXdm%2560%2540d_%255DsrsEcn%257D%2540,ey%257B%255Dmnz%257CHo%257CSqqFezRa%257B_%2540~go%2540orBhrVn%257BEsb%255Erdd%2540,%257B%257CbYyv%2560%257DHxwQbzLsb%255E~eKewB%2560qKo%2560GnrGmq%255Dv%255E~eBwoRrb%255Eet_%2540hkSn%257DB,_~vZi%257Bo%257DHia%2540vbPinc%2540s%255EcPg~Yvae%2540bzI')
p_funda=('https://www.funda.nl/zoeken/koop?price=%220-325000%22&type=[%22group%22]&sort=%22price_up%22&custom_area=wcv_%2540o%2560n_IyiKgqCouPtlBfsDnmIp%257Be%2540vgTxpNn_HePngCcwBj%257COdoQp%255ElnXuuRxtA%2560aQbhYolDxs%255EzuTjrKln%2540vec%2540%257DlDbwBgqFswg%2540%257Bf%255BfzGw%257DJgsDscIo%257Be%2540%257BpDkoF%257CSehNljFeo%255ChaDwdu%2540eaU,cmw%255Dw_s%257CHgk%255E%257BmB_mE%257BbQdxSgtKph%255BkxAzwFroIwbSrhOja%2540bfI,%257D~zXsg%257B%257CHehNvuJufQokAcP%257DcHuxJ%257D%2560Utzl%2540r%257BT,kniYian%257CHeuCueC%257ByElv%2540_fB%2560hDjrKtmCtcAogF,%257DksYcza%257CHewBefKcyAewFwxm%2540tuK%2560bDvpLfzGtlIhnc%2540%257BNl%257DA%257BeO')


#####   Analyses    #####   #####   ###########################
def mean_by_location(df, col):
    df_gr = df.groupby('Location')[col].agg(['mean','count']).assign(mean=lambda x: x['mean'].round(1)).sort_values('mean')
    print(col,"\n",df_gr)
    return df_gr.index

def filter_by_string(d,c,tx):
    return d[d[c].str.contains(tx, na=False)]
    
def filter_per_loc(d,l,s):
    return d[d['Location']==l].sort_values(s)

def dupli_row(d,so):
    d[d.duplicated(keep=False)].sort_values(so)

def print_null_rows(df,col_pr,column):
    nu=df[df[column].isnull()]
    print(f'Num of Rows with Null_Values in {column}: {len(nu)}')
    return nu[col_pr].tolist()

def inspect_dataframe(df):
    print(f"Shape: {df.shape}\n")
    print("Column Data Types:")
    print(df.dtypes, "\n")
    print("Null Values per Column:")
    print(df.isnull().sum(), "\n")
    print("Rows with Null Values:")
    print(df[df.isnull().any(axis=1)])
    print("\n")
    print(f"Duplicate Rows sorted by 'Location':")
    print(df[df.duplicated(keep=False)].sort_values(by='Location', ascending=True))
    print("\n")
    print("Unique Values per Column (sorted):")
    for col in df.columns:
        unique_vals = sorted(df[col].dropna().unique())
        print(f"\n{col} ({len(unique_vals)} unique):\n {unique_vals}")
    print("\n")

def prepare_data(df,min_sz=47,max_pr=325,price_col='Price',size_col='Area',price_per_sqm_col='Price/SqM',hab_col='Bedrooms',rent=False,drop_dupl=None,drop_cols=None):
    df[hab_col] = df[hab_col].fillna(0)
    df[price_col] = (df[price_col].astype(float) / 1000).round(1)
    df[price_per_sqm_col] = (df[price_col] / df[size_col]).round(1)
    df['Price/room'] = (df[price_col] / df[hab_col]).round(1)
    df=df[(df[price_col] <= max_pr)& (df['Area'] >= min_sz) & (df[hab_col] < 10)]
    print(df.shape)
    if drop_dupl is not None:
        print(df.loc[df.duplicated(subset=drop_dupl, keep=False), drop_dupl].sort_values(by=drop_dupl))
        df = df.drop_duplicates(subset=drop_dupl)#.reset_index(drop=True)
        print(df.shape)
    if drop_cols:
        df = df.drop(columns=drop_cols, errors='ignore')
    return df

def print_by_group(d,col,s):
    gr=d.groupby(col,sort=False)
    groups_idxs={}
    for c, g in gr:
        print(f"\n\n--- {c} ---")
        print(g.sort_values(s).drop(col,axis=1))
        groups_idxs[c]=g.index.tolist()
    return groups_idxs
        
def filter_rent_rows(df, mx_pr_1h=1.2, mx_pr_room=0.8, min_area_1h=60,min_area_2h=75,min_area_3h=100,include=None,exclude=None,s="Price/room"):
    hab1 = (df['Bedrooms'] == 1) & (df['Price'] <= mx_pr_1h)& (df['Area'] >= min_area_1h)
    hab2 = (df['Bedrooms'] == 2) & (df['Price/room'] <= mx_pr_room) & (df['Area'] >= min_area_2h)
    hab3 = (df['Bedrooms'] >= 3) & (df['Price/room'] <= mx_pr_room) & (df['Area'] >= min_area_3h)
    res=pd.concat([df[hab1],df[hab2],df[hab3]])#.sort_values(s)
    if exclude:
        res = res[~res['Location'].isin(exclude)]
    if include:
        res = res[res['Location'].isin(include)]
    return res

def filter_buy_rows(df,min_h=2,min_price_sqm=1.5,max_price_sqm=3,min_area_any=55,min_area_large=100,min_hab_large=3,max_size=150,fr=1970,to=2036,excl=None,incl=None,s="Price/SqM"):
    base = (df['Price/SqM'] <= max_price_sqm)&(df['Price/SqM'] >= min_price_sqm) & (df['Area'] >= min_area_any)&(df['Bedrooms'] >= min_h)&(df['Area']<=max_size)#&(df['Y']>=fr)&(df['Y']<=to)
    large_area_rule = (df['Area'] < min_area_large) | ((df['Area'] >= min_area_large) & (df['Bedrooms'] >= min_hab_large))
    res=df[base&large_area_rule]#.sort_values(s)
    if excl:
        res=res[~res['Location'].isin(excl)]
    if incl:
        res = res[res['Location'].isin(incl)]
    return res

        
def plot_price_vs_size(df, title, price_col, size_col):
    plt.figure(figsize=(10, 6))
    plt.scatter(df[size_col], df[price_col], alpha=0.7, edgecolor='k')
    plt.title(title)
    plt.xlabel(size_col)
    plt.ylabel(price_col)
    plt.grid(True)
    plt.show()
    
def plot_histogram(df,t,c):
    plt.figure(figsize=(10, 6))
    sns.histplot(df[c], kde=True, bins=30)
    plt.title('Histogram '+t)
    plt.xlabel(c)
    plt.ylabel('Frequency')
    plt.show()

def plot_correlation_heatmap(df, cols, title):
    plt.figure(figsize=(8, 6))
    correlation_matrix = df[cols].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
    plt.title(title+' - Corr b/ Var', fontsize=16)
    plt.show()

def print_df_by_var(df,var,dfname):
    for v in var:
        print('\n'+dfname+"_"+v)
        print(sorted(df[v]))

def plot_boxplot(df, x_col, y_col, locations, group_num=None, char=10):
    df_filtered = df[df[x_col].isin(locations)]
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df_filtered, x=x_col, y=y_col)
    title = f'{y_col} by {x_col} (group {group_num})'
    plt.title(title)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    labels = [label.get_text()[:char] for label in plt.gca().get_xticklabels()]
    plt.gca().set_xticklabels(labels)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def boxplot_location_groups(df, y_col='Price/SqM', n_groups=4):
    locations = df['Location'].unique()
    group_size = len(locations) // n_groups
    location_groups = [locations[i*group_size:(i+1)*group_size] for i in range(n_groups)]
    if len(locations) % n_groups != 0:
        location_groups[-1] = np.append(location_groups[-1], locations[n_groups*group_size:])
    for i, group in enumerate(location_groups, 1):
        plot_boxplot(df, 'Location', y_col, group, group_num=i, char=10)
    plt.ioff()
    plt.show()


############################ Scraping ###########################
def scrape_huurwoningen_rent(cities, price=(200, 1500), radius=25, living_size=50, bedrooms=1, construction_year=(1990, 2025)):
    all_data = []
    for city in cities:
        count_per_city=0
        url = (f"{BASE_URL_woningen_rent}/en/in/{city}/"f"?price={price[0]}-{price[1]}&radius={radius}&living_size={living_size}"f"&bedrooms={bedrooms}&construction_year={construction_year[0]}-{construction_year[1]}"f"&sort=price&direction=asc")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        pagination = soup.select_one("ul.pagination__list")
        if pagination:
            li_items = pagination.find_all("li")
            num_pages = len(li_items) - 1  # subtract "next"
        else:
            num_pages = 1
        print(f"\nFound {num_pages} pages for {city}\n")
        for page in range(1, num_pages + 1):
            if page == 1:
                page_url = url
            else:
                page_url = (f"{BASE_URL_woningen_rent}/en/in/{city}/"f"?price={price[0]}-{price[1]}&radius={radius}&living_size={living_size}"f"&bedrooms={bedrooms}&construction_year={construction_year[0]}-{construction_year[1]}"f"&page={page}&sort=price&direction=asc")
            print(f"Scraping {city}, page {page}: {page_url}")
            response = requests.get(page_url)
            soup = BeautifulSoup(response.text, "html.parser")
            listings = soup.select("div.listing-search-item__content a.listing-search-item__link--title")
            links = [BASE_URL_woningen_rent + a["href"] for a in listings]
            for link in links:
                print(link)
                count_per_city+=1
                detail_resp = requests.get(link)
                detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
                location = detail_soup.select_one("h1.listing-detail-summary__title").get_text(strip=True).split(" in ")[-1]
                price_el = detail_soup.select_one("div.listing-detail-summary__price span.listing-detail-summary__price-main")
                price_val = int("".join(ch for ch in price_el.get_text(strip=True) if ch.isdigit())) if price_el else None
                area = int(detail_soup.select_one("dd.listing-features__description--surface_area span").get_text(strip=True).replace(" m²", ""))
                bedrooms_val = int(detail_soup.select_one("dd.listing-features__description--number_of_bedrooms span").get_text(strip=True))
                terrace = detail_soup.select_one("dd.listing-features__description--roof_terrace span").get_text(strip=True)
                all_data.append({"OriginalSearch":url,"SearchCity": city,"Location": location,"Link": link,"Price": price_val,"Area": area,"Bedrooms": bedrooms_val,"Terrace": terrace,})
        print(f'{city} Count {count_per_city}')
    df = pd.DataFrame(all_data)
    df.to_csv("rent_huurwoningen.csv", index=False)
    print("Printed to csv")
    return df


def parse_month_year(text):
    if not text or "nog niet bekend" in text.lower():
        return None
    parts = text.split()
    if len(parts) == 2:
        month_name, year = parts
        month_num = DUTCH_MONTHS.get(month_name.lower())
        if month_num:
            return f"{month_num:02d}-{str(year)[-2:]}"
    return None


def get_last_page_selenium(url, headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    last_page = 1
    try:
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='?page=']")))
            links = driver.find_elements(By.CSS_SELECTOR, "a[href^='?page=']")
        except TimeoutException:
            links = []
        numbers = []
        for link in links:
            inner = link.get_attribute("innerHTML").strip()
            if inner.isdigit():
                numbers.append(int(inner))
        if numbers:
            last_page = max(numbers)
    finally:
        driver.quit()
    return last_page

def flatten_projects(projects):
    rows = []
    for proj in projects:
        base = {k: v for k, v in proj.items() if k != "Types"}
        if not proj["Types"]:
            rows.append(base)
        else:
            for t in proj["Types"]:
                row = {**base, **t}
                rows.append(row)
    return pd.DataFrame(rows)

def scrape_property_built(soup, prop_type):
    data = {"Location": None, "Price": None, "Area": None, "Bedrooms": None, "Y": None, "Energy": None}
    loc_el = soup.select_one("h1[data-global-id] span.text-neutral-40")
    if loc_el:
        parts = loc_el.get_text(strip=True).split()
        if len(parts) > 2:
            data["Location"] = " ".join(parts[2:])
    price_el = soup.select_one("div.my-3.flex.flex-wrap div.flex-col.text-xl div, div.my-3 span")
    if price_el:
        raw_price = price_el.get_text(strip=True)
        nums = re.findall(r"\d+", raw_price.replace(".", "").replace(",", ""))
        data["Price"] = int("".join(nums)) if nums else None
    stats = soup.select("ul.flex.flex-wrap.gap-4 span.md\\:font-bold")
    if len(stats) == 0:
        return None
    if len(stats) >= 3:
        if len(stats) > 3:  
            area_el, beds_el, energy_el = stats[0], stats[2], stats[3]
        else:
            area_el, beds_el, energy_el = stats[0], stats[1], stats[2]
        data["Area"] = re.sub(r"\D", "", area_el.get_text())
        if prop_type in ["Buy", "Rent"]:
            data["Bedrooms"] = beds_el.get_text(strip=True)
            data["Energy"] = energy_el.get_text(strip=True)
    elif len(stats) <= 2:
        data["Area"] = re.sub(r"\D", "", stats[0].get_text())
        if prop_type in ["Buy", "Rent"]:
            data["Bedrooms"] = stats[1].get_text(strip=True)
    if prop_type in ["Buy", "Rent"]:
        by_el = soup.find("dt", string=re.compile("Bouwjaar"))
        if by_el and by_el.find_next("dd"):
            raw_year = by_el.find_next("dd").get_text(strip=True)
            match = re.search(r"\d{4}", raw_year)
            data["Y"] = int(match.group()) if match else None
    if prop_type == "Land":
        data["Bedrooms"] = None
        data["Energy"] = None
        data["Y"] = None
    return data

def scrape_project(soup):
    aantal = None
    aantal_el = soup.select_one("dl[data-testid='Aantal huizen'] dd")
    if aantal_el:
        raw = aantal_el.get_text(strip=True)
        m = re.search(r"\((\d+)", raw) 
        if m:
            aantal = int(m.group(1))
    location = None
    loc_el = soup.select_one("a[href*='/detail/nieuwbouw/'] p.text-xl.font-semibold")
    if loc_el:
        raw_loc = loc_el.get_text(strip=True)
        location = re.sub(r"\s*\([^)]*\)", "", raw_loc).strip()
    project_info = {"NumUnits": aantal,"Sale": None,"Build": None,"Delivery": None,"Location": location}
    for key, eng in [("Start verkoop", "Sale"),("Start bouw", "Build"),("Verwachte oplevering", "Delivery"),]:
        dl = soup.select_one(f"dl[data-testid='{key}']")
        if dl:
            dd = dl.find("dd")
            if dd:
                project_info[eng] = parse_month_year(dd.get_text(strip=True))
    rows = []
    lis = soup.select("ul.space-y-6 > li")
    for li in lis:
        entry = {"Name_Prop": None, "Price": None, "Area": None, "Units": None}
        span = li.select_one("button span")
        if span:
            nums = re.findall(r"\d+", span.get_text())
            if nums:
                entry["Units"] = int(nums[0])
        h3 = li.select_one("h3 button")
        if h3:
            entry["Name_Prop"] = h3.get_text(strip=True)
        p = li.select_one("p.mt-1.font-bold")
        if p:
            nums = re.findall(r"\d+", p.get_text().replace(".", "").replace(",", ""))
            if nums:
                entry["Price"] = max(map(int, nums))
        ul = li.select_one("ul li")
        if ul:
            nums = re.findall(r"\d+", ul.get_text())
            if nums:
                entry["Area"] = max(map(int, nums))
        rows.append({**project_info, **entry})
    return pd.DataFrame(rows)


def scrape_funda(urls,prop_typ=["Rent", "Land", "Buy", "Project"]):
    all_links = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    property_types = prop_typ
    url_type_map = dict(zip(urls, property_types))
    for base_url in urls:
        search_type = url_type_map[base_url]
        last_page = get_last_page_selenium(base_url, headless=False)
        print(f"\nSearch type: {search_type} | Num of Pages: {last_page} | {base_url}")
        for page in range(1, last_page + 1):
            if page == 1:
                page_url = base_url
            else:
                sep = "&" if "?" in base_url else "?"
                page_url = f"{base_url}{sep}search_result={page}"
            print(f"Fetching page {page}")
            resp = requests.get(page_url, headers=headers)
            soup = BeautifulSoup(resp.text, "html.parser")
            container = soup.find("div", {"class": "flex flex-col gap-3 mt-4"})
            if not container:
                continue
            for h2 in container.find_all("h2"):
                a = h2.find("a", href=True)
                if a and a["href"].startswith("/detail/"):
                    full_link = urljoin("https://www.funda.nl", a["href"])
                    print(full_link)
                    all_links.append({"page": page,"search_url": base_url,"property_url": full_link,"type": search_type})
    df = pd.DataFrame(all_links).drop_duplicates()
    details = []
    for _, row in df.iterrows():
        print(f"Scraping {row['property_url']} ({row['type']})")
        resp = requests.get(row["property_url"], headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        if row["type"] in ["Buy", "Rent", "Land"]:
            data = scrape_property_built(soup, prop_type=row["type"])
            if data:
                details.append({**row.to_dict(), **data})
        elif row["type"] == "Project":
            proj_df = scrape_project(soup)
            for _, proj_row in proj_df.iterrows():
                details.append({**row.to_dict(), **proj_row.to_dict()})
        else:
            details.append(row.to_dict())
    final_df = pd.DataFrame(details).reset_index(drop=True)
    final_df.to_csv("funda.csv", index=False)
    print("Printed to csv")
    return final_df






