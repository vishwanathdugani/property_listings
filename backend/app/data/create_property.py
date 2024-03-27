import sys

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

# Constants
EXCEL_FILE_PATH = 'Enodo_Skills_Assessment_Data_File.xlsx'
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/token"

# Endpoint URLs
ENDPOINTS = {
    "property": f"{BASE_URL}/properties/",
    "classification": f"{BASE_URL}/property_classifications/",
    "assessment": f"{BASE_URL}/assessments/",
    "sales_appeal": f"{BASE_URL}/sales_appeals/",
    "feature": f"{BASE_URL}/property_features/",
    "misc_info": f"{BASE_URL}/misc_info/"
}

def get_access_token(username="admin", password="password"):
    try:
        response = requests.post(
            LOGIN_URL,
            auth=HTTPBasicAuth(username, password)
        )
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.RequestException as e:
        print(f"Error getting access token: {e}")
        return None


def post_data(endpoint, token, data):
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(endpoint, headers=headers, json=data)
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"Failed to post data to {endpoint}. Response: {response.status_code}, {response.text}")
        return None


def parse_decimal(value):
    return float(value)


def parse_integer(value):
    try:
        return int(value)
    except Exception as e:
        return None


def parse_date(value):
    try:
        return datetime.strptime(str(value), '%Y-%m-%d').date() if value and str(value).lower() != 'nan' else None
    except ValueError:
        return None


def main():
    token = get_access_token()
    if not token:
        print("Failed to obtain access token.")
        return

    df = pd.read_excel(EXCEL_FILE_PATH, decimal=",")

    for _, row in df.iterrows():
        try:
            property_data = {
                # Mapping Excel columns to property fields
                "longitude": row["Longitude"],
                "latitude": row["Latitude"],
                "zip": str(row["Zip"]).strip(),
                "house_no": str(row["HOUSENO"]),
                "dir": row["DIR"].strip(),
                "street": row["STREET"].strip(),
                "suffix": row["SUFFIX"].strip(),
                "apt": str(row["APT"]).strip(),
                "city": row["CITY"].strip(),
            }
            property_resp = post_data(ENDPOINTS["property"], token, property_data)
            if not property_resp:
                print("Failed to create property.")
                continue

            property_id = property_resp["id"]

            classification_data = {
                "property_id": property_id,
                "ovac_ls": parse_integer(row["OVACLS"]),
                "class_description": row["CLASS_DESCRIPTION"].strip(),
                "res_type": row["RES_TYPE"].strip(),
                "bldg_use": str(row["BLDG_USE"]).strip(),
                "apt_desc": str(row["APT_DESC"]).strip(),
            }
            post_data(ENDPOINTS["classification"], token, classification_data)

            assessment_data = {
                "property_id": property_id,
                "current_land": parse_integer(row["CURRENT_LAND"]),
                "current_building": parse_integer(row["CURRENT_BUILDING"]),
                "current_total": parse_integer(row["CURRENT_TOTAL"]),
                "estimated_market_value": parse_integer(row["ESTIMATED_MARKET_VALUE"]),
                "prior_land": parse_integer(row["PRIOR_LAND"]),
                "prior_building": parse_integer(row["PRIOR_BUILDING"]),
                "prior_total": parse_integer(row["PRIOR_TOTAL"]),
            }
            post_data(ENDPOINTS["assessment"], token, assessment_data)

            sales_appeal_data = {
                "property_id": property_id,
                "multi_sale": bool(row["MULTI_SALE"]),
                "deed_type": parse_integer(row["DEED_TYPE"]),
                "sale_date": parse_date(row["SALE_DATE"]),
                "sale_amount": row["SALE_AMOUNT"],
            }
            post_data(ENDPOINTS["sales_appeal"], token, sales_appeal_data)

            feature_data = {
                "property_id": property_id,
                "comm_units": parse_integer(row["COMM_UNITS"]),
                "ext_desc": row["EXT_DESC"].strip(),
                "full_bath": parse_integer(row["FULL_BATH"]),
                "half_bath": parse_integer(row["HALF_BATH"]),
                "bsmnt_desc": row["BSMT_DESC"].strip(),
                "attic_desc": str(row["ATTIC_DESC"]).strip(),
                "ac": row["AC"],
                "fireplace": parse_integer(row["FIREPLACE"]),
                "gar_desc": row["GAR_DESC"].strip(),
                "age": parse_integer(row["AGE"]),
                "building_sq_ft": parse_integer(row["BUILDING_SQ_FT"]),
                "land_sq_ft": parse_integer(row["LAND_SQ_FT"]),
            }
            post_data(ENDPOINTS["feature"], token, feature_data)

            misc_info_data = {
                "property_id": property_id,
                "rec_type": row["REC_TYPE"].strip(),
                "pin": row["PIN"],
                "town": row["TOWN"],
                "volume": parse_integer(row["VOLUME"]),
                "loc": row["LOC"].strip(),
                "tax_code": row["TAX_CODE"],
                "neighborhood": row["NEIGHBORHOOD"],
            }
            post_data(ENDPOINTS["misc_info"], token, misc_info_data)
        except Exception as e:
            print(e)
            sys.exit()


if __name__ == "__main__":
    main()

