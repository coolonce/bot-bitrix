from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import message
from aiogram.utils import executor

import hashlib

from keyboard import *


from btrx import *

import logging
TOKEN = "1920575611:AAFIuquH_Z7lDvj8ZuJk0LHa00YnpQbHHzo"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Приветствуем нас в нашем боте, чтобы ознакомится с командами введите /help")

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply("Напишите _Компания: название компании_ (вводить без точки в конце)", parse_mode='Markdown')


@dp.message_handler()
async def echo(message: types.Message):
    await handle_company_mesage(message)
    # await message.answer(company_name)


async def handle_company_mesage(message: types.Message):
    company_name = ""
    msg = message.text.replace(':', '').split(' ')
    if len(msg) > 1:
        company_name = msg[1]
        company_id = find_companyId_by_name(company_name)
        if not company_id == -1 :
            user_contact_id = get_contact_id(message.from_user.first_name, message.from_user.last_name, message.chat.id)
            create_deal_for_contract(user_contact_id, message.chat.id, 15, company_id)
            await message.answer(
                '''Информация по компании %s найдена.\nДля получения всей информации необходимо оплатить.\nПолучить ссылку на оплату?''' % (msg[1]),
             reply_markup=keyboard_ysnNo)
        else:
            await message.answer("Компания не найдена")
    else:
        await message.answer("Введите _/help_ для помощи.", parse_mode='Markdown')



@dp.callback_query_handler(lambda c: c.data == 'accept')
async def process_callback_accept(callback_query: types.CallbackQuery):
    payment_url = create_payment_url(callback_query.message.from_user.first_name, callback_query.message.from_user.last_name, callback_query.message.chat.id)
    await callback_query.message.answer(payment_url, parse_mode='HTML')



#TODO тут я заебался уже
def create_payment_url(first_name, last_name, chat_id):
    amount = "100" #TODO в конфиг
    contact_id = get_contact_id(first_name, last_name, chat_id)

    deal_id = get_deal_by_chat_id(chat_id, contact_id)

    merchantLogin = 'MyRenter'
    password = 'pFUzbLePuuW54b18X8oA'
    inv_id = str(deal_id)
    shp_contactId=contact_id
    description = 'payment_info'
    crc =  hashlib.sha256((merchantLogin+':'+str(amount)+':'+str(inv_id)+':'+password).encode('utf-8')).hexdigest()
    return '''<a href="https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=%s&OutSum=%s&InvId=%s&Description=%s&SignatureValue=%s&IsTest=1">Ссылка на оплату</a>    
    '''%(merchantLogin, amount, inv_id, description, crc)



def test_crc():
    merchantLogin = 'MyRenter'
    password = 'pFUzbLePuuW54b18X8oA'
    inv_id = '1'
    summ = '100'
    Description = "Pay"
    crc =  hashlib.sha256((merchantLogin+':'+str(summ)+':'+str(inv_id)+':'+password).encode('utf-8')).hexdigest()
    # print(merchantLogin+':'+str(summ)+':'+str(inv_id)+':'+Description+':'+password)
    # print(crc)
    url = '''https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=%s&OutSum=%s&InvId=%s&Description=%s&SignatureValue=%s&IsTest=1    
    '''%(merchantLogin,summ,inv_id,Description, crc)
    # print(url)




if __name__ == '__main__':
    # test_crc()
    executor.start_polling(dp, skip_updates=True)


#https://auth.robokassa.ru/Merchant/Index.aspx?MerchantLogin=MyRenter&OutSum=15&Description=undefined&SignatureValue=d31a4f7020e66ec1b68316be699acecb503aa3dea06386715bd7445f8d5db200&Encoding=UTF-8&IsTest=1&Shp_productId=undefined&Shp_username=Vadim%20Kiselev