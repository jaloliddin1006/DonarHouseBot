from django.test import TestCase

# Create your tests here.
import requests


BASE_URL = "https://api-ru.iiko.services"
API_KEY = "b391a9a839ed47fe87f65390acf50741"


####################### access token olish #####################
def get_access_token(api_key):
    url = f"{BASE_URL}/api/1/access_token"
    response = requests.post(url, json={"apiLogin": api_key})
    response.raise_for_status()
    return response.json().get("token")

access_token = get_access_token(API_KEY)

# access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBcGlMb2dpbklkIjoiZGIzNWQ1Y2MtYTYzZi00NDBkLTg0NzktYzBiN2E3M2IxNzI1IiwibmJmIjoxNzM2MjQ1NjQyLCJleHAiOjE3MzYyNDkyNDIsImlhdCI6MTczNjI0NTY0MiwiaXNzIjoiaWlrbyIsImF1ZCI6ImNsaWVudHMifQ.Ro7HZ_O5uGcRAjxPvWYfRF3wPOa0L-AnEOxNJbwV7yc"
print(f"Access Token: {access_token}")


# def get_products(token):
#     url = f"{BASE_URL}/api/1/products"
#     headers = {"Authorization": f"Bearer {token}"}
#     response = requests.get(url, headers=headers)
#     # response.raise_for_status()
#     return response.json()

# # products = get_products(access_token)
# # print(products)



####################### Tashkilotlar ro'yxatini olish #####################

def get_organizations(token):
    url = f"{BASE_URL}/api/1/organizations"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "organizationIds": ["497f6eca-6276-4993-bfeb-53cbbbba6f08"],  # Kerakli tashkilot ID
        "returnAdditionalInfo": True,
        "includeDisabled": True,
        "returnExternalData": ["string"]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Xatoliklarni aniqlash
    return response.json()

# organizations = get_organizations(access_token)
# for org in organizations.get('organizations'):
#     print(org)
# print(organizations)

organization_id = "7d69db4a-90ce-4eba-83e4-5c3a4eec4baf"


####################### Terminal guruhlarini olish #####################
def get_terminal_groups(token, organization_id):
    url = f"{BASE_URL}/api/1/terminal_groups"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "organizationIds": [organization_id],
        "includeDisabled": True,
        "returnExternalData": ["string"]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Xatoliklarni aniqlash uchun
    return response.json()

# terminal_groups = get_terminal_groups(access_token, organization_id)
# print(terminal_groups)
terminal_group_id_1 = "90cf7ac5-7d2c-070a-0189-637b206e0064"
terminal_group_id_2 = "05e182dd-4bb6-4905-b81e-34487cba6187"


####################### Maxsulotlar ro'yxatini olish #####################

def get_nomenclature(token, organization_id):
    url = f"{BASE_URL}/api/1/nomenclature"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "organizationId": organization_id,
        "startRevision": 0
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Xatoliklarni aniqlash uchun
    return response.json()

# nomenclature = get_nomenclature(access_token, organization_id)

# for product in nomenclature.get("products", []):
#     print(f"id: {product.get('id')}| code: {product.get('code')}| order: {product.get('order')}| parentGroup: {product.get('parentGroup')} | weight: {product.get('weight')}| unit: {product.get('measureUnit')}| prices: ", end=" ")
#     for price in product.get('sizePrices', []):
#         print(price.get('price').get('currentPrice'), end=" | ")
#     print(f", name: {product.get('name')}")
    
    
productId = "28437f20-7303-440d-a8ca-afde01732b7e"
    
    
    
    
    
#######################################   create or update customer #############################

def create_or_update_customer(access_token, phone, organization_id, name=None, email=None):
    """
    Simplified function to create or update a customer in the iiko system.

    :param access_token: str - Access token for the API
    :param customer_id: str - Unique identifier for the customer
    :param phone: str - Customer phone number
    :param organization_id: str - Organization ID
    :param name: str - Customer name (optional)
    :param email: str - Customer email (optional)
    :return: dict - Response from the API
    """
    url = f"{BASE_URL}/api/1/loyalty/iiko/customer/create_or_update"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        # "id": customer_id,
        "phone": phone,
        "organizationId": organization_id,
        "name": name,
        "email": email
    }

    # Remove keys with None values
    payload = {k: v for k, v in payload.items() if v is not None}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

# Example usage
# try:
#     # access_token = "your_access_token"
#     # customer_id = "497f6eca-6276-4993-bfeb-53cbbbba6f08"

#     response = create_or_update_customer(
#         # customer_id,
#         access_token,
#         phone = "+998932977419",
#         organization_id=organization_id,
#         name="Jaloliddin",
#         email="jmamatmusayev@gmail.com"
#     )

#     print("Customer created/updated successfully:", response)
# except requests.exceptions.HTTPError as e:
#     print("Error while creating/updating customer:", e)

customer_id="f8990000-6beb-ac1f-e366-08dd2e876d32"
    
    

################################## create order ####################################
import requests
import uuid

def create_order(
    access_token,
    organization_id,
    terminal_group_id,
    items,
    customer=None,
    order_id=None,
    external_number=None,
    comment=None,
    order_type_id=None,
    tab_name=None
):
   
    url = f"{BASE_URL}/api/1/orders/create"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "organizationId": organization_id,
        "terminalGroupId": terminal_group_id,
        # "order": {
        #     # "id": order_id or str(uuid.uuid4()),
        #     # "externalNumber": external_number,
        #     "items": items,
        #     "customer": customer,
        #     "comment": comment,
        #     # "orderTypeId": order_type_id,
        #     # "tabName": tab_name,
        # },
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

# Misol uchun foydalanish
# access_token = "your_access_token"
# organization_id = "7bc05553-4b68-44e8-b7bc-37be63c6d9e9"
# terminal_group_id = "e8d0a621-90b7-4c0a-8c82-8a880a5ba3a8"

items = [
    {
        "productId": productId,
        "price": 12000,
        "amount": 2,
        "type": "Product",
    }
]

customer = {
    "phone": "+998901234567",
    "name": "John",
    "surname": "Doe",
    "email": "john.doe@example.com",
    "shouldReceiveOrderStatusNotifications": True,
    "type": "regular",
}

# result = create_order(
#     access_token,
#     organization_id,
#     terminal_group_id_1,
#     items,
#     # customer=customer,
#     comment="Qo'shimcha so'rov: qo'shimcha sous kerak.",
# )
# print(result)








################################ send sms ######################################

# def send_sms(access_token, phone, text, organization_id):
#     """
#     iiko API orqali SMS yuborish.

#     :param access_token: iiko API tokeni
#     :param phone: Telefon raqami (string formatda)
#     :param text: SMS matni
#     :param organization_id: Tashkilot IDsi
#     :return: Javob JSON yoki xatolik xabari
#     """
#     url = "https://api-ru.iiko.services/api/1/loyalty/iiko/message/send_sms"
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "phone": phone,
#         "text": text,
#         "organizationId": organization_id
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         return {"error": response.status_code, "message": response.text}

# # Misol uchun foydalanish
# # access_token = "your_access_token"
# phone = "+998932977419"
# text = "Salom, sizni bizning maxsus takliflarimizga taklif qilamiz!"
# # organization_id = "7bc05553-4b68-44e8-b7bc-37be63c6d9e9"

# result = send_sms(access_token, phone, text, organization_id)
# print(result)