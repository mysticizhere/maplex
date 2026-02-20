import os
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP, tool

from ogc_client import OgcApiClient


DEFAULT_OGC_BASE_URL = os.getenv("OGC_BASE_URL", "https://example.org/ogcapi")


mcp = FastMCP("ogc-mcp-backend")


def _get_client(base_url: Optional[str] = None) -> OgcApiClient:
    """
    Helper to construct an OGC API client with the configured base URL.
    """
    return OgcApiClient(base_url or DEFAULT_OGC_BASE_URL)


# ---------- OGC API Features tools ----------

@tool
def list_feature_collections(
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    List OGC API Features collections.

    Arguments:
      base_url: Optional OGC API base URL. If omitted, OGC_BASE_URL is used.
    """
    client = _get_client(base_url)
    try:
        return client.list_feature_collections()
    finally:
        client.close()


@tool
def get_features(
    collection_id: str,
    bbox: Optional[List[float]] = None,
    limit: Optional[int] = None,
    filter_expr: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Query features from a collection.

    Arguments:
      collection_id: Target collection identifier.
      bbox: Optional [minx, miny, maxx, maxy].
      limit: Optional maximum number of features.
      filter_expr: Optional implementation-specific filter expression.
      base_url: Optional OGC API base URL.
    """
    client = _get_client(base_url)
    try:
        return client.get_features(
            collection_id=collection_id,
            bbox=bbox,
            limit=limit,
            filter_expr=filter_expr,
        )
    finally:
        client.close()


# ---------- OGC API Records tools ----------

@tool
def list_record_collections(
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    List OGC API Records collections.
    """
    client = _get_client(base_url)
    try:
        return client.list_record_collections()
    finally:
        client.close()


@tool
def search_records(
    query: Optional[str] = None,
    limit: Optional[int] = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Search OGC API Records.

    Arguments:
      query: Optional free-text query string.
      limit: Optional maximum number of records.
      base_url: Optional OGC API Records base URL.
    """
    client = _get_client(base_url)
    try:
        return client.search_records(query=query, limit=limit)
    finally:
        client.close()


# ---------- OGC API EDR tools ----------

@tool
def list_edr_collections(
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    List collections that can be used via OGC API EDR.
    """
    client = _get_client(base_url)
    try:
        return client.list_edr_collections()
    finally:
        client.close()


@tool
def edr_position(
    collection_id: str,
    coords: List[float],
    datetime_str: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Request Environmental Data Retrieval at a specific position.

    Arguments:
      collection_id: EDR collection identifier.
      coords: Coordinate list, e.g. [lon, lat] or [lon, lat, z].
      datetime_str: Optional ISO 8601 datetime or interval.
      base_url: Optional OGC API EDR base URL.
    """
    client = _get_client(base_url)
    try:
        return client.edr_position(
            collection_id=collection_id,
            coords=coords,
            datetime_str=datetime_str,
        )
    finally:
        client.close()


if __name__ == "__main__":
    # Run the MCP server over stdio.
    mcp.run()

