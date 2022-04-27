from bs4 import BeautifulSoup
import aiohttp



class Network:
    SITE_URL = 'https://74.ru/horoscope/daily/'

    async def _get_page(self):
        async with aiohttp.ClientSession() as client:
            async with client.get(url=self.SITE_URL) as response:
                return(await response.text())


class Manager:
    def __init__(self):
        self.network = Network()

    async def __find_horoscope(self, id: int) -> str:
        html = await self.network._get_page()
        page = BeautifulSoup(html, 'lxml')

        articles = page.find('section', class_='JTS1e').find_all('article')
        card_description = articles[id].find('div', class_='_2j-zP _1ylC5').text.strip()
        return(card_description)

    
    async def __call__(self, horoscope_id: int) -> str:
        site_response = await self.__find_horoscope(horoscope_id)
        return(site_response)
