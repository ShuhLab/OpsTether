# Connect an AI agent to the separate OpsTether service

**Important**: This free skill only provides operating instructions. It does not include an MCP server, bypass OAuth, grant access to any Linux host, or cover any fees that OpsTether may charge after its public beta. You must connect to OpsTether **separately**.

Remote MCP URL: `https://opstether.m2g.pro/mcp`
Website/account: https://opstether.m2g.pro/dashboard
OAuth discovery: https://opstether.m2g.pro/auth/realms/opstether/.well-known/openid-configuration

## Every client

1. Create/sign in to an OpsTether account on the hosted dashboard.
2. Install/pair the outbound Linux agent on **your own authorized server** using only the dashboard-generated installation instructions, after reviewing the root-access warning. Never paste pairing credentials into a chat or ZIP.
3. In the AI client, add the remote URL as an HTTP MCP server, choose OAuth, and sign in with the same OpsTether account.
4. Verify `devices_list` returns only your intended servers; do read-only `system_status` before any write operation.

## Claude Code

Claude Code supports remote HTTP MCP through the `claude mcp add` CLI. OpsTether does not offer anonymous MCP access or open Dynamic Client Registration.

After the service operator has registered the exact Claude OAuth callback and the public client `opstether-claude`, use:

```sh
claude mcp add --transport http --scope user --client-id opstether-claude --callback-port 8765 opstether https://opstether.m2g.pro/mcp
claude mcp login opstether
claude mcp get opstether
```

The service must register the exact callback URI, including the chosen port. The intended callback forms are `http://localhost:8765/callback` and `http://127.0.0.1:8765/callback`. **OAuth login is not yet verified end to end for Claude Code as of the initial skill release**; contact OpsTether support if you see `invalid_client` or `invalid_redirect_uri`. Do not weaken redirect allowlists or share account passwords to work around errors.

To install this skill in Claude Code, put the directory containing this `SKILL.md` under your project `.claude/skills/opstether-linux-ops/`, or in `~/.claude/skills/opstether-linux-ops/` for your user. The skill and MCP connection are **separate steps**.

## Claude (claude.ai, Claude Desktop, Cowork)

Claude offers custom remote MCP connectors. Go to **Customize → Connectors → Add custom connector**. Use server name OpsTether and the URL above. Under Authentication choose a sign-in option and, when asked to choose an OAuth client, **Use your own OAuth client** if the OpsTether operator has registered one. Public client ID: `opstether-claude` (no client secret). The corresponding redirect is `https://claude.ai/api/mcp/auth_callback`.

**Do not claim this connection is already live or independently verified.** OpsTether must enable that OAuth client before it works. Claude connector availability also depends on account and organization settings.

## ChatGPT (existing documented connector)

Where supported, configure a custom MCP server with this URL, OAuth, public client ID `opstether-chatgpt`, blank secret, and scopes `openid profile email opstether:admin`. Read https://github.com/ShuhLab/OpsTether/blob/main/docs/GETTING_STARTED.md for the current confirmed route.

## Other clients

Cursor, Copilot and other MCP-capable agents may require **their own** OAuth app registration and exact callback URL. MCP support alone does not guarantee a working connection. Ask OpsTether support about the desired client/redirect; do not claim universal plug-and-play compatibility.
