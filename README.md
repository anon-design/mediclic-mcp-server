# MCP Server template

Plantilla del skill `seo-geo-optimizer` para servidor MCP público que expone
features, comparativas, glosario y formulario de demo a agentes de IA.

## Setup en cliente nuevo

1. Clonar template a `/opt/<brand>-mcp-server/`.
2. Editar `config.py` con `BRAND`, `SITE_URL`, `COMPARISONS_AVAILABLE`.
3. Llenar `data/features.json`, `data/pricing.json`, `data/glossary.json`
   con datos del cliente.
4. Instalar: `pip install -r requirements.txt`.
5. Test local: `python3 main.py`.
6. Deploy:
   - DNS: `mcp.<dominio>` A record → IP del server.
   - Hestia/nginx vhost con Let's Encrypt → proxy a localhost:8200.
   - systemd service `<brand>-mcp.service` con auto-restart.
7. Validación: `curl https://mcp.<dominio>/health`.
8. Submission a Anthropic MCP marketplace
   (`https://github.com/modelcontextprotocol/servers`).

## requirements.txt

```
mcp[fastmcp]>=0.1.0
```

## systemd unit (`/etc/systemd/system/mediclic-mcp.service`)

```ini
[Unit]
Description=Mediclic MCP Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/mediclic-mcp-server
ExecStart=/usr/bin/python3 /opt/mediclic-mcp-server/main.py
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

## nginx vhost (`mcp.mediclic.org.conf`)

```nginx
server {
    listen 443 ssl http2;
    server_name mcp.mediclic.org;

    ssl_certificate /etc/letsencrypt/live/mcp.mediclic.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mcp.mediclic.org/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8200;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Cliente Claude Desktop config

Agregar a `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mediclic": {
      "url": "https://mcp.mediclic.org",
      "transport": "streamable-http"
    }
  }
}
```
