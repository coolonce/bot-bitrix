from os import truncate
from bitrix24 import *
bx24 = Bitrix24('https://property.bitrix24.ru/rest/2955/0uxepsze4xzwu3vk/')

def find_company_by_name(name):
    result = bx24.callMethod('crm.company.list', filter={'TITLE': name})
    if len(result) > 0:
        # c_id = result[0]['ID']
        # print(c_id)
        # print(get_company_info_by_id(c_id))
        return result[0]['ID']
    else:
        return -1

def get_company_info_by_id(c_id):
    result = bx24.callMethod('crm.company.get/?id='+str(c_id))    
    if len(result) > 0:
        return result
    else:
        return -1

def find_companyId_by_name(name):
    return find_company_by_name(name)

def find_contact(first_name, last_name, chat_id):
    result =  bx24.callMethod('crm.contact.list', filter={'TITLE': chat_id, 'NAME': first_name, 'LAST_NAME': last_name});
    if len(result) > 0:
        return result[0]['ID']
    else:
        return -1

def get_contact_id(first_name, last_name, chat_id):
    contact_id = find_contact(first_name, last_name,chat_id)
    if not contact_id == -1 or not contact_id is None:
        return contact_id
    else:
        create_contact(first_name, last_name, chat_id)
        return find_contact(first_name, last_name, chat_id)

def create_contact(first_name, last_name, chat_id):
    try:
        bx24.callMethod('crm.contact.add', fields={'TITLE': chat_id, 'NAME': first_name, 'LAST_NAME': last_name})
        return True
    except:
        return False
    

def create_deal_for_contract(contact_id, chat_id, amount, company_id):
    info = create_company_info(company_id)
    try:
        deal = bx24.callMethod('crm.deal.add', fields={
              "TITLE": 'Касса_Оплата_Информации:'+str(chat_id),
              "CONTACT_ID": contact_id,
              "COMMENTS": info,
              "OPPORTUNITY": amount
          })
        print(deal)
        return True
    except:
        return False

def get_deal_by_chat_id(chat_id, contact_id):
    result = bx24.callMethod('crm.deal.list',order={'ID': 'DESC'},filter={'TITLE': 'Касса_Оплата_Информации:'+str(chat_id)})    
    if len(result) > 0:
        return bx24.callMethod('crm.deal.get/?id='+str(result[0]['ID']))['ID']
    else:
        return -1

def create_company_info(company_id):
    company = get_company_info_by_id(company_id)

    fields = ['UF_CRM_1572363633722', 'UF_CRM_5DB9353B0228A', 'HAS_PHONE', 'HAS_EMAIL','WEB']

    msg = {
        'title': company['TITLE'],
        'phone': "Не заполнено",
        'email': "Не заполнено",
        'web': "Не заполнено",
        'kvt': "Не заполнено",
        'adressObject': "Не заполнено"
    }

    for field in fields:
        if field in company and field == 'UF_CRM_1572363633722':
            msg['kvt'] = company[field]
        if field in company and field == 'UF_CRM_5DB9353B0228A':
            msg['adressObject'] = company[field]
        if field in company and field == 'HAS_PHONE' and company[field] == 'Y':
            msg['phone'] = ''
            for phone in company['PHONE']:
                msg['phone'] += phone['VALUE']+', '
        if field in company and field == 'HAS_EMAIL' and company[field] == 'Y':
            msg['email'] = ''
            for email in company['EMAIL']:
                msg['email'] += email['VALUE']+', '
        if field in company and field == 'HAS_WEB':
            msg['web'] = ''
            for web in company['WEB']:
                msg['web'] += web['VALUE']+', '
    return '''\nНазвание компании: %s\nТелефон: %s\nE-mail: %s\nСайт: %s\nАдрес Объекта:%s\nкВт: %s
    '''% (msg['title'], msg['phone'], msg['email'], msg['web'], msg['adressObject'], msg['kvt'])
