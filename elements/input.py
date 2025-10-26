import allure
from playwright.sync_api import Locator, expect
from ui_coverage_tool import ActionType

from elements.base_element import BaseElement
from tools.logger import get_logger

logger = get_logger("INPUT")


class Input(BaseElement):
    @property
    def type_of(self) -> str:
        return "input"

    def get_locator(self, nth: int = 0, **kwargs) -> Locator:
        return super().get_locator(nth, **kwargs).locator('input')

    def get_raw_locator(self, nth: int = 0, **kwargs) -> str:
        # Переопределяем метод формирования XPath-селектора:
        #  - сначала получаем общий селектор блока
        #  - затем уточняем путь до самого <input>, добавляя '//input'
        # Это нужно, чтобы трекер точно знал, с каким элементом шло взаимодействие.
        return f'{super().get_raw_locator(**kwargs)}//input'

    def fill(self, value: str, nth: int = 0, **kwargs):
        step = f'Fill {self.type_of} "{self.name}" to value "{value}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            locator.fill(value)

        # После успешного fill фиксируем покрытие как действие FILL
        self.track_coverage(ActionType.FILL, nth, **kwargs)

    def check_have_value(self, value: str, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" has a value "{value}"'

        with allure.step(step):
            locator = self.get_locator(nth, **kwargs)
            logger.info(step)
            expect(locator).to_have_value(value)

        # Фиксируем в покрытии, что значение проверено — тип VALUE
        self.track_coverage(ActionType.VALUE, nth, **kwargs)
