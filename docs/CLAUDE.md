# OpsTether with Claude Code and Claude

OpsTether's **free, Claude Code-compatible Agent Skill** is available now:

- [Skill source](../skills/opstether-linux-ops/SKILL.md)
- [Download the Agent Skill ZIP](https://opstether.m2g.pro/downloads/opstether-linux-ops-1.0.0.zip)
- [Hosted OpsTether service](https://opstether.m2g.pro/)
- [Service dashboard](https://opstether.m2g.pro/dashboard)
- [MCP endpoint](https://opstether.m2g.pro/mcp)

**Important separation:** the downloadable skill instructs Claude how to operate OpsTether tools. It does not install or host the MCP server, grant access to any Linux device, or authenticate Claude by itself. A separately connected OpsTether account and an OAuth-capable client are required.

## Claude Code

Install the skill into `~/.claude/skills/opstether-linux-ops/SKILL.md` (user scope), or `.claude/skills/opstether-linux-ops/SKILL.md` under a trusted project. Copy its `references/` files with it.

The documented remote MCP command, **after the required public OAuth client and callback are registered** with OpsTether, is:

```sh
claude mcp add --transport http --scope user --client-id opstether-claude --callback-port 8765 opstether https://opstether.m2g.pro/mcp
claude mcp login opstether
claude mcp get opstether
```

The intended callbacks are exact: `http://localhost:8765/callback` and `http://127.0.0.1:8765/callback`. OpsTether disables open Dynamic Client Registration. **The Claude-specific OAuth login is not yet confirmed in production; do not describe this CLI route as tested or plug-and-play.** If an `invalid_client` or redirect error appears, request client registration via [support](https://opstether.m2g.pro/support), providing the client name and exact callback; never send credentials.

## Claude (claude.ai / Desktop / Cowork)

In Claude, open **Customize → Connectors → Add custom connector** and enter the remote OpsTether MCP URL. Claude supports manually provided OAuth clients where the provider requires one. The intended OpsTether public client is `opstether-claude`, using `https://claude.ai/api/mcp/auth_callback`, **once this client is registered by OpsTether**. Do not claim this route is fully available before a successful authorization test.

## Install the Linux agent

Independently, create an OpsTether account via the [dashboard](https://opstether.m2g.pro/dashboard). Pair an outbound agent on a Linux host you own or administer with permission, after reading the root-access warning. Test `devices_list` and read-only `system_status` before executing any changes.

**Security:** the Linux agent can have root access. Review commands and changes, keep OAuth codes and device credentials private, and confirm the exact target server.

Docs: [Getting started](GETTING_STARTED.md) · [Security](../SECURITY.md) · [Privacy](https://opstether.m2g.pro/privacy).

Official references: [Claude MCP integration](https://code.claude.com/docs/en/mcp), [Claude custom remote connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
