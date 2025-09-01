# scrape_Real_estate_NL 🏠 
Scrape Rent/Buy(newProjects/ExistingBuildings/Land) listings in NL (Ams/Lei/Utr/Hag/Rot) to then make analyses based on price and other characteristics.
It collects housing listings, cleans the datasets, and provides tools for filtering, analyzing, and visualizing market trends such as **price per square meter**, **price per room**, and **location-based comparisons**.  

---

## 🚀 Features  
- Scrape property listings for **Rent**, **Buy**, **Land**, and **Project** properties.  
- Merge and clean data from different platforms.  
- Remove duplicates and handle missing values.  
- Custom filtering for **rent affordability** and **buying criteria** (price per sqm, min/max size, etc.).  
- Statistical summaries (`describe`, group means, null inspection).  
- Visualization tools:
  - Price vs. Size scatter plots  
  - Histograms of key variables  
  - Boxplots by location or bedrooms  
  - Correlation heatmaps  

---

## 📦 Dependencies  
All functions are imported from the local `Dependencies` module, which provides the following key utilities:  

- **Scraping**
  - `scrape_huurwoningen_rent` 
  - `scrape_funda`
  - Scraped data is saved in funda.csv and rent_huurwoningen.csv

- **Data Cleaning**
  - `inspect_dataframe(df)`
  - `print_null_rows(df, *cols)`
  - `prepare_data(df, rent, drop_cols)`  

- **Filtering**
  - `filter_rent_rows(...)`
  - `filter_buy_rows(...)`
  - `filter_per_loc(df, location, col)`
  - `filter_by_string(df, col, string)`  

- **Analysis**
  - `mean_by_location(df, col)`
  - `print_by_group(df, group_col, y_col)`  

- **Visualization**
  - `boxplot_location_groups(df, y_col)`
  - `plot_price_vs_size(df, title, x_col, y_col)`
  - `plot_histogram(df, title, col)`
  - `plot_correlation_heatmap(df, cols, title)`  

---
