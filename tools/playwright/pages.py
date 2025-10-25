import allure
from playwright.sync_api import Playwright, Page

from config import settings, Browser
from tools.playwright.mocks import mock_static_resources


def initialize_playwright_page(
        playwright: Playwright,
        test_name: str,
        browser_type: Browser,
        storage_state: str | None = None
) -> Page:
    browser = playwright[browser_type].launch(headless=settings.headless)
    # Создаем контекст для новой сессии браузера
    context = browser.new_context(
        base_url=settings.get_base_url(),
        storage_state=storage_state,
        record_video_dir=settings.videos_dir
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True) # Включаем трейсинг
    page = context.new_page()
    mock_static_resources(page) # Отключаем загрузку статических ресурсов

    yield page # Открываем новую страницу в контексте

    # В данном случае request.node.name содержит название текущего автотеста
    context.tracing.stop(path=settings.tracing_dir.joinpath(f'{test_name}.zip')) # Сохраняем трейсинг в файл
    browser.close()

    # Прикрепляем файл с трейсингом к Allure отчету
    allure.attach.file(settings.tracing_dir.joinpath(f'{test_name}.zip'), name='trace', extension='zip')
    # Прикрепляем видео автотеста к Allure отчету
    allure.attach.file(page.video.path(), name='video', attachment_type=allure.attachment_type.WEBM)
