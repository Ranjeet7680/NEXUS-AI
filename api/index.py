import os
import sys
from urllib.parse import parse_qs, urlencode

# Ensure root workspace is available on sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.main import app as fastapi_app

class VercelPathRewriteMiddleware:
    """
    Restores the original request path from the query parameter rewrite on Vercel.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            query_string = scope.get("query_string", b"").decode("utf-8")
            params = parse_qs(query_string, keep_blank_values=True)
            if "__path__" in params and params["__path__"]:
                original_path = params["__path__"][0]
                if not original_path.startswith("/"):
                    original_path = "/" + original_path
                scope["path"] = original_path
                scope["raw_path"] = original_path.encode("utf-8")

                # Remove __path__ from query_string
                clean_pairs = []
                for k, vs in params.items():
                    if k != "__path__":
                        for v in vs:
                            clean_pairs.append((k, v))
                scope["query_string"] = urlencode(clean_pairs).encode("utf-8")

        await self.app(scope, receive, send)

app = VercelPathRewriteMiddleware(fastapi_app)
