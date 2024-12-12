import requests
from bs4 import BeautifulSoup
try:
    import lxml
    from lxml import etree
    USE_LXMLS = True
except ImportError:
    USE_LXMLS = False
import re
import SteamParser.errors as error

class SteamParser:
    def __init__(self,USE_LXML:bool = False):
        if USE_LXML == False:
            self.USE_LXML = 'html.parser'
        elif USE_LXML == True:
            if USE_LXMLS == True:
                self.USE_LXML = 'lxml'
            else:
                raise ImportWarning('Параметр use_lxml установлен в true, однако при попытке импорта lxml произошла ошибка')
        else: 
            raise error.USE_LXML_ERROR('Вы пытаетесь устоновить недопустимое значение')

    def get_bundle_info(self,link:str) -> dict:
        '''
        example = ('https://store.steampowered.com/bundle/34206/Remnant_Ultimate_Bundle/')
        возращает словарь в виде:
        {
            'bundle_name': 'Remnant Ultimate Bundle',
            'bundle_price': 4908.62,
            'description': 'НАБОР ULTIMATE\r\nСоберите коллекцию REMNANT! НАБОР ULTIMATE включает в себя REMNANT: FROM THE ASHES — ПОЛНОЕ ИЗДАНИЕ и REMNANT II® — ИЗДАНИЕ ULTIMATE.\n\r\nREMNANT: FROM THE ASHES — ПОЛНОЕ ИЗДАНИЕ\r\nRemnant: From the Ashes — динамичный шутер от третьего лица, где вам предстоит стать одним из последних выживших в постапокалиптическом мире, полном чудовищ. В одиночку или вместе с двумя другими игроками вы отправитесь в путешествие, чтобы сразиться с эпическими боссами и полчищами смертоносных врагов, защитить Землю и вернуть человечеству утраченное.\r\nСостав полного издания Remnant: From the Ashes:\r\nRemnant: From the Ashes\r\nRemnant: From the Ashes — дополнение Swamps of Corsus\r\nRemnant: From the Ashes — дополнение Subject 2923\n\r\nПолучите в своё распоряжение все приключения Remnant: From the Ashes. Отправьтесь в путешествие по постапокалиптическому миру в одиночку или в компании двух других игроков. Сражайтесь с эпическими боссами и полчищами смертоносных врагов, чтобы возродить человечество.\n\r\nВ дополнении Swamps of Corsus вы отправитесь в покрытый болотами мир Корсус, где узнаете историю культа Искал. Вы также сможете проверить свои силы в режиме выживания с элементами жанра roguelike: начав путь с одним только пистолетом и горстью лома, вы должны будете как можно дольше противостоять напору врагов и боссов, силы которых постоянно растут.\n\r\nДополнение Subject 2923 продолжает сюжет Remnant: From the Ashes. В новой кампании вам предстоит побывать в неизведанных местах, встретить неожиданных 
            союзников и бросить вызов новым врагам, чтобы раз и навсегда покончить с Корнем.\n\r\nREMNANT\xa0II®\r\nRemnant II® — продолжение крайне успешной игры Remnant: From the Ashes. Выжившим представителям человечества предстоит отправиться в жуткие миры и вступить в бой с новыми беспощадными тварями и богоподобными боссами. Исследуйте глубины неизведанного в одиночку или вместе с друзьями и помешайте злу разрушить реальность. Чтобы не допустить истребления человечества, игрокам придется пройти сложнейшие испытания, полагаясь на собственные навыки и помощь друзей.\n\r\nВ ИЗДАНИЕ ULTIMATE входят REMNANT II®, ТРИ КОМПЛЕКТА БРОНИ ИЗ\xa0REMNANT:\xa0FROM\xa0THE\xa0ASHES, КОМПЛЕКТ ДЛЯ ВЫЖИВАНИЯ и НАБОР ИЗ ТРЁХ ДОПОЛНЕНИЙ.',
            'in_bundle': ['https://store.steampowered.com/app/1282100/REMNANT_II/?snr=1_430_4__431', 'https://store.steampowered.com/app/617290/Remnant_From_the_Ashes/?snr=1_430_4__431', 'https://store.steampowered.com/app/1245150/Remnant_From_the_Ashes__Swamps_of_Corsus/?snr=1_430_4__431', 'https://store.steampowered.com/app/1344680/Remnant_From_the_Ashes__Subject_2923/?snr=1_430_4__431']}
        }
        '''
        cookies = {
            'birthtime': '606063601',
            'lastagecheckage': '17-March-1979',
        }
        headers = {
            'Accept-Language': 'ru,en;q=0.9'
        }
        
        responce = requests.get(link,headers=headers,cookies=cookies)
        responce.raise_for_status()
        soup = BeautifulSoup(responce.text,self.USE_LXML)
        
        page_name = soup.find('h2',class_="pageheader").text
        game_price = float(soup.find('div',class_="discount_final_price").text[:-1].replace(',','.').replace(' руб',''))
        description = soup.find('p').text
        in_packs = [i['href'] for i in soup.find_all(class_="tab_item_overlay")]
        
        return {
            'bundle_name':page_name,
            'bundle_price':game_price,
            'description':description,
            'in_bundle':in_packs
        }
        
    def get_app_info(self,link:str,strict_regime = True) -> dict:
        full_desc = False
        ''' 
        link: example('https://store.steampowered.com/app/431960/Wallpaper_Engine/')
        
        возрощает список в виде ->
        
        {
            name:'Wallpaper Engine'
            
            price: 249.0
            
            description:'Устанавливайте шикарные живые обои на рабочий стол. Анимируйте собственные изображения для создания новых обоев или импортируйте видео/веб-сайты и делитесь ими в Мастерской Steam!'
            
            
            minimal_option:
            
            
            {
                ОС: Windows 10, Windows 11
                Процессор: 1.66 GHz Intel i5 or equivalent
                Оперативная память: 1024 MB ОЗУ
                Видеокарта: HD Graphics 4000 or above     
                DirectX: версии 11
                Место на диске: 512 MB
                
            }
            
            
            recomendation_option:
            
            {
                ОС: Windows 10, Windows 11
                Процессор: 2.0 GHz Intel i7 or equivalent
                Оперативная память: 2048 MB ОЗУ
                Видеокарта: NVIDIA GeForce GTX 660, AMD HD7870, 2 GB VRAM or above
                DirectX: версии 11
                Место на диске: 1024 MB
            }
            
            
            source:
            
            {
                images = 
                
                [
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_d9190a12d54e0d7d5b213bed1ae8f2a9112c8cd1.1920x1080.jpg?t=1733409718,
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_39ed0a9730b67a930acb8ceed221cc968bee7731.1920x1080.jpg?t=1733409718,
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_526b8ec8fbf77cbba08ab320304b23262b61c636.1920x1080.jpg?t=1733409718,
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_c63a5b855bf66be02b7d1c167987f7cf2a38870a.1920x1080.jpg?t=1733409718,
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_6db665650ff05359aeb0f7e31252075e37705054.1920x1080.jpg?t=1733409718,
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_4de8564700e99ba7ecac2794127cc85ceba63778.1920x1080.jpg?t=1733409718,
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_0abd29c8ef88347b4ccf263475c9124663248937.1920x1080.jpg?t=1733409718,
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_a57cba85acf4d5b27f9db75e5303b9b07e6e5daa.1920x1080.jpg?t=1733409718,
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_2b31c6305d1b3cc1ee4a62f835f741005ab7bab6.1920x1080.jpg?t=1733409718,
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_03355afd883aa905003bc11f6ad9427cf9f33297.1920x1080.jpg?t=1733409718,
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_7a8b38d3cd0cf0129d845c7d1a8afa86c2b45ea5.1920x1080.jpg?t=1733409718,
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_dcc02834621a8871ba951ff56ee3e76aa9280e2f.1920x1080.jpg?t=1733409718,
                    https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/431960/ss_6fb1c2f1bfcb140dc506d017ef0c6f9ba1853d34.1920x1080.jpg?t=1733409718    
                ]
                
                videos = 
                
                [
                    
                    https://video.fastly.steamstatic.com/store_trailers/256735610/movie_max.mp4
                
                ]
            
            }
        
        }
        '''
        
        headers = {
            'Accept-Language': 'ru,en;q=0.9'
        }
        self.check()
        data = {}
        responce = requests.get(link,headers=headers)
        responce.raise_for_status()
        soup = BeautifulSoup(responce.text,self.USE_LXML)
        
        # находит название игры
        try:
            game_name = soup.find(class_="apphub_AppName").text
        except AttributeError:
            game_name = None
        if not game_name:
            try:
                game_name = soup.find(class_="apphub_AppName").text
            except AttributeError:
                game_name = None
            if not game_name:
                if strict_regime == True:
                    raise error.DONT_FIND_INFO('Не найден атрибут name')
                else: name = None
            else:
                name = soup.find(class_="appHubAppName").text
        else:
            name = soup.find(class_= "apphub_AppName" ).text
            
        # находит цену
        if soup.find('div',class_="game_purchase_action"):
            match = re.search(r'data-price-final="(\d+)"',str(soup.find('div',class_="game_purchase_action")))
            if soup.find('div',class_="game_purchase_price price"):
                match = re.search(r'data-price-final="(\d+)"',str(soup.find('div',class_="game_purchase_action")))
            if match:
                price = int(match.group(1)) / 100
            elif soup.find(class_="game_purchase_price price"):
                    price = soup.find(class_="game_purchase_price price").text.strip()
            else:
                if strict_regime == True:
                    raise error.DONT_FIND_INFO('Не найден атрибут price')
                else: price = None
        else:
            if strict_regime == True:
                raise error.DONT_FIND_INFO('Не найден атрибут price')
            else: price = None
        
        # находит описание игры
        if soup.find(class_="game_description_snippet"):
            description = str(soup.find(class_="game_description_snippet").text.strip())
            if not description:
                if strict_regime == True:
                    raise error.DONT_FIND_INFO('Не найден атрибут description')
                else: description = None
        elif soup.find(class_="glance_details").text:
            description = soup.find(class_="glance_details").text.strip()
            if not description:
                if strict_regime == True:
                    raise error.DONT_FIND_INFO('Не найден атрибут description')
                else: description = None
        else:
            if strict_regime == True:
                raise error.DONT_FIND_INFO('Не найден атрибут description')
            else: description = None
        
        
        if soup.find(class_="game_area_sys_req_full"):
            minimal_option = soup.find(class_="game_area_sys_req_full")
            html_code = minimal_option.find(class_="bb_ul")
            if not html_code:
                if strict_regime == True:
                    raise error.DONT_FIND_INFO('Не найден атрибут option')
                else: full_option = None
            matches = re.findall(r'<li><strong>(.*?)</strong>\s*([^<]*)<br\s*/?>', str(html_code))
            full_option = {key.strip(':'): value.strip() for key, value in matches}
            full_desc = True
            if not minimal_option: 
                if strict_regime == True:
                    raise error.DONT_FIND_INFO('Не найден атрибут option')
                else: full_option = None
            
            
        if soup.find(class_="game_area_sys_req_leftCol"):
            minimal_option = soup.find(class_="game_area_sys_req_leftCol")
            html_code = minimal_option.find(class_="bb_ul")
            if not html_code: 
                if strict_regime == True:
                    raise error.DONT_FIND_INFO('Не найден атрибут option')
                else: minimal_option = None
            matches = re.findall(r'<li><strong>(.*?)</strong>\s*([^<]*)<br\s*/?>', str(html_code))
            minimal_option = {key.strip(':'): value.strip() for key, value in matches}
            if not minimal_option: 
                if strict_regime == True:
                    raise error.DONT_FIND_INFO('Не найден атрибут option')
                else:
                    minimal_option = None
        
        if soup.find(class_="game_area_sys_req_rightCol"):
            recomendation_option = soup.find(class_="game_area_sys_req_rightCol")
            html_code = recomendation_option.find(class_="bb_ul")
            if not html_code: 
                if strict_regime == True:
                    raise error.DONT_FIND_INFO('Не найден атрибут option')
                else:
                    recomendation_option = None
            matches = re.findall(r'<li><strong>(.*?)</strong>\s*([^<]*)<br\s*/?>', str(html_code))
            recomendation_option = {key.strip(':'): value.strip() for key, value in matches}
            if not recomendation_option: 
                if strict_regime == True:
                    raise error.DONT_FIND_INFO('Не найден атрибут option')
                else:
                    recomendation_option = None
        
        # находит фото,видео трейлера ссылки
        if soup.find(id="highlight_player_area"):
            image = []
            html_code = soup.find(id="highlight_player_area")
            videos:list = re.findall(r'https?://[^\s\'"<>]+/store_trailers/[^\s\'"<>]+/movie_max/*\.mp4', str(html_code))
            if not videos:
                videos = [None]
                    
            images = html_code.find_all(class_="screenshot_holder")
            if not images:
                if strict_regime == True:
                    raise error.DONT_FIND_INFO('Не найден атрибут Photo')
                else:
                    images = None
            for img in images:
                image.append(img.find('a')['href'])
        sourse = {
            'images':image,
            'videos':videos
        }        
        data['name'] = name
        data['price'] = price
        data['description'] = description
        if full_desc != True:
            data['minimal_option'] = minimal_option
            data['recomendation_option'] = recomendation_option
        else:data['option'] = full_option
        data['source'] =sourse
        return data
        
    def find_game(self,pattern:str,supportedlang='russian',page_start = 0) -> dict:
        
        '''
        выбирайте между этими языками:
         
        [
            
        russian,romanian,schinese,tchinese,
        
        japanese,koreana,bulgarian,thai,
        
        czech,danish,german,english,spanish,
        
        latam,greek,french
        
        ]
        
        Возращает вот такой список
        
        {
            game_name:url,
            game_name:url,
            game_name:url,
        }
        '''
        data = {}
        headers = {
            'Accept-Language': 'ru,en;q=0.9'
        }
        if supportedlang:
            if isinstance(supportedlang, list):
                tmp = ''
                for i in supportedlang:
                    tmp = tmp + i + ','
                supportedlang = tmp
            elif isinstance(supportedlang, str):pass
            else:
                raise TypeError('В аргумент вошло какое либо из этх значений dict,int')
            response = requests.get(f'https://store.steampowered.com/search/results/?query&start={str(page_start)}&count=100&dynamic_data=&sort_by=_ASC&term={pattern.replace(' ','%20')}&snr=1_7_7_151_7&infinite=1&supportedlang={supportedlang}',headers=headers)
            response.raise_for_status()
            js = response.json()
            soup = BeautifulSoup(js['results_html'],self.USE_LXML)
            all_game = soup.find_all('a')
            for game in all_game: 
                data[game.find('span').text] = game['href']
        
        else:
            response = requests.get(f'https://store.steampowered.com/search/results/?query&start=0&count=5000&dynamic_data=&sort_by=_ASC&term={pattern.replace(' ','%20')}&snr=1_7_7_151_7&infinite=1',headers=headers)
            response.raise_for_status()
            js = response.json()
            soup = BeautifulSoup(js['results_html'],self.USE_LXML)
            all_game = soup.find_all('a')
            for game in all_game: 
                data[game.find('span').text] = game['href']
        
        return data
        
    def get_game_id(self,link:str) -> int:
        id = ''
        for i in link:
            try:
                int(i)
                id += str(i)
            except ValueError:
                if id: break
                continue
        return(int(id))
        
    def get_account_info(self,link:str) -> dict:
        '''
        Возращает список в виде ->
            example = (https://steamcommunity.com/id/55562515522211125410)
        {   
            steamID:76561199180091312
            name:allanchik
            description:thanks for buying :)
            other_name:
            [
                {'newname': 'allanchik', 'timechanged': '24 ноя в 6:46'}
                {'newname': 'misipi', 'timechanged': '24 ноя в 6:00'}
                {'newname': 'Seven', 'timechanged': '25 окт в 10:06'}
                {'newname': 'frost', 'timechanged': '8 окт в 7:13'}
            ]
            avatarFull: https://avatars.fastly.steamstatic.com/83048dc27b9ecbe0fbc9a02397881f1546bb66e8_full.jpg
            vacBanned: 0
            onlineState: In-Game/Soundpad
            date_reg: June 13, 2021
            
            
        }
        '''
        if USE_LXMLS == True:
            headers = {
                'Accept-Language': 'ru,en;q=0.9'
            }
            
            other_names = requests.get(link + '/ajaxaliases/',headers=headers)
            other_names = other_names.json()

            lxml_code = requests.get(link + '?xml=1').text
            tree = etree.fromstring(text=lxml_code.encode())

            steamID64 = tree.findtext('steamID64')
            steamID = tree.findtext('steamID')
            summary = tree.findtext('summary')
            avatarFull = tree.findtext('avatarFull')
            vacBanned = tree.findtext('vacBanned')
            date_reg = tree.findtext('memberSince')
            onlineState = tree.findtext('stateMessage')
            description = re.sub(r'<img[^>]*>', '', summary)
            onlineState = onlineState.replace('<br/>','/')
            
            data = {   
                'steamID':steamID64,
                'name':steamID,
                'description':description,
                'other_name': other_names,
                'avatarFull': avatarFull,
                'vacBanned': vacBanned,
                'onlineState': onlineState,
                'date_reg': date_reg         
                }
            return data
        else:
            raise error.USE_LXML_ERROR(f"Не удалось импортировать модуль 'lxml'. Проверьте, установлен ли он и правильно ли указано имя.")

    def check(self,url) -> str:
        if re.search(r'/bundle/', url):
            return 'bundle'
        elif re.search(r'/app/', url):
            return 'app'