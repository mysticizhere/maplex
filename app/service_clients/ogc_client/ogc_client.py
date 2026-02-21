from __future__ import annotations

import typing as t

from app.exceptions import BaseException
from app.service_clients import BaseAPIClient
from app.service_clients.ogc_client.base_ogc_client import BaseOgcClient


def _check_response(response: t.Any) -> None:
    """Raise BaseException on HTTP error status."""
    if response.status_code >= 400:
        text = getattr(response, "text", None)
        msg = (text if isinstance(text, str) else "Request failed") or "Request failed"
        raise BaseException(msg[:500], status_code=response.status_code)


def _json_or_empty(response: t.Any, *, default: dict | list | None = None) -> t.Any:
    """Parse JSON body or return default (empty dict if None)."""
    if not getattr(response, "content", None):
        return default if default is not None else {}
    try:
        return response.json()
    except Exception:
        return default if default is not None else {}


class OgcApiClient(BaseOgcClient):

    @classmethod
    @BaseAPIClient.api_handler()
    async def list_processes(cls) -> dict | list:
        """GET /processes - List available processes."""
        response = await cls.get(path="/processes")
        _check_response(response)
        out = _json_or_empty(response)
        return out if out is not None else {}

    @classmethod
    @BaseAPIClient.api_handler()
    async def get_process(cls, process_id: str) -> dict:
        """GET /processes/{processId} - Get process description."""
        response = await cls.get(path=f"/processes/{process_id}")
        _check_response(response)
        out = _json_or_empty(response, default={})
        return out if isinstance(out, dict) else {}

    @classmethod
    @BaseAPIClient.api_handler()
    async def execute_process(cls, process_id: str, inputs: dict | None = None) -> dict:
        """POST /processes/{processId}/execution - Execute process and return job details."""
        payload = inputs if inputs is not None else {}
        response = await cls.post(path=f"/processes/{process_id}/execution", json=payload)
        _check_response(response)
        out = _json_or_empty(response, default={})
        out = out if isinstance(out, dict) else {}
        # 201 may return Location header with job URL; capture jobId for status/results
        location = response.headers.get("Location") or response.headers.get("location")
        if location and "jobId" not in out and "job_id" not in out:
            job_id = location.rstrip("/").split("/")[-1]
            if job_id:
                out["jobId"] = job_id
        return out

    @classmethod
    @BaseAPIClient.api_handler()
    async def get_job_status_or_results(cls, job_id: str) -> dict:
        """GET /jobs/{jobId} for status; if done, GET /jobs/{jobId}/results and return results."""
        status_response = await cls.get(path=f"/jobs/{job_id}")
        _check_response(status_response)
        status_body = _json_or_empty(status_response, default={})
        status_body = status_body if isinstance(status_body, dict) else {}
        status_value = (
            (status_body.get("status") or status_body.get("jobStatus") or "").lower()
        )
        if status_value in ("successful", "succeeded", "done", "complete", "completed"):
            results_response = await cls.get(path=f"/jobs/{job_id}/results")
            _check_response(results_response)
            results_body = _json_or_empty(results_response, default={})
            return {"status": status_body, "results": results_body}
        return status_body

