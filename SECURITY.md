# OpsTether security

OpsTether gives an authenticated AI client administrative access to servers paired with the hosted service. The Linux agent installation requires explicit acceptance of root access. Host privileges determine what the agent can do; root access can affect the entire host.

## Access model

- OAuth sign-in identifies the account used by the AI client.
- The configured public OAuth client uses Authorization Code with PKCE S256 and no client secret. Access tokens are checked for their signature, issuer, audience, expiry and required scopes.
- Paired devices belong to an organization, and requests are scoped to that organization.
- The agent initiates its connection to the service; an inbound SSH port is not required for OpsTether.
- Pairing credentials are intended for the generated installation flow. Keep them private.
- Operational output is bounded, and the service records audit metadata and usage. Redaction of known secret patterns does not guarantee that every sensitive value is removed.

Protect your OpsTether account, the AI client account and the host administration channel. Review operations that change files, services or system configuration before authorizing them.

Root shell commands can reach the files, programs and network resources available to the host. Restrictions on individual file tools do not sandbox a root shell. Do not rely on automatic redaction to remove all secrets. Commands and returned output are processed by the hosted service and the connected AI client; avoid requesting secrets or unrelated personal data.

## Report a security issue

Use the private [support channel](https://opstether.m2g.pro/support). Open [@OpsTetherBot](https://t.me/OpsTetherBot?start=support), send `/support`, and identify the request as a security report.

Include a short description of the affected behavior, the approximate time it occurred, and reproduction steps that use systems you control. Send only the information needed to explain the issue. Keep active credentials, private keys and unrelated customer data out of the report and out of public issue threads.

Support messages are relayed to the service operator and stored with the Telegram identifiers and delivery information needed to handle the conversation. Read the [privacy policy](https://opstether.m2g.pro/privacy) before sending sensitive information.

If you need to stop agent access immediately, use an administrative channel you control to stop the agent on the affected host. Investigate and rotate any credentials you believe were exposed.

## Repository scope

This repository contains public documentation for the hosted service. It does not contain the backend or agent/client source code, deployment secrets or production state. See the [proprietary notice](PROPRIETARY_NOTICE.md) and [service security information](https://opstether.m2g.pro/security).
