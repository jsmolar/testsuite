"""Module containing base classes for common objects"""
import abc
from dataclasses import dataclass, is_dataclass, fields, field
from copy import deepcopy
from typing import Literal, Optional

JSONValues = None | str | int | bool | list["JSONValues"] | dict[str, "JSONValues"]

# pylint: disable=invalid-name


def asdict(obj) -> dict[str, JSONValues]:
    """
    This function converts dataclass object to dictionary.
    While it works similar to `dataclasses.asdict` a notable change is usage of
    overriding `asdict()` function if dataclass contains it.
    This function works recursively in lists, tuples and dicts. All other values are passed to copy.deepcopy function.
    """
    if not is_dataclass(obj):
        raise TypeError("asdict() should be called on dataclass instances")
    return _asdict_recurse(obj)


def _asdict_recurse(obj):
    if hasattr(obj, "asdict"):
        return obj.asdict()

    if not is_dataclass(obj):
        return deepcopy(obj)

    result = {}
    for field in fields(obj):
        value = getattr(obj, field.name)
        if value is None:
            continue  # do not include None values

        if is_dataclass(value):
            result[field.name] = _asdict_recurse(value)
        elif isinstance(value, (list, tuple)):
            result[field.name] = type(value)(_asdict_recurse(i) for i in value)
        elif isinstance(value, dict):
            result[field.name] = type(value)((_asdict_recurse(k), _asdict_recurse(v)) for k, v in value.items())
        else:
            result[field.name] = deepcopy(value)
    return result


@dataclass
class MatchExpression:
    """
    Data class intended for defining K8 Label Selector expressions.
    Used by selector.matchExpressions API key identity.
    """

    operator: Literal["In", "NotIn", "Exists", "DoesNotExist"]
    values: list[str]
    key: str = "group"


@dataclass
class Selector:
    """Dataclass for specifying selectors based on either expression or labels"""

    matchExpressions: Optional[list[MatchExpression]] = field(default=None, kw_only=True)
    matchLabels: Optional[dict[str, str]] = field(default=None, kw_only=True)

    def __post_init__(self):
        if not (self.matchLabels is None) ^ (self.matchExpressions is None):
            raise AttributeError("`matchLabels` xor `matchExpressions` argument must be used")


@dataclass
class Credentials:
    """Dataclass for Credentials structure"""

    in_location: Literal["authorizationHeader", "customHeader", "queryString", "cookie"]
    keySelector: str

    def asdict(self):
        """Custom asdict because of needing to put location as parent dict key for inner dict"""
        if self.in_location == "authorizationHeader":
            return {self.in_location: {"prefix": self.keySelector}}
        return {self.in_location: {"name": self.keySelector}}


@dataclass
class Rule:
    """
    Data class for rules represented by simple pattern-matching expressions.
    Args:
        :param selector: that is fetched from the Authorization JSON
        :param operator: `eq` (equals), `neq` (not equal), `incl` (includes) and `excl` (excludes), for arrays
                         `matches`, for regular expressions
        :param value: a fixed comparable value
    """

    selector: str
    operator: Literal["eq", "neq", "incl", "excl", "matches"]
    value: str


@dataclass
class ABCValue(abc.ABC):
    """
    Abstract Dataclass for specifying a Value in Authorization,
    can be either static or reference to value in AuthJson.
    """


@dataclass
class Value(ABCValue):
    """Dataclass for static Value. Can be any value allowed in JSON: None, string, integer, bool, list, dict"""

    value: JSONValues


@dataclass
class ValueFrom(ABCValue):
    """Dataclass for dynamic Value. It contains reference path to existing value in AuthJson."""

    selector: str


@dataclass
class Cache:
    """Dataclass for specifying Cache in Authorization"""

    ttl: int
    key: ABCValue


@dataclass
class PatternRef:
    """Dataclass for specifying Pattern reference in Authorization"""

    patternRef: str


class LifecycleObject(abc.ABC):
    """Any objects which has its lifecycle controlled by create() and delete() methods"""

    @abc.abstractmethod
    def commit(self):
        """Commits resource.
        if there is some reconciliation needed, the method should wait until it is all reconciled"""

    @abc.abstractmethod
    def delete(self):
        """Removes resource,
        if there is some reconciliation needed, the method should wait until it is all reconciled"""


class Authorino(LifecycleObject):
    """Authorino instance"""

    @abc.abstractmethod
    def wait_for_ready(self):
        """True, if after some waiting the Authorino is ready"""

    @property
    @abc.abstractmethod
    def metrics_service(self):
        """Authorino metrics service name"""

    @property
    @abc.abstractmethod
    def authorization_url(self):
        """Authorization URL that can be plugged into envoy"""

    @property
    @abc.abstractmethod
    def oidc_url(self):
        """Authorino oidc url"""


class PreexistingAuthorino(Authorino):
    """Authorino which is already deployed prior to the testrun"""

    def __init__(self, authorization_url, oidc_url, metrics_service) -> None:
        super().__init__()
        self._authorization_url = authorization_url
        self._oidc_url = oidc_url
        self._metrics_service = metrics_service

    def wait_for_ready(self):
        return True

    @property
    def metrics_service(self):
        return self._metrics_service

    @property
    def authorization_url(self):
        return self._authorization_url

    @property
    def oidc_url(self):
        return self._oidc_url

    def commit(self):
        return

    def delete(self):
        return
