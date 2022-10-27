# Поиск вакансий
import math
import maya
import requests
import pprint
from parserapp.models import Vacancy, Skills_table, Params

def hh_serch(tex, param, del_bd,user_serch,res):
    kol_vac=int(res)
    url = 'https://api.hh.ru/vacancies'
    if del_bd == 'delit':
        Params.objects.filter(user=user_serch).delete()
        Vacancy.objects.filter(user=user_serch).delete()
        Skills_table.objects.filter(user=user_serch).delete()

    if param == "name":
        ser = 'В названии вакансии '
    elif param == "company_name":
        ser = 'В названии компании'
    elif param == "description":
        ser ='В описание'

    params = {
        'text': tex,
        'search_field': param,
        'area': 1,
    }

    Params.objects.create(name_search=tex, where_search=ser,user=user_serch)
    result = requests.get(url, params=params).json()

    if kol_vac <= result['found']:
        kol = math.ceil(kol_vac/20)
    else:
        kol = math.ceil(result['found']/20)

    for i in range(kol):

        params = {
            'text': tex,
            'search_field': param,
            'page': i,
            'area': 1,
        }

        result = requests.get(url, params=params).json()
        # pprint.pprint(result)
        if (i + 1)*20 > kol_vac:
            iter = kol_vac-i*20
        else:
            iter = 20
        for z in range(iter):
            try:

                if result['items'][z]['salary']:
                    if result['items'][z]['salary']['from'] :

                        zp1 = 'от ' + str(result['items'][z]['salary']['from'])
                    else:
                        zp1 = ''
                    if result['items'][z]['salary']['to']:
                       zp2 = ' до ' + str(result['items'][z]['salary']['to'])
                    else:
                        zp2 = ''
                    zp = zp1 + zp2 + ' ' + result['items'][z]['salary']['currency']
                else:
                    zp = 'Не указана'

                ab = result['items'][z]['snippet']['responsibility'].replace('<highlighttext>', '')
                ab = ab.replace('</highlighttext>','')

                date_of = maya.parse(result['items'][z]['published_at']).datetime(to_timezone='Europe/Moscow', naive=False)
                # date_pub = " ".join(['Дата публикации',str(date_of.date()),'в', str(date_of.time()),'по МСК'])

                vac = Vacancy.objects.create(name=result['items'][z]['name'], salary=zp,
                                       about=ab,
                                       link=result['items'][z]['alternate_url'],user=user_serch,
                                       date_publik=date_of.date(),date_time=date_of.time())

                for skills_vac in requests.get(result['items'][z]['url']).json()['key_skills']:
                    skill_vacancy = skills_vac['name']
                    skill_vacancy=skill_vacancy.replace('/', ' ')
                    vac.skils.create(skil=skill_vacancy,user=user_serch)

            except:
                pass

