from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.catalog.repository import get_course, list_courses
from app.catalog.service import provider_descriptors, refresh_catalog
from app.db.session import connect
from app.schemas.provider import (
    CatalogRefreshRequest,
    CatalogRefreshSummary,
    CatalogSearchFilters,
    CatalogCourse,
    ProviderDescriptor,
)

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/providers", response_model=list[ProviderDescriptor])
def providers() -> list[ProviderDescriptor]:
    return provider_descriptors()


@router.post("/refresh", response_model=CatalogRefreshSummary)
async def refresh(request: CatalogRefreshRequest) -> CatalogRefreshSummary:
    return await refresh_catalog(request)


@router.get("/courses", response_model=list[CatalogCourse])
def courses(
    q: str | None = None,
    provider: str | None = None,
    department: str | None = None,
    topic: str | None = None,
    mode: str | None = None,
    min_teachability_score: float | None = None,
    license: str | None = Query(default=None),
) -> list[CatalogCourse]:
    filters = CatalogSearchFilters(
        q=q,
        provider=provider,
        department=department,
        topic=topic,
        mode=mode,
        min_teachability_score=min_teachability_score,
        license=license,
    )
    with connect() as conn:
        conn.row_factory = __import__("sqlite3").Row
        return list_courses(conn, filters)


@router.get("/search", response_model=list[CatalogCourse])
def search(q: str, provider: str | None = None, mode: str | None = None) -> list[CatalogCourse]:
    with connect() as conn:
        conn.row_factory = __import__("sqlite3").Row
        return list_courses(conn, CatalogSearchFilters(q=q, provider=provider, mode=mode))


@router.get("/courses/{course_id}", response_model=CatalogCourse)
def course_detail(course_id: str) -> CatalogCourse:
    with connect() as conn:
        conn.row_factory = __import__("sqlite3").Row
        course = get_course(conn, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
