# Getting started with OpsTether

## Before you connect

You need a Linux server you are authorized to administer, an OpsTether account, and an AI client that supports remote MCP servers with OAuth. The server must be able to make an outbound connection to the hosted service.

The primary access route is the OpsTether website and a direct MCP connection. OpsTether is not listed in the OpenAI Directory. Check that your client account and workspace permit custom remote MCP connections with OAuth. Required plans and permissions depend on the client; these instructions do not guarantee access for every account.

The agent installation requests root access. That access allows the connected AI to change system configuration, run programs, stop services, and read, modify or delete files. Review this access before installing the agent.

## 1. Sign in

Open the [OpsTether dashboard](https://opstether.m2g.pro/dashboard) and select **Sign in or create an account**. Complete the hosted sign-in flow.

## 2. Pair your Linux server

Select **Connect server** in the dashboard. Review the generated installation command, including the acknowledgement of root access, then run it on the intended server.

The command contains credentials for that installation flow and has an expiry time. Keep it private and use it only for the intended server. If it expires, generate a new command in the dashboard.

After installation, return to the dashboard and select **Refresh**. Confirm that the intended server appears as online.

## 3. Connect ChatGPT with OAuth

Where custom MCP connections are available in ChatGPT, open **Plugins → + → Add custom MCP server**. Add this remote server URL:

```text
https://opstether.m2g.pro/mcp
```

Choose **OAuth** authentication. The hosted service uses Authorization Code with PKCE S256.

For a ChatGPT custom connector using the callback `https://chatgpt.com/connector_platform_oauth_redirect`, the configured public client settings are:

| Setting | Value |
| --- | --- |
| Client ID | `opstether-chatgpt` |
| Client secret | Leave empty; this is a public OAuth client |
| Token endpoint authentication | `none` |
| Requested scopes | `openid profile email opstether:admin` |
| Resource / audience | `https://opstether.m2g.pro/mcp` |

Enter these values where the form exposes the corresponding fields. Authorization endpoints are available through [OAuth discovery](https://opstether.m2g.pro/auth/realms/opstether/.well-known/openid-configuration). Complete sign-in with the same OpsTether account you used in the dashboard and review the requested consent. The client ID is public configuration, not an account password or an API token.

Automatic client registration is disabled. Other clients, or a different callback URL, require the service operator to register a compatible OAuth client and its exact callback before you connect. Contact [support](https://opstether.m2g.pro/support) with the client name and callback URL; do not send credentials.

If the custom MCP option is absent, check the account and workspace requirements with your client provider or workspace administrator. Creating an OpsTether account does not enable that option in the AI client.

## 4. Confirm the connected server

Start with a request such as:

> List my connected servers.

Check the returned server name before requesting an operation. You can then ask for system resource usage, service status or relevant logs. For example:

> Show the system resource usage on this server.

> Show the status of the nginx systemd service.

Use your client's review and approval controls where available. Root access permits destructive operations, so authorize only the actions you intend to perform.

## If a server is missing or offline

Confirm that the dashboard and AI client use the same OpsTether account. Refresh the server list, check whether the agent is running on the intended host, and check its outbound connectivity to the service. If the installation command expired before it was used, create a new one.

For help, open [support](https://opstether.m2g.pro/support), start [@OpsTetherBot](https://t.me/OpsTetherBot?start=support), and send `/support`. Then send the question you want the operator to receive. Include relevant symptoms and error text without passwords, tokens or installation credentials.

[Service documentation](https://opstether.m2g.pro/docs) · [Privacy](https://opstether.m2g.pro/privacy) · [Terms](https://opstether.m2g.pro/terms) · [Security](../SECURITY.md)
