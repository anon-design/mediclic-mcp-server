"""
Configuración del MCP server — editar para cada cliente.
"""

# Identidad del producto
BRAND = "Mediclic"  # ← cambiar por nombre del cliente
SITE_URL = "https://www.mediclic.org"  # ← cambiar por dominio del cliente

# Comparativas disponibles. Cada key debe tener una página
# `/comparar/<brand-lower>-vs-<competitor-lower>` en el sitio.
COMPARISONS_AVAILABLE = {
    "doctoralia": {
        "summary": "Doctoralia es directorio + agenda + reseñas + asistente IA Noa. Mediclic es EMR + IA clínica integrada.",
        "differentiator": "Mediclic enfocado en consulta clínica con IA. Doctoralia enfocado en captación de pacientes.",
        "type": "complementary",
        "audit_date": "2026-04-30",
    },
    "medicloud": {
        "summary": "MediCloud es EMR clásico español con presencia GT desde 2019, precios públicos. Mediclic suma 6 módulos IA + dual coding CIE-10+CIE-11.",
        "differentiator": "Mediclic incluye IA y firma criptográfica; MediCloud es más económico pero sin IA.",
        "type": "substitute",
        "audit_date": "2026-04-30",
    },
    "medicpro": {
        "summary": "MedicPro es plataforma centroamericana enfocada en gestión administrativa (RR.HH., inventario, financiero). Mediclic enfocado en consulta clínica con IA.",
        "differentiator": "Mediclic para clínica con IA; MedicPro para gestión administrativa amplia.",
        "type": "different_focus",
        "audit_date": "2026-04-30",
    },
    "reservo": {
        "summary": "Reservo es plataforma chilena multi-vertical (médico+dental+estética+spa). Mediclic es 100% médico con IA clínica.",
        "differentiator": "Mediclic para especialización médica con IA; Reservo para multi-vertical.",
        "type": "different_focus",
        "audit_date": "2026-04-30",
    },
    "dricloud": {
        "summary": "DriCloud es EMR español con IA y 8,000 clientes. Mediclic se diferencia por origen guatemalteco, calculadora pediátrica auditada y firma criptográfica.",
        "differentiator": "Ambos tienen IA; Mediclic con foco GT y calculadora pediátrica auditada.",
        "type": "substitute_with_ia",
        "audit_date": "2026-04-30",
    },
}
