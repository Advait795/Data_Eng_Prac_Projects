# SQL Analysis — Supplier-to-Sales Data Platform

## 1. Overview

This document records the initial SQL analysis performed on the `stg_online_retail` staging table in PostgreSQL.

The objective is to explore retail transaction data, identify revenue patterns, and understand customer and product performance.

**Source table:** `stg_online_retail`  
**Database:** `supplier_sales_db`  
**Total records:** 541,909

---

## 2. Revenue Analysis by Country

### Business Question

Which countries generate the highest recorded revenue?

### SQL Query

```sql
SELECT
    country,
    SUM(line_revenue) AS total_revenue
FROM stg_online_retail
GROUP BY country
ORDER BY total_revenue DESC;
```

### Findings

| Country        | Total Revenue |
| -------------- | ------------: |
| United Kingdom | £8,187,806.36 |
| Netherlands    |   £284,661.54 |
| EIRE           |   £263,276.82 |
| Germany        |   £221,698.21 |
| France         |   £197,403.90 |

**Observation:**

- The United Kingdom contributes the highest recorded revenue.
- The Netherlands ranks second.
- Recorded revenue is significantly concentrated in the United Kingdom.

---

## 3. Monthly Revenue Analysis

### Business Question

How does recorded revenue change over time?

### SQL Query

```sql
SELECT
    DATE_TRUNC('month', invoice_date) AS sales_month,
    ROUND(SUM(line_revenue), 2) AS monthly_revenue
FROM stg_online_retail
GROUP BY DATE_TRUNC('month', invoice_date)
ORDER BY sales_month;
```

### Findings

| Month          |       Revenue |
| -------------- | ------------: |
| December 2010  |   £748,957.02 |
| January 2011   |   £560,000.26 |
| February 2011  |   £498,062.65 |
| March 2011     |   £683,267.08 |
| April 2011     |   £493,207.12 |
| May 2011       |   £723,333.51 |
| June 2011      |   £691,123.12 |
| July 2011      |   £681,300.11 |
| August 2011    |   £682,680.51 |
| September 2011 | £1,019,687.62 |
| October 2011   | £1,070,704.67 |
| November 2011  | £1,461,756.25 |
| December 2011  |   £433,668.01 |

**Observations:**

- November 2011 recorded the highest monthly revenue of £1,461,756.25.
- Revenue increased considerably from September onwards.
- February 2011 recorded the lowest monthly revenue.
- December 2011 is a partial month because the dataset ends on 9 December 2011.

---

## 4. Top 10 Products and Services by Revenue

### Business Question

Which products or services generate the highest recorded revenue?

### SQL Query

```sql
SELECT
    stock_code,
    description,
    ROUND(SUM(line_revenue), 2) AS total_revenue
FROM stg_online_retail
GROUP BY stock_code, description
ORDER BY total_revenue DESC
LIMIT 10;
```

### Findings

| Stock Code | Description                        |     Revenue |
| ---------- | ---------------------------------- | ----------: |
| DOT        | DOTCOM POSTAGE                     | £206,245.48 |
| 22423      | REGENCY CAKESTAND 3 TIER           | £164,762.19 |
| 47566      | PARTY BUNTING                      |  £98,302.98 |
| 85123A     | WHITE HANGING HEART T-LIGHT HOLDER |  £97,715.99 |
| 85099B     | JUMBO BAG RED RETROSPOT            |  £92,356.03 |
| 23084      | RABBIT NIGHT LIGHT                 |  £66,756.59 |
| POST       | POSTAGE                            |  £66,230.64 |
| 22086      | PAPER CHAIN KIT 50'S CHRISTMAS     |  £63,791.94 |
| 84879      | ASSORTED COLOUR BIRD ORNAMENT      |  £58,959.73 |
| 79321      | CHILLI LIGHTS                      |  £53,768.06 |

**Observations:**

- DOTCOM POSTAGE has the highest recorded revenue.
- Postage and service-related entries appear alongside physical products.
- Product and non-product charges may need to be classified separately for more meaningful product-performance reporting.

---

## 5. Top 10 Customers by Revenue

### Business Question

Which customers contribute the highest recorded revenue?

### SQL Query

```sql
SELECT
    customer_id,
    COUNT(DISTINCT invoice_no) AS total_orders,
    ROUND(SUM(line_revenue), 2) AS total_revenue
FROM stg_online_retail
WHERE customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10;
```

### Findings

| Customer ID | Total Orders | Total Revenue |
| ----------- | -----------: | ------------: |
| 14646       |           77 |   £279,489.02 |
| 18102       |           62 |   £256,438.49 |
| 17450       |           55 |   £187,482.17 |
| 14911       |          248 |   £132,572.62 |
| 12415       |           26 |   £123,725.45 |
| 14156       |           66 |   £113,384.14 |
| 17511       |           46 |    £88,125.38 |
| 16684       |           31 |    £65,892.08 |
| 13694       |           60 |    £62,653.10 |
| 15311       |          118 |    £59,419.34 |

**Observations:**

- Customer 14646 has the highest recorded revenue at £279,489.02.
- Customer 18102 ranks second.
- Customer 14911 has the highest invoice count among the top 10 customers, with 248 invoices.
- Records without a CustomerID were excluded from this customer-level analysis.

---

## 6. Monthly Order Volume and Average Order Value

### Business Question

How many orders are placed each month, and what is the average invoice value?

### SQL Query

```sql
WITH invoice_totals AS (
    SELECT
        DATE_TRUNC('month', invoice_date) AS sales_month,
        invoice_no,
        SUM(line_revenue) AS invoice_revenue
    FROM stg_online_retail
    GROUP BY 1, 2
)
SELECT
    sales_month,
    COUNT(*) AS total_orders,
    ROUND(SUM(invoice_revenue), 2) AS monthly_revenue,
    ROUND(AVG(invoice_revenue), 2) AS average_order_value
FROM invoice_totals
GROUP BY sales_month
ORDER BY sales_month;
```

### Findings

| Month          | Total Orders | Monthly Revenue | Average Order Value |
| -------------- | -----------: | --------------: | ------------------: |
| December 2010  |        2,025 |     £748,957.02 |             £369.86 |
| January 2011   |        1,476 |     £560,000.26 |             £379.40 |
| February 2011  |        1,393 |     £498,062.65 |             £357.55 |
| March 2011     |        1,983 |     £683,267.08 |             £344.56 |
| April 2011     |        1,744 |     £493,207.12 |             £282.80 |
| May 2011       |        2,162 |     £723,333.51 |             £334.57 |
| June 2011      |        2,012 |     £691,123.12 |             £343.50 |
| July 2011      |        1,927 |     £681,300.11 |             £353.55 |
| August 2011    |        1,737 |     £682,680.51 |             £393.02 |
| September 2011 |        2,327 |   £1,019,687.62 |             £438.20 |
| October 2011   |        2,637 |   £1,070,704.67 |             £406.03 |
| November 2011  |        3,462 |   £1,461,756.25 |             £422.23 |
| December 2011  |        1,015 |     £433,668.01 |             £427.26 |

**Observations:**

- November 2011 recorded the highest order volume, with 3,462 invoices.
- November also recorded the highest monthly revenue.
- September 2011 recorded the highest average order value of £438.20.
- December 2011 contains partial-month data.

---

## 7. SQL Concepts Practised

The analysis provided practical experience with the following PostgreSQL concepts:

| SQL Concept       | Application                                                 |
| ----------------- | ----------------------------------------------------------- |
| `SELECT`          | Retrieving relevant columns                                 |
| `SUM()`           | Calculating total revenue                                   |
| `COUNT()`         | Counting records and invoices                               |
| `COUNT(DISTINCT)` | Counting unique invoices                                    |
| `GROUP BY`        | Aggregating data by country, month and customer             |
| `ORDER BY`        | Ranking results                                             |
| `LIMIT`           | Retrieving the top 10 results                               |
| `WHERE`           | Filtering missing CustomerIDs                               |
| `DATE_TRUNC()`    | Grouping timestamps by month                                |
| `ROUND()`         | Formatting numerical results                                |
| CTE (`WITH`)      | Calculating invoice-level totals before monthly aggregation |

---

## 8. Data Interpretation and Limitations

The SQL analysis represents an initial exploration of the transaction data.

The following limitations should be considered:

1. Revenue calculations use `Quantity × UnitPrice` without final transaction classification.
2. Negative quantities, cancellations, returns and potential stock adjustments have not yet been fully classified.
3. Postage and other non-product entries appear in product revenue rankings.
4. Customer-level analysis excludes records with missing CustomerIDs.
5. December 2011 represents a partial month.

Consequently, these results should be interpreted as **preliminary recorded transaction metrics**, rather than final net sales or validated business KPIs.

---

## 9. Current Status and Next Steps

### Completed

- Initial source data assessment.
- Data-quality investigation.
- Python transformation pipeline.
- Automated transformation tests.
- PostgreSQL staging table creation.
- CSV ingestion into PostgreSQL.
- Initial database validation.
- Exploratory SQL analysis.

### Next Steps

1. Design an analytical data model.
2. Identify suitable fact and dimension tables.
3. Define transaction classification and handling rules.
4. Develop analytical tables in PostgreSQL.
5. Automate Python-to-PostgreSQL ingestion.
6. Extend the architecture towards AWS.

**Current project phase:** Initial data ingestion, transformation and exploratory SQL analysis completed.
