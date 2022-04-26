from configparser import ConfigParser
from loguru import logger







class Core:

    def __init__(self, path: str):
        self.path = path
        self.sections = self.__initialization
        attrbs = self.__get_sections_dictonary


    @property
    def __initialization(self):
        """
        Читает конфиг и инициализирует его
        Создает динамические объекты на основе конфига
        """

        self.config = ConfigParser()
        self.config.read(self.path)

        #Создание динамического объекта, для всех секций конфига
        sections = type('Sections', (), {})

        #Цикл for по всем секциям в конфиге
        for section in self.config:

            #Создание динамического объекта для секции(текущей итерации) 
            #в который будут помещены атрибуты данной секции
            parametrs = type('Parametrs', (), {})

            #Добавлении в объект секций, объект в который будут помещены атрибуты секции
            #Атрибут будет иметь имя идентичное названию секции
            setattr(sections, section, parametrs)
            #Цикл for по параметрам секции
            for key in self.config[section]:

                #Создание нового атрибута в объекте который будет содержать в себе все атрибуты
                #и значения из секции конфига
                value = int(self.config[section][key]) if self.config[section][key].isdigit() else self.config[section][key]
                setattr(parametrs, key, value)
        logger.info('Конфиг успешно инициализирован')
        return(sections)


    @property
    def __get_sections_dictonary(self):
        """
        Возвращает список секций и ее атрибуты в виде {section_name: [attr1, attr2]}

        section[0] - Название секции
        section[1] - Ссылка на объект секции
        param[0] - Название атрибута
        param[1] - Ссылка на объект атрибута
        """
        sections_dict = {
            section[0]: [
                param[0] for param in getattr(section[1], '__dict__').items() if not param[0].startswith('_')
            ] for section in self.sections.__dict__.items() if not section[0].startswith('_')
        }
        return(sections_dict)

