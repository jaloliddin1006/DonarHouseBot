IIKO_BASE_URL = "https://api-ru.iiko.services/api/1"
IIKO_API_KEY = "b391a9a839ed47fe87f65390acf50741"
IIKO_ORGANIZATION_ID = "7d69db4a-90ce-4eba-83e4-5c3a4eec4baf"
TERMINAL_GROUP_ID_1 = "90cf7ac5-7d2c-070a-0189-637b206e0064"
TERMINAL_GROUP_ID_2 = "05e182dd-4bb6-4905-b81e-34487cba6187"
ORDER_TYPES = [
    {
        'id': '5b1508f9-fe5b-d6af-cb8d-043af587d5c2', 
        'name': 'Доставка самовывоз', 
        'orderServiceType': 'DeliveryPickUp', 
        'isDeleted': False, 
        'externalRevision': 0, 
        'isDefault': True
        },
    {
        'id': '76067ea3-356f-eb93-9d14-1fa00d082c4e', 
        'name': 'Доставка курьером', 
        'orderServiceType': 'DeliveryByCourier', 
        'isDeleted': False, 
        'externalRevision': 0, 
        'isDefault': True
        },
    {
        'id': 'bbbef4dc-5a02-7ea3-81d3-826f4e8bb3e0', 
        'name': 'Обычный заказ', 
        'orderServiceType': 'Common', 
        'isDeleted': False, 
        'externalRevision': 0, 
        'isDefault': False
        }
]