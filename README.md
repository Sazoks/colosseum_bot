# colosseum_bot
Бот для автоматического добавления билетов в Колизей в корзину.

## Детали проекта
- Проект разрабатывался на коммерческой основе на сайте FL.ru
- Цена: 5000р
- Сроки: 5 дней
- Страница для парсинга: https://clck.ru/rgdp9

## Алгоритм работы бота
1. Пользователь указывает нужную дату, время, количество билетов и параметр, отвечающий за автообход капчи.
2. После этого пользователь запускает бота, нажимая кнопку "Начать мониторинг".
3. После запуска бот создает отдельный процесс с помощью модуля multiprocessing и начинает мониторинг наличия билетов.
4. Каждые 1-3 минуты бот проверяет в указнной дате и времени наличие билетов. Если они есть, бот начинает процесс добавления билетов в корзину, попутно обходя капчу, если она есть и если был указан соответствующий параметр.
