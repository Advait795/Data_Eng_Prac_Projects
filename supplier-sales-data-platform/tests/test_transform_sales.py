import pandas as pd 
import pytest
from src.transform_sales import transform_data, validate_data

def test_transform_date():
    df = pd.DataFrame({
        "InvoiceNo" : ["536365", "536366"],
        "StockCode" : ["85123A", "71053"],
        "Description": ["Product A", None],
        "Quantity" : [2,3],
        "InvoiceDate" : ["12/1/2010 08:26", "12/1/2010 08:30"],
        "UnitPrice": [5.0, 2.0],
        "CustomerID": [17850.0, None],
        "Country": ["United Kingdom", "France"] 
    })

    result = transform_data(df)

    assert len(result) == 2
    assert result["LineRevenue"].tolist() == [10.0, 6.0]
    assert result["customer_id_missing"].tolist() == [False, True]
    assert result["description_missing"].tolist() == [False, True]
    assert pd.api.types.is_datetime64_any_dtype(result["InvoiceDate"])

def test_trnasform_does_not_modify_input():
    df = pd.DataFrame({
        "InvoiceNo": ["536365"],
        "StockCode": ["85123A"],
        "Description": ["Product A"],
        "Quantity": [2],
        "InvoiceDate": ["12/1/2010 08:26"],
        "UnitPrice": [5.0],
        "CustomerID": [17850.0],
        "Country": ["United Kingdom"]
    })

    original_df = df.copy(deep=True) 

    transform_data(df)

    pd.testing.assert_frame_equal(df, original_df)

def test_transform_raises_error_for_inalid_date():
    df = pd.DataFrame({
        "InvoiceDate": ["not-a-date"],
        "Quantity": [2],
        "UnitPrice": [5.0],
        "CustomerID": [17850.0],
        "Description": ["Product A"]
    })

    with pytest.raises(ValueError):
        transform_data(df)

def test_validate_data_catches_incorrect_revenue():
    df = pd.DataFrame({
        "InvoiceDate": ["12/1/2010 08:26"],
        "Quantity": [2],
        "UnitPrice": [5.0],
        "CustomerID": [17850.0],
        "Description": ["Product A"]
    })

    result = transform_data(df)

    # Deliberately introduce an incorrect value
    result.loc[0, "LineRevenue"] = 999.0


    with pytest.raises(AssertionError, match="Revenue calculation mismatch"):
        validate_data(result)