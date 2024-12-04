from asgiref.sync import sync_to_async
from tgbot.bot.loader import bot, STICERS
from tgbot.models import Branch, Order
from tgbot.bot.utils.all_texts import BOT_WORDS


async def get_cart_items_text(orderItems: list, order: Order = None, user_language: str = 'uz'):
    # print(orderItems)
    # print(order)
    total_price = 0
    text = f"{BOT_WORDS['your_bucket'].get(user_language)}: \n\n"
    for index, item in orderItems:
        text += f"""{STICERS[index]} <b> {item.get("product__name")}</b> \n """
        text += f"""  >  {item.get("quantity")}  x  {int(item.get("product__price"))} UZS => {item.get("total_price")} UZS\n\n"""
        total_price += item.get("total_price")
        
    text += f"{BOT_WORDS['all'].get(user_language)}<b>: {total_price} UZS </b>\n\n"
    
    if order:
        text += f"{BOT_WORDS['order_info'].get(user_language)}:\n\n"
        text += f"{BOT_WORDS['order_id'].get(user_language)}: <b>#{order.id}</b>\n"
        if order.delivery == 'pickup':
            branch = await sync_to_async(Branch.objects.get)(id=order.branch_id)
            
            text += f"{BOT_WORDS['order_type'].get(user_language)}: <b>{BOT_WORDS['pickup'].get(user_language)}</b>\n"
            text += f"{BOT_WORDS['branch'].get(user_language)}: <a href='{branch.location}'><b>{branch.name}</b></a>\n"
            text += f"{BOT_WORDS['order_user'].get(user_language)}: <b>{order.full_name}</b>\n"
            text += f"{BOT_WORDS['order_phone'].get(user_language)}: <b>{order.phone}</b>\n"
        else:
            text += f"{BOT_WORDS['order_type'].get(user_language)}: <b>{BOT_WORDS['delivery'].get(user_language)}</b>\n"
            text += f"{BOT_WORDS['order_user_input'].get(user_language)}: <b>{order.full_name}</b>\n"
            text += f"{BOT_WORDS['order_phone'].get(user_language)}: <b>{order.phone}</b>\n"
            text += f"{BOT_WORDS['order_address'].get(user_language)}: <b>{order.address}</b>\n"
            text += f"{BOT_WORDS['order_addention'].get(user_language)}: <b>{order.addention}</b>\n"
        if order.is_paid:
            text += f"{BOT_WORDS['order_status'].get(user_language)}: <b>{BOT_WORDS['payment_success'].get(user_language)}</b>"
        else:
            text += f"{BOT_WORDS['order_status'].get(user_language)}: <b>{BOT_WORDS['payment_wait'].get(user_language)}</b>"
    
    return text

