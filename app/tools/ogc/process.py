from __future__ import annotations

from app.service_clients.ogc_client.ogc_client import OgcApiClient
from app.utils.auth import require_bearer_token


def register_tools(mcp):

    @mcp.tool(name="ogc_list_processes")
    @require_bearer_token()
    async def ogc_list_processes() -> dict:
        """List available OGC processes. Uses GET /processes. Returns the process list from the OGC API - Processes server."""
        return await OgcApiClient.list_processes()

    @mcp.tool(name="ogc_get_process_info")
    @require_bearer_token()
    async def ogc_get_process_info(process_id: str) -> dict:
        """Get detailed information about an OGC process by ID (inputs, outputs, execution link). Uses GET /processes/{processId}. Pass the process ID (e.g. from ogc_list_processes)."""
        return await OgcApiClient.get_process(process_id)

    @mcp.tool(name="ogc_execute_process")
    @require_bearer_token()
    async def ogc_execute_process(process_id: str, inputs: dict | None = None) -> dict:
        """Execute an OGC process asynchronously. Uses POST /processes/{processId}/execution. Pass process_id and optional inputs dict. Returns job details (e.g. jobId) to check status or fetch results later."""
        return await OgcApiClient.execute_process(process_id, inputs=inputs)

    @mcp.tool(name="ogc_get_job_status_or_results")
    @require_bearer_token()
    async def ogc_get_job_status_or_results(job_id: str) -> dict:
        """Get current OGC job status. Uses GET /jobs/{jobId}. If the job is done (successful/succeeded/done/complete), also fetches and returns results via GET /jobs/{jobId}/results. Otherwise returns current job status only."""
        return await OgcApiClient.get_job_status_or_results(job_id)
