# OpsTether for Claude.ai, Claude Desktop, Cowork and Claude Code

**OpsTether now has separate, registered public OAuth clients for Claude.ai and Claude Code (16 November 2026).** Exact callbacks and PKCE S256 were checked against the Keycloak authorization endpoint. Interactive sign-in and MCP tool execution **inside a Claude account have not yet been verified**; please report incompatibilities rather than relying on unsupported claims.

OpsTether is a **separate hosted Linux administration MCP service**, not hosted by Anthropic or Agensi. A free Agent Skill provides instructions but does not create an account, grant Linux server access, or replace OAuth.

- Website: https://opstether.m2g.pro/
- Dashboard/account: https://opstether.m2g.pro/dashboard
- Remote MCP: `https://opstether.m2g.pro/mcp`
- Free Agent Skill: [SKILL.md](../SKILL.md)
- Download: [OpsTether Linux Ops skill ZIP v1.1.0](https://opstether.m2g.pro/downloads/opstether-linux-ops-1.1.0.zip)
- Full skill connection guide: [references/connect.md](connect.md)

## 1. Pair the user's Linux server

Create or sign in to your account on the OpsTether dashboard. Choose **Connect server**, review the generated installer and warning that this Linux agent may run as root, and pair a Linux server you own or have permission to administer. Never publish pairing credentials.

## 2a. Claude.ai / Claude Desktop / Cowork custom connector

In Claude, open **Customize → Connectors → Add custom connector**. Enter:

| Field | Value |
| --- | --- |
| Name | OpsTether |
| Remote MCP URL | `https://opstether.m2g.pro/mcp` |
| Authentication | OAuth sign-in |
| OAuth client choice | **Use your own OAuth client** |
| Public client ID | `opstether-claude` |
| Client secret | **None; leave blank** |
| Registered redirect | `https://claude.ai/api/mcp/auth_callback` |
| Scopes, if requested | `openid profile email opstether:admin` |

This client is specifically registered with the exact Claude web callback; open Dynamic Client Registration (DCR) stays disabled for security. Authenticate in the hosted OpsTether Keycloak login page and enable the connector. Availability and controls depend on your Claude account/workspace. **No end-to-end Claude account sign-in has been verified yet.**

Official reference: [Anthropic custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

## 2b. Claude Code CLI

Use a recent Claude Code version (upgrade if necessary). A separate public client `opstether-claude-code` is pre-registered for **exactly** `http://localhost:8765/callback`. The local port must be available when authenticating.

```bash
claude mcp add-json opstether \
  '{"type":"http","url":"https://opstether.m2g.pro/mcp","oauth":{"clientId":"opstether-claude-code","callbackPort":8765,"scopes":"openid profile email opstether:admin"}}' \
  --scope user
claude mcp get opstether
claude mcp login opstether
```

The JSON `oauth.scopes` field ensures that `opstether:admin` is explicitly requested. The SDK detects the authorization server through OAuth discovery. Do not use `opstether-claude` (web-only callback) in Claude Code, and do not replace `localhost` with another callback without registration. Claude Code versions affected by the `127.0.0.1` callback bug should be upgraded to v2.1.231 or newer.

Official reference: [Claude Code MCP](https://code.claude.com/docs/en/mcp).

## 3. Install the optional free skill

For Claude Code, unzip the free Agent Skill ZIP into `~/.claude/skills/opstether-linux-ops/` (all local projects) or `.claude/skills/opstether-linux-ops/` (a trusted project). The folder must contain `SKILL.md`. A project-scoped copy is also provided at [`.claude/skills/opstether-linux-ops/SKILL.md`](https://github.com/ShuhLab/OpsTether/blob/main/.claude/skills/opstether-linux-ops/SKILL.md).

The skill does **not** configure MCP automatically; the connector step above remains required. It guides safe server selection, inspections, bounded logs, Docker/systemd diagnosis and user-approved changes.

Official reference: [Claude Code Skills](https://code.claude.com/docs/en/skills).

## 4. Verify and operate safely

After OAuth, ask Claude to list your connected Linux servers. Verify the intended server appears and perform a read-only health request first. Root actions (shell commands, service restarts, package changes, file writes or firewall changes) can be disruptive: confirm exact target and request explicit approval.

If authorization is rejected, check the correct client ID and registered exact callback, and send the client type and redacted error to [OpsTether support](https://opstether.m2g.pro/support). Never share OAuth tokens, login passwords or installation codes.

### Other MCP clients

ChatGPT uses its separate `opstether-chatgpt` OAuth client. Cursor, Copilot and others may require separately registered exact callbacks. **MCP compatibility alone is not proof of successful OAuth integration.** See [the general getting-started guide](https://github.com/ShuhLab/OpsTether/blob/main/docs/GETTING_STARTED.md).
