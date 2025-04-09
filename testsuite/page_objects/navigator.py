import abc
import inspect
from dataclasses import dataclass
from typing import Type, Callable

NAV_META = "nav_meta"
step_tree = {}


def step(cls, **kwargs):
    def decorator(method):
        setattr(method, NAV_META, cls)
        method._kwargs = kwargs
        return method

    return decorator


class Navigable:
    """"""

    def __init__(self, page):
        self.page = page

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        step_tree.update(
            {
                getattr(method, NAV_META): StepMetadata(cls, method)
                for _, method in inspect.getmembers(cls, inspect.isfunction)
                if method.__qualname__.split(".")[0] == cls.__name__ and hasattr(method, NAV_META)
            }
        )

    @abc.abstractmethod
    def is_displayed(self):
        """"""


@dataclass
class StepMetadata:
    cls: Type[Navigable]
    method: Callable


class Navigator:
    def __init__(self, page: Page):
        self.page = page
        self.path = []

    @staticmethod
    def _is_displayed(page):
        elements = page.is_displayed()
        if not isinstance(elements, tuple):
            elements = (elements,)

        is_displayed = True

        for element in elements:
            if not element.is_visible():
                is_displayed = False
                break
        return is_displayed

    def _construct_path(self, destination: Type[Navigable]):
        step_metadata = step_tree.get(destination)
        if step_metadata is None:
            return

        page_instance = step_metadata.cls(self.page)
        if self._is_displayed(page_instance):
            return
        bound_method = getattr(page_instance, step_metadata.method.__name__)
        self.path.append(bound_method)

        return self._construct_path(step_metadata.cls)

    def _run(self):
        for i in reversed(self.path):
            i()

    def navigate(self, dest_page: Type[Navigable]):
        self.path.clear()
        self._construct_path(dest_page)
        self._run()
        return dest_page(self.page)
