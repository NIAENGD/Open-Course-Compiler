from __future__ import annotations

from app.providers.base import CourseProvider
from app.providers.mit_ocw import MitOcwProvider
from app.providers.open_yale import OpenYaleProvider

_PROVIDERS: dict[str, CourseProvider] = {
    MitOcwProvider.provider_id: MitOcwProvider(),
    OpenYaleProvider.provider_id: OpenYaleProvider(),
}


def get_provider(provider_id: str) -> CourseProvider:
    return _PROVIDERS[provider_id]


def list_providers() -> list[CourseProvider]:
    return list(_PROVIDERS.values())
