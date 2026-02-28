from pathlib import Path

from django.conf import settings
from django.http import FileResponse, HttpResponseNotFound
from django.views.static import serve as static_serve


def spa(request, path=""):
    """
    Serve the built frontend (Vite) from disk.
    - If the requested file exists under FRONTEND_DIST_DIR, return it.
    - Otherwise return index.html (SPA fallback).
    """
    dist_dir = Path(settings.FRONTEND_DIST_DIR)
    if path:
        candidate = dist_dir / path
        if candidate.is_file():
            return static_serve(request, path, document_root=dist_dir)

    index_file = dist_dir / "index.html"
    if index_file.is_file():
        return FileResponse(index_file.open("rb"), content_type="text/html")

    return HttpResponseNotFound(
        "Frontend build not found. Run the frontend build to create dist/."
    )
