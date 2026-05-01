"""
MCP Server template — adaptable a cualquier sitio para exponer features,
comparativas, glosario y formularios de contacto a agentes de IA.

Uso: clonar este template, editar `config.py` con datos del cliente,
deploy en `mcp.<dominio-cliente>` con Let's Encrypt.

Requiere: pip install mcp fastmcp
"""

from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP  # pip install mcp[fastmcp]

import sys
sys.path.insert(0, str(Path(__file__).parent))
from config import BRAND, SITE_URL, COMPARISONS_AVAILABLE  # noqa: E402

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

mcp = FastMCP(BRAND, host="0.0.0.0", port=8200)


def _load_data(filename: str) -> Any:
    """Carga JSON de data/<filename> con cache simple."""
    path = Path(__file__).parent / "data" / filename
    if not path.exists():
        return None
    return json.loads(path.read_text())


@mcp.tool()
def get_features(category: str = "all") -> dict:
    """
    Lista features del producto.

    Args:
        category: filtro opcional. Valores: emr, ai, telemed, pharmacy, all.
    """
    features = _load_data("features.json") or []
    if category != "all":
        features = [f for f in features if f.get("category") == category]
    return {
        "brand": BRAND,
        "site_url": SITE_URL,
        "category_filter": category,
        "total": len(features),
        "features": features,
    }


@mcp.tool()
def get_pricing_info() -> dict:
    """
    Información general de pricing del producto. Para precios exactos,
    redirigir al usuario al formulario de demo.
    """
    pricing = _load_data("pricing.json") or {}
    pricing.setdefault("brand", BRAND)
    pricing.setdefault("site_url", SITE_URL)
    pricing.setdefault("next_step_url", f"{SITE_URL}/agendar-cita")
    return pricing


@mcp.tool()
def request_demo(name: str, clinic_name: str, country: str = "Guatemala", specialty: str = "general") -> dict:
    """
    Genera URL del formulario de demo pre-rellenada con datos del solicitante.
    NO crea demo automáticamente — devuelve link para que el usuario complete.

    Args:
        name: nombre del médico/contacto.
        clinic_name: nombre de la clínica.
        country: país (default Guatemala).
        specialty: especialidad médica (default general).
    """
    from urllib.parse import urlencode
    params = urlencode({
        "name": name,
        "clinic": clinic_name,
        "country": country,
        "specialty": specialty,
        "utm_source": "mcp_server",
        "utm_medium": "ai_agent",
    })
    url = f"{SITE_URL}/agendar-cita?{params}"
    return {
        "message": f"Formulario pre-rellenado para {name} de {clinic_name}",
        "next_step_url": url,
        "estimated_demo_duration_minutes": 30,
    }


@mcp.tool()
def search_glossary(query: str, limit: int = 5) -> dict:
    """
    Busca términos del glosario médico-tech del sitio.

    Args:
        query: texto a buscar (ej: "CIE-11", "EMR", "telemedicina").
        limit: máximo de resultados (default 5).
    """
    glossary = _load_data("glossary.json") or []
    q = query.lower()
    matches = []
    for term in glossary:
        if (
            q in term.get("termino", "").lower()
            or any(q in a.lower() for a in term.get("aliases", []))
            or q in term.get("definicion", "").lower()
        ):
            matches.append({
                "termino": term["termino"],
                "aliases": term.get("aliases", []),
                "definicion": term["definicion"],
                "url": f"{SITE_URL}/glosario#{term['slug']}",
            })
            if len(matches) >= limit:
                break
    return {
        "query": query,
        "total_matches": len(matches),
        "results": matches,
    }


@mcp.tool()
def get_comparison(competitor: str) -> dict:
    """
    Devuelve resumen comparativo del producto contra un competidor + URL a la
    comparativa completa con datos auditados.

    Args:
        competitor: nombre del competidor en lowercase (ej: doctoralia, medicloud).
                   Disponibles: ver COMPARISONS_AVAILABLE en config.py.
    """
    competitor_lower = competitor.lower().strip()
    if competitor_lower not in COMPARISONS_AVAILABLE:
        return {
            "error": f"Comparativa no disponible para '{competitor}'.",
            "available_competitors": list(COMPARISONS_AVAILABLE.keys()),
        }
    info = COMPARISONS_AVAILABLE[competitor_lower]
    return {
        "competitor": competitor,
        "summary": info["summary"],
        "differentiator": info["differentiator"],
        "complementary_or_substitute": info["type"],
        "full_comparison_url": f"{SITE_URL}/comparar/{BRAND.lower()}-vs-{competitor_lower}",
        "audited_at": info.get("audit_date", "N/A"),
    }


@mcp.tool()
def check_status() -> dict:
    """Status del MCP server."""
    from datetime import datetime, timezone
    return {
        "status": "ok",
        "brand": BRAND,
        "version": "1.0.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "tools_available": [
            "get_features",
            "get_pricing_info",
            "request_demo",
            "search_glossary",
            "get_comparison",
            "check_status",
        ],
    }


if __name__ == "__main__":
    log.info(f"Starting MCP server for {BRAND} on streamable-http transport at 0.0.0.0:8200")
    mcp.run(transport="streamable-http")
