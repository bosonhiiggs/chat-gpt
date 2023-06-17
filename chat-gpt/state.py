from aiogram.dispatcher.filters.state import StatesGroup, State


class MainMenuStates(StatesGroup):
    """
    Описано главное меню и его возможности по навигации с помощью состояний

        - mein_menu - Главное меню
        - menu_point_1 - Первый пункт (echo)
        - menu_point_2 - Второй пункт (GPT chat model)
        - menu_point_3 - Второй пункт (GPT QA model)
        - menu_point_4 - Второй пункт (GPT генерация изображения)

    """

    main_menu = State()
    menu_point_1 = State()
    menu_point_2 = State()
    menu_point_3 = State()
    menu_point_4 = State()
