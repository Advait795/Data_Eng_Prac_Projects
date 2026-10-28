# Data Quality Rules

| Data issue                   | Evidence found          | Proposed handling                                                                                                     |
| ---------------------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Missing `CustomerID`         | 135,080 records         | Preserve records and flag missing customer IDs.                                                                       |
| Missing `Description`        | 1,454 records           | Preserve records and flag missing descriptions.                                                                       |
| Negative quantity            | 10,624 records          | Preserve records and investigate transaction types before deciding how to handle them in sales reporting.             |
| Zero price                   | 2,515 records           | Preserve records and investigate their business meaning.                                                              |
| Negative price               | 2 records               | Preserve records and flag them as potential accounting adjustments.                                                   |
| Exact duplicate rows         | 5,268 extra occurrences | Do not automatically remove duplicates until their origin and business impact are understood.                         |
| Invoice dates stored as text | All 541,909 records     | Parse `InvoiceDate` into a datetime column, validate parsing results, and preserve the original raw source unchanged. |

## Implementation Principles

1. **Preserve raw data:** Never modify the original source CSV during transformation.
2. **Flag before removing:** Identify data-quality issues before deciding whether records should be excluded.
3. **Avoid unsupported assumptions:** Do not invent missing values or assume that unusual records are invalid without sufficient evidence.
4. **Validate transformations:** Check record counts, data types, missing values, and calculated values after processing.
5. **Keep decisions traceable:** Document the reasoning behind data-quality rules and any changes to those rules.

## Current Status

These rules are provisional. They will be refined as the source data is investigated further and the transformation pipeline is implemented and tested.
