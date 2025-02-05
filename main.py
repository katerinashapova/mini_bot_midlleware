#основной исполняемый файл - точка входа в бот
import asyncio
import logging
from aiogram.fsm.state import StatesGroup
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers.other import other_router
from handlers.user import user_router
from middlewares.inner import (
    FirstInnerMiddleware,
    SecondInnerMiddleware,
    ThirdInnerMiddleware,
)
from middlewares.outer import (
    FirstOuterMiddleware,
    SecondOuterMiddleware,
    ThirdOuterMiddleware,
)

from middlewares.i18n import TranslatorMiddleware

from lexicon.lexicon_ru import LEXICON_RU
from lexicon.lexicon_en import LEXICON_EN

# Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)

translations = {
    'default': 'ru',
    'en': LEXICON_EN,
    'ru': LEXICON_RU,

}
# Функция конфигурирования и запуска бота
async def main() -> None:

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()



    # Регистриуем роутеры в диспетчере
    dp.include_router(user_router)
    dp.include_router(other_router)

    # Здесь будем регистрировать миддлвари
    dp.update.outer_middleware(FirstOuterMiddleware())
    #user_router.callback_query.outer_middleware(SecondOuterMiddleware())
    #other_router.message.outer_middleware(ThirdOuterMiddleware())
    #user_router.message.middleware(SecondInnerMiddleware())
    #user_router.callback_query.middleware(SecondInnerMiddleware())
    #other_router.message.middleware(ThirdInnerMiddleware())
    dp.update.middleware(TranslatorMiddleware())

    # Запускаем polling
    await dp.start_polling(bot, _translations = translations)


asyncio.run(main())