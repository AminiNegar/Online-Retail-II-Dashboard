# 📊 Online Retail Analytics & Executive Dashboard System

This project implements a comprehensive, end-to-end data pipeline designed to analyze online retail transaction data. The pipeline handles everything from raw data preprocessing and cleaning using Pandas, to structured storage and relational querying in an SQLite database, and finally, deploying an interactive web-based executive dashboard.

---

## 🚀 Key Features

* **Data Cleaning & Preprocessing:** Automated detection and handling of missing values, removal of duplicate transaction logs, and statistical outlier filtering using the Interquartile Range (IQR) method.
* **ETL Pipeline:** Seamless transition of processed structured data from memory (Pandas DataFrames) directly into an SQLite relational database (`.db`).
* **Advanced SQL Analytics:** Deep dive metrics using SQL `GROUP BY` and aggregate functions (`SUM`, `COUNT`, `AVG`) to extract business insights like Top-N products, loyal customers, and peak traffic hours.
* **In-Notebook Interactive Dashboard:** A fully responsive executive dashboard embedded directly within the Jupyter Notebook (`.ipynb`) environment using the Panel framework and interactive Plotly visualization components.

---

## 📂 Dataset Schema

The pipeline is optimized for standard E-commerce/Online Retail transactional datasets with the following fields:
* `Invoice`: Unique 6-digit identifier for each transaction.
* `StockCode`: Unique product/item identifier.
* `Description`: Product name/nominal specification.
* `Quantity`: Total units ordered per transaction line.
* `InvoiceDate`: Exact timestamp of the transaction.
* `Price`: Unit price of the product.
* `Customer ID`: Unique identifier assigned to each individual customer.
* `Country`: The region/country where the order was placed.
* `amount`: *Calculated Field* — Representing total line revenue ($Quantity \times Price$).

---

## 🛠 Tech Stack & Dependencies

* **Language:** Python 3.12
* **Data Manipulation:** Pandas, NumPy
* **Database Engine:** SQLite / SQLite3
* **Visualizations:** Plotly Express
* **Dashboard Framework:** Panel (optimized for inline Jupyter environments)
* **File I/O Engine:** Openpyxl (Excel compatibility)

---

## 💻 How to Run the Project

### 1. Installation
Install the required packages using pip:
```bash
pip install pandas numpy plotly panel openpyxl
```
<img width="1788" height="712" alt="image" src="https://github.com/user-attachments/assets/5ed5a465-431c-470f-96e0-b3ff679bf827" />

