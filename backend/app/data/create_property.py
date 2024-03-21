import json
import sys

import pandas as pd
import requests
from requests.auth import HTTPBasicAuth

# Constants
EXCEL_FILE = "/Users/soumyatalikoti/Downloads/Enodo_Skills_Assessment_Data_File.xlsx"

BASE_URL = "http://localhost:8000"
LOGIN_URL = "http://localhost:8000/token"
CREATE_PROPERTY_URL = "http://localhost:8000/properties/"
UPDATE_PROPERTY_URL = f"{BASE_URL}/properties/{{}}"
DELETE_PROPERTY_URL = f"{BASE_URL}/properties/{{}}"
RANGE_PROPERTY_URL = f"{BASE_URL}/properties/range"
PROPERTY_LISTINGS = f"{BASE_URL}/properties_listings/"
LOG_FILE = "failed_logs.txt"


def get_access_token():
    try:
        response = requests.post(
            LOGIN_URL,
            auth=HTTPBasicAuth("admin", "password")
        )
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.RequestException as e:
        print(f"Error getting access token: {e}")
        return None


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, float):
            if obj == float('inf') or obj == float('-inf') or obj != obj:  # Checks for inf, -inf, NaN
                return None  # Convert non-compliant values to None
        return super(CustomJSONEncoder, self).default(obj)


def row_to_property_base(row):
    return {
        "full_address": str(row["Full Address"]),
        "longitude": str(row["Longitude"]),
        "latitude": str(row["Latitude"]),
        "zip": str(row["Zip"]),
        "rec_type": str(row["REC_TYPE"]),
        "pin": str(row["PIN"]),
        "ovacls": str(row["OVACLS"]),
        "class_description": str(row["CLASS_DESCRIPTION"]),
        "current_land": str(row["CURRENT_LAND"]),
        "current_building": str(row["CURRENT_BUILDING"]),
        "current_total": str(row["CURRENT_TOTAL"]),
        "estimated_market_value": str(row["ESTIMATED_MARKET_VALUE"]),
        "prior_land": str(row["PRIOR_LAND"]),
        "prior_building": str(row["PRIOR_BUILDING"]),
        "prior_total": str(row["PRIOR_TOTAL"]),
        "pprior_land": str(row["PPRIOR_LAND"]),
        "pprior_building": str(row["PPRIOR_BUILDING"]),
        "pprior_total": str(row["PPRIOR_TOTAL"]),
        "pprior_year": str(row["PPRIOR_YEAR"]),
        "town": str(row["TOWN"]),
        "volume": str(row["VOLUME"]),
        "loc": str(row["LOC"]),
        "tax_code": str(row["TAX_CODE"]),
        "neighborhood": str(row["NEIGHBORHOOD"]),
        "houseno": str(row["HOUSENO"]),
        "dir": str(row["DIR"]),
        "street": str(row["STREET"]),
        "suffix": str(row["SUFFIX"]),
        "apt": str(row["APT"]),
        "city": str(row["CITY"]),
        "res_type": str(row["RES_TYPE"]),
        "bldg_use": str(row["BLDG_USE"]),
        "apt_desc": str(row["APT_DESC"]),
        "comm_units": str(row["COMM_UNITS"]),
        "ext_desc": str(row["EXT_DESC"]),
        "full_bath": str(row["FULL_BATH"]),
        "half_bath": str(row["HALF_BATH"]),
        "bsmt_desc": str(row["BSMT_DESC"]),
        "attic_desc": str(row["ATTIC_DESC"]),
        "ac": str(row["AC"]),
        "fireplace": str(row["FIREPLACE"]),
        "gar_desc": str(row["GAR_DESC"]),
        "age": str(row["AGE"]),
        "building_sq_ft": str(row["BUILDING_SQ_FT"]),
        "land_sq_ft": str(row["LAND_SQ_FT"]),
        "bldg_sf": str(row["BLDG_SF"]),
        "units_tot": str(row["UNITS_TOT"]),
        "multi_sale": str(row["MULTI_SALE"]),
        "deed_type": str(row["DEED_TYPE"]),
        "sale_date": str(row["SALE_DATE"]),
        "sale_amount": str(row["SALE_AMOUNT"]),
        "appcnt": str(row["APPCNT"]),
        "appeal_a": str(row["APPEAL_A"]),
        "appeal_a_status": str(row["APPEAL_A_STATUS"]),
        "appeal_a_result": str(row["APPEAL_A_RESULT"]),
        "appeal_a_reason": str(row["APPEAL_A_REASON"]),
        "appeal_a_pin_result": str(row["APPEAL_A_PIN_RESULT"]),
        "appeal_a_propav": str(row["APPEAL_A_PROPAV"]),
        "appeal_a_currav": str(row["APPEAL_A_CURRAV"]),
        "appeal_a_resltdate": str(row["APPEAL_A_RESLTDATE"])
    }


def post_property(token_, property_data):
    headers = {
        "Authorization": f"Bearer {token_}",
        "Content-Type": "application/json"
    }
    json_data = json.dumps(property_data, cls=CustomJSONEncoder)
    response = requests.post(CREATE_PROPERTY_URL, data=json_data, headers=headers)
    if response.status_code != 201:
        print(f"Failed to post property. Response: {response.text}")
    return response


def get_property(property_id):
    url = f"{BASE_URL}/properties/{property_id}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        property_data = response.json()
        print("Property data:", property_data)
        return property_data
    elif response.status_code == 404:
        print("Property not found")
    else:
        print(f"Failed to retrieve property. Status code: {response.status_code}, Response: {response.text}")


def update_property(token_, property_id, property_data):
    url = UPDATE_PROPERTY_URL.format(property_id)
    headers = {"Authorization": f"Bearer {token_}", "Content-Type": "application/json"}
    json_data = json.dumps(property_data, cls=CustomJSONEncoder)
    response = requests.put(url, data=json_data, headers=headers)
    return response


def delete_property(token_, property_id):
    url = DELETE_PROPERTY_URL.format(property_id)
    headers = {"Authorization": f"Bearer {token_}"}
    response = requests.delete(url, headers=headers)
    return response.json()


def get_property_listings(token_):
    url = PROPERTY_LISTINGS
    headers = {"Authorization": f"Bearer {token_}"}
    response = requests.get(url, headers=headers)
    return response.json()


def get_property_listings_range(token_):
    url = RANGE_PROPERTY_URL
    headers = {"Authorization": f"Bearer {token_}", "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()


if __name__ == "__main__":
    token = get_access_token()
    print(get_property_listings_range(token))
    # if token:
    #     df = pd.read_excel(EXCEL_FILE, dtype=str)
    #
    #     for index, row in df.iterrows():
    #         property_data = row_to_property_base(row)
    #         post_response = post_property(token, property_data)
    #         print(post_response.json())
    #         if post_response.status_code == 201:
    #             property_id = post_response.json().get("id")
    #             print(f"Property {property_id} created.")

                # # Update the property
                # update_response = update_property(token, property_id, {"zip": "99999"})
                # if update_response.status_code == 200:
                #     print(f"Property {property_id} updated.")
                # else:
                #     print(f"Failed to update property {property_id}.")

                # # Delete the property
                # delete_response = delete_property(token, property_id)
                # if delete_response.status_code == 204:
                #     print(f"Property {property_id} deleted.")
                # else:
                #     print(f"Failed to delete property {property_id}.")
    #         else:
    #             print("Failed to create property.")
    # else:
    #     print("Failed to obtain access token.")