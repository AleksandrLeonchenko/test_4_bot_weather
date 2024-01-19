from django.http import HttpResponse, HttpRequest

from .bot import stop_flag, start_polling, stop_polling, bot


def start_bot(request: HttpRequest) -> HttpResponse:
    """
    Запускает бота, если он еще не запущен.

    :param request: Объект запроса.
    :return: Ответ с сообщением о статусе запуска бота.
    """
    if not stop_flag.is_set():
        start_polling()
        stop_flag.clear()
        return HttpResponse("Бот запущен!")
    else:
        return HttpResponse("Бот уже работает!")


def stop_bot(request: HttpRequest) -> HttpResponse:
    """
    Останавливает бота, если он запущен.

    :param request: Объект запроса.
    :return: Ответ с сообщением о статусе остановки бота.
    """
    if not stop_flag.is_set():
        stop_polling()
        return HttpResponse("Бот остановлен!")
    else:
        return HttpResponse("Бот не запущен!")

