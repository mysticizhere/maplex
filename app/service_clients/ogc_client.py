import httpx
from typing import Any, Dict, List, Optional


class OgcApiClient:
    """
    Minimal OGC API client for use by the MCP backend.

    This client is intentionally generic and targets OGC API patterns
    as implemented by pygeoapi and other conformant servers.
    """

    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        # base_url typically points to an OGC API endpoint, e.g.
        # "https://example.org/ogcapi"
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(timeout=timeout)

    # ---------- Common helpers ----------

    def _get_json(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    # ---------- OGC API Features ----------

    def list_feature_collections(self) -> Dict[str, Any]:
        """
        List available OGC API Features collections.
        """
        return self._get_json("/collections")

    def get_features(
        self,
        collection_id: str,
        bbox: Optional[List[float]] = None,
        limit: Optional[int] = None,
        filter_expr: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Query features from a collection.

        The exact filter syntax is implementation dependent (e.g. CQL2).
        """
        params: Dict[str, Any] = {}
        if bbox is not None:
            params["bbox"] = ",".join(map(str, bbox))
        if limit is not None:
            params["limit"] = limit
        if filter_expr is not None:
            params["filter"] = filter_expr

        path = f"/collections/{collection_id}/items"
        return self._get_json(path, params=params)

    # ---------- OGC API Records ----------

    def list_record_collections(self) -> Dict[str, Any]:
        """
        List record collections, if supported by the server.
        """
        return self._get_json("/collections", params={"type": "records"})

    def search_records(
        self,
        query: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Minimal Records search.

        Many implementations expose a /search endpoint; adjust if needed.
        """
        params: Dict[str, Any] = {}
        if query:
            params["q"] = query
        if limit is not None:
            params["limit"] = limit

        return self._get_json("/search", params=params)

    # ---------- OGC API EDR ----------

    def list_edr_collections(self) -> Dict[str, Any]:
        """
        List collections that may support EDR query patterns.
        """
        return self._get_json("/collections")

    def edr_position(
        self,
        collection_id: str,
        coords: List[float],
        datetime_str: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Request Environmental Data Retrieval at a specific position.
        """
        params: Dict[str, Any] = {
            "coords": ",".join(map(str, coords)),
        }
        if datetime_str:
            params["datetime"] = datetime_str

        path = f"/collections/{collection_id}/position"
        return self._get_json(path, params=params)

    def close(self) -> None:
        self.client.close()

