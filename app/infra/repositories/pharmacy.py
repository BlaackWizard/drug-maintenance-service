from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from ...domain.entities.pharmacy import PharmacyEntity


@dataclass
class BasePharmacyRepo(ABC):
    @abstractmethod
    async def check_pharmacy_exists_by_title(self, title: str):
        ...

    @abstractmethod
    async def add_pharmacy(self, pharmacy: PharmacyEntity):
        ...


@dataclass
class MemoryPharmacyRepo(BasePharmacyRepo):

    _saved_pharmacies: List[PharmacyEntity] = field(
        default_factory=list,
        kw_only=True,
    )

    async def check_pharmacy_exists_by_title(self, title: str):
        try:
            return bool(
                next(
                    pharmacy for pharmacy in self._saved_pharmacies if pharmacy.title.as_generic_type() == title
                ),
            )
        except StopIteration:
            return False

    async def add_pharmacy(self, pharmacy: PharmacyEntity):
        self._saved_pharmacies.append(pharmacy)
