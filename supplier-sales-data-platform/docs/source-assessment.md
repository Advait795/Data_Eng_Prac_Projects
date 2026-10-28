Source Data Assessment — Online Retail

1. Dataset Overview

Source: Kaggle — Online Retail dataset

File: OnlineRetail.csv

Total rows: 541,909

Total columns: 8

Memory usage: Approximately 33.1 MB

2. Missing-Value Assessment

Column

Total rows

Missing values

Missing percentage

Description

541,909

1,454

0.27%

CustomerID

541,909

135,080

24.93%

All other columns currently show zero missing values.

3. Findings and Potential Risks

Finding 1: Missing CustomerID

Observation: 135,080 records do not have a CustomerID.

Potential impact: These transactions may not be attributable to individual customers, limiting customer-level analysis.

Investigation: Examined records with missing CustomerID to understand whether transaction and product information was still available.

Additional observation: Records with missing CustomerID include both rows with product descriptions and rows with missing descriptions. Some also have zero or negative unit prices.

Potential risk: Removing all records without a CustomerID could discard useful transaction or product information.

Current decision: No records will be removed solely because CustomerID is missing.

Finding 2: Missing Description

Observation: 1,454 records do not have a product description, representing approximately 0.27% of the dataset.

Additional observation: All 1,454 records with missing descriptions also have a missing CustomerID.

Potential impact: Product-level interpretation and reporting may be affected, even when a StockCode is available.

Investigation required: Check whether StockCode is present and whether missing descriptions can be resolved using reliable product reference data.

Current decision: No records will be removed solely because Description is missing.

Finding 3: Invoice Numbers and Negative Quantities

Observation: 10,624 records have negative quantities.

Observation: 9,288 records have invoice numbers beginning with C. All these records have negative quantities.

Additional observation: 1,336 records have negative quantities but invoice numbers that do not begin with C.

Potential interpretation: The C prefix may identify cancellation or credit transactions.

Potential risk: Rejecting every negative quantity could remove legitimate returns, reversals, or other business adjustments.

Investigation required: Examine negative-quantity records without the C prefix before defining transaction validation rules.

Current decision: Negative quantities will not be treated as invalid solely because they are negative.

Finding 4: Negative-Quantity Records Without a C Invoice Prefix

Observation: The 1,336 records in this exception group all have negative quantities, a UnitPrice of zero, and a missing CustomerID.

Invoice pattern: All 1,336 invoice numbers are unique within this exception group.

Product codes: The records contain 1,082 unique StockCodes.

Missing descriptions: 862 records have a missing Description, approximately 64.5% of the group.

Descriptions available: The remaining 474 records have a description.

Potential risk: These records may not represent ordinary sales. Including them in sales calculations without classification could distort quantity-based reporting, although their zero unit prices mean they contribute zero to a simple Quantity × UnitPrice calculation.

Current decision: Preserve the records and do not classify them as invalid until their meaning is better understood.

Finding 5: Descriptions Suggesting Stock Issues and Adjustments

Observation: Descriptions in the exception group include damages, damaged, faulty, thrown away, Unsaleable, destroyed., wet damaged, smashed, missing, mixed up, and incorrect stock entry.

Additional observation: Other descriptions include reverse 21/5/10 adjustment, sold as set on dotcom, ebay, check, and question marks.

Potential interpretation: The records may include damaged or discarded stock, reversals, corrections, and other non-standard transactions.

Important limitation: Descriptions alone do not confirm the precise business meaning of every record.

Potential risk: Treating all these records as ordinary sales or automatically rejecting them could produce misleading business metrics.

Current decision: Do not apply final transaction classifications based solely on negative quantities or descriptions.

Finding 6: Distribution of Negative Quantities in the Exception Group

The 1,336 negative-quantity records without a C invoice prefix have the following quantity statistics:

Statistic

Quantity

Count

1,336

Mean

-154.91

Standard deviation

588.29

Minimum

-9,600

25th percentile

-84

Median

-30

75th percentile

-8

Maximum

-1

Observation: The median quantity is -30, while the mean is approximately -154.91.

Observation: Quantities range from -1 to -9,600.

Potential interpretation: The mean being substantially lower than the median indicates that some records have much larger negative quantities than a typical record in this group.

Potential risk: Large negative quantities could materially affect quantity-based reporting if these records are included without understanding their purpose.

Current decision: Do not remove or cap quantities based on their magnitude alone.

Finding 7: Extreme Negative Quantities and Related Adjustment Patterns

Observation: 47 records in the exception group have quantities of -1,000 or lower.

Quantity range: The most negative quantity is -9,600.

Observed descriptions: Examples include printing smudges/thrown away, throw away, Unsaleable, destroyed., Damaged, incorrect stock entry., reverse previous adjustment, and wrongly marked. 23343 in box.

Potential pattern: Some records share nearby invoice numbers, timestamps, product descriptions, or related correction wording. For example, several records marked Unsaleable, destroyed. occur close together on 31 October 2011, and several records marked Damaged occur around 21 June 2011.

Potential interpretation: These patterns may indicate grouped stock write-offs, corrections, or adjustment events rather than ordinary sales.

Important limitation: The available data does not confirm the precise meaning or validity of every record.

Potential risk: Automatically rejecting extreme quantities could remove meaningful business events. Including them in sales reporting without classification could distort quantity metrics.

Current decision: Do not reject records based on quantity magnitude alone.

Next action: Check exact duplicate rows and continue investigating transaction patterns before defining cleaning rules.

4. Data-Type Observations

InvoiceDate is currently stored as an object and may require conversion to a datetime type.

CustomerID is stored as a floating-point number, although it represents an identifier.

InvoiceNo and StockCode are stored as objects, which is reasonable for identifiers because they may contain non-numeric characters.

Data types should be validated and converted as part of the transformation stage, with the original source data preserved.

5. Outstanding Questions

Why are some CustomerID values missing?

Can missing product descriptions be resolved using reliable reference data?

What is the exact meaning of invoice numbers beginning with C?

What business events do negative-quantity records without a C prefix represent?

Are any invoice lines duplicated?

What date range does the dataset cover?

How should cancellations, returns, stock write-offs, and adjustments be represented in downstream sales reporting?

Should records with missing descriptions or customer identifiers be retained, flagged, or excluded from particular analytical outputs?

How should exceptionally large negative quantities be handled once their business meaning is established?

6. Current Data-Handling Decisions

Preserve the original source file without modification.

Do not delete records solely because CustomerID or Description is missing.

Do not reject records solely because their quantity is negative.

Do not classify transactions based only on invoice prefixes or descriptions.

Investigate anomalies before defining validation, rejection, and transformation rules.

Keep source profiling separate from data cleaning so that decisions are evidence-based and traceable.

7. Status and Next Steps

Initial source profiling and preliminary transaction-pattern investigation are complete.

The investigation has identified missing identifiers, missing product descriptions, negative-quantity transactions, zero-price records, and descriptions suggesting stock issues or adjustments. The investigation of extreme negative quantities identified 47 records with quantities of -1,000 or lower, including several possible groups of stock adjustments or corrections.

Next steps:

Check for exact duplicate rows.

Investigate the dataset's date range.

Define explicit transaction classification and data-quality rules.

Implement transformations and validation checks in the pipeline.

Record rejected or flagged records and the reasons for each decision.

No source records have been deleted or modified as part of this assessment.

### Finding 8: Exact Duplicate Rows

- **Observation:** `df.duplicated().sum()` identifies 5,268 extra occurrences of exact duplicate rows.
- **Additional observation:** `df.duplicated(keep=False).sum()` identifies 10,147 rows belonging to groups of exact duplicates, including the first occurrence in each group.
- **Investigation:** Inspected repeated records and confirmed that some invoice-product combinations contain identical rows alongside rows with different quantities.
- **Potential risk:** Removing duplicate rows without understanding their origin could change transaction quantities and sales totals.
- **Current decision:** No duplicate rows will be removed during source assessment.
- **Next action:** Investigate the dataset's date range, then define appropriate data-quality and deduplication rules based on the evidence.

### Finding 9: Date Range and Date Parsing

- **Observation:** `InvoiceDate` is stored as a string in the source dataset.
- **Investigation:** Inspected the source date format and converted the values using `pd.to_datetime()` with the explicit format `%m/%d/%Y %H:%M`.
- **Date range:** Earliest invoice date: `2010-12-01 08:26:00`. Latest invoice date: `2011-12-09 12:50:00`.
- **Validation:** Zero date values failed conversion using the specified format.
- **Potential risk:** Incorrect date-format assumptions can produce invalid dates or misinterpret dates, affecting time-based reporting.
- **Current decision:** Use the verified date format for parsing. Preserve the original source data unchanged and perform transformations on a separate working representation.
- **Status:** Initial date-range investigation completed. Further validation will be included in pipeline testing.

## 10. Data Quality Flags and Missing-Value Overlap

### Investigation

Created Boolean flags to identify records with missing customer IDs and product descriptions.

```python
df["customer_id_missing"] = df["CustomerID"].isna()
df["description_missing"] = df["Description"].isna()
```

### Findings

| Data quality check                         | Records |
| ------------------------------------------ | ------: |
| Total source records                       | 541,909 |
| Missing CustomerID                         | 135,080 |
| Missing Description                        |   1,454 |
| Both CustomerID and Description missing    |   1,454 |
| CustomerID missing but Description present | 133,626 |

All 1,454 records with missing descriptions also have missing customer IDs.

Of the 135,080 records with missing customer IDs:

- 1.08% also have missing descriptions.
- 98.92% have a non-missing description.

### Interpretation

Missing customer IDs and missing product descriptions are distinct data-quality issues, although they overlap in this dataset.

A missing customer ID does not automatically make a transaction unusable for every reporting purpose. For example, a record may still contribute to overall sales reporting if its transaction details satisfy the applicable business rules, even when customer-level attribution is unavailable.

A non-missing description does not, by itself, establish that the product information is correct.

### Initial Handling Decision

- Retain records with missing customer IDs and flag them for data-quality monitoring.
- Retain records with missing descriptions and flag them separately.
- Keep the two flags independent so that each issue can be investigated and measured separately.
- Do not invent missing values or delete records solely because these fields are missing.

### Validation

The Boolean flags were checked against the source data. The counts matched the initial profiling results:

- `customer_id_missing`: 135,080 records.
- `description_missing`: 1,454 records.
- Both flags set to `True`: 1,454 records.

These checks validate the observed counts and overlap. They do not establish the cause of the missing values or whether every affected record is suitable for every downstream reporting purpose.

### Finding 11: Zero-Price Records with Positive Quantities

- **Observation:** 2,515 records have a `UnitPrice` of zero. Of these, 1,179 have a positive `Quantity`, while 1,336 have a negative `Quantity`.
- **Investigation:** The 1,179 positive-quantity records contain 72,603 units in total and contribute £0 to recorded line revenue. Of these records, 1,139 have a missing `CustomerID` and 592 have a missing `Description`.
- **Invoice-level analysis:** 400 records belong to 53 distinct invoices that also contain at least one positive-priced line. The remaining 779 records belong to 766 distinct invoices with no positive-priced line identified.
- **Additional investigation:** Inspected invoice `537197`, which contains a zero-price product alongside positively priced products and a postage line. This is consistent with, but does not prove, the possibility of a free item or promotional transaction.
- **Potential risk:** Removing all zero-price records could discard meaningful transaction or operational information. Including them without an explicit business rule could also affect sales reporting and quantity-based metrics.
- **Current decision:** Preserve these records during source assessment. Do not automatically delete them or classify them as errors.
- **Next action:** Investigate the business meaning of zero-price records and define explicit rules for revenue reporting and quantity-based analysis before transforming the data.
