# Agensi listing — OpsTether Linux Operations (free)

> Publication checklist / source copy. **This is not proof that Agensi approved a listing.**
> Current ZIP: https://opstether.m2g.pro/downloads/opstether-linux-ops-1.1.0.zip
> Version: 1.1.0 · Format: one SKILL.md plus six text-only support files · Price: **Free**

## Listing fields

**Name:** OpsTether Linux Server Operations

**Summary (under 300 characters):**  
A free Claude Code and MCP companion skill for inspecting and operating authorized Linux servers with OpsTether. Covers systemd, Docker, logs, files and persistent terminals. The hosted MCP service must be connected separately via OAuth.

**Suggested categories:** Developer Tools / DevOps / Automation (select the closest live Agensi categories).

**Suggested tags:** `linux`, `devops`, `mcp`, `claude-code`, `systemd`, `docker`, `infrastructure`, `server-operations`, `persistent-terminal`.

**Pricing:** Free; no subscription, payout account or payment setup for the skill.

**Needs access to:** Separately hosted OpsTether MCP service at https://opstether.m2g.pro/mcp; an OpsTether account; an OAuth-capable AI client; and a Linux server owned or administered with permission. The ZIP does **not** include a server instance, authorization, privileged credentials, or Linux binaries.

**Logo:** https://raw.githubusercontent.com/ShuhLab/OpsTether/main/assets/opstether-icon.png (square 1024×1024 PNG).

**Download:** https://opstether.m2g.pro/downloads/opstether-linux-ops-1.1.0.zip

**Source:** https://github.com/ShuhLab/OpsTether/tree/main/skills/opstether-linux-ops

**Claude integration guide:** https://github.com/ShuhLab/OpsTether/blob/main/docs/CLAUDE.md

## Description (Markdown)

### Linux operations guided by AI — with explicit human control

OpsTether Linux Server Operations is a **free AI Agent Skill** that teaches Claude Code and other compatible agents how to use the separate OpsTether MCP service for Linux administration. It guides server selection, read-only diagnosis, log inspection, systemd service checks, Docker workflows, file operations and persistent terminal sessions. It asks for authorization before changes and verifies results afterwards.

**The skill is instructions, not the MCP server.** Agensi does not host OpsTether. Users must register separately on the [OpsTether site](https://opstether.m2g.pro/), pair a Linux server they are allowed to administer, add `https://opstether.m2g.pro/mcp` to their AI client, and complete the separate OAuth authorization flow. The skill itself does not provide an account, tool access, server hosting, credentials or a pre-configured OAuth login.

**Compatibility:** Agent Skill instructions can be installed in Claude Code. An optional GitHub Claude Code plugin is also available separately. OpsTether has pre-registered distinct OAuth clients for Claude Web and Claude Code with exact callbacks, and server-side PKCE/token-flow tests have passed. Interactive login from an actual Claude account still needs end-user verification, and other agents may require separate OAuth callback registration. Do not assume universal OAuth support.

**Security:** The separately installed Linux agent can have root privileges. This skill starts with read-only checks, requires server identity confirmation and explicit user approval for state-changing actions, treats logs as untrusted, and avoids exposing credentials.

**Cost:** The downloadable skill is free. OpsTether is a separate proprietary hosted service currently in a public beta, subject to its own current service terms.

[Quickstart](https://github.com/ShuhLab/OpsTether/blob/main/docs/CLAUDE.md) · [Security](https://opstether.m2g.pro/security) · [Support](https://opstether.m2g.pro/support)

## See it in action — read-only real MCP test (17 November 2026)

**Actual test request:** "List the Linux servers connected to my OpsTether account. On the selected server, show the system's uptime and free memory, and check whether the OpsTether control systemd service is running. Do not change anything."

The test was run against an OpsTether account with **one authorized online Linux device**. Host-identifying details and internal quota metadata are omitted from this public demonstration. No simulated values or fabricated commands are presented.

**Actual tool sequence and evidence:**

1. `devices_list`: returned **1 connected device**, marked **online**.
2. `system_status` on the selected device: architecture `amd64`, operating system `linux`, uptime **159,020 seconds** (approximately **44 hours 10 minutes**), total memory **16,764,948,480 bytes** (about 15.61 GiB), free memory **14,348,496,896 bytes** (about 13.36 GiB).
3. `service_status` for the selected OpsTether control service: `active_state=active`, `sub_state=running`.

**Full user-facing result, with hostname omitted for publication:**

> I found one authorized Linux server in your OpsTether account, and its connection is currently online. The selected server is running Linux on amd64 with approximately 44 hours of uptime. Total RAM is about 15.61 GiB, of which about 13.36 GiB is currently reported free. The requested OpsTether control service is active and running according to systemd.
>
> **No changes were made.** These checks confirm the device is reachable and this systemd service is running at the time of inspection. They do not establish disk health, application-level response times, past failures or how the service will behave later. If further investigation is needed, I can read a bounded number of service log lines or perform a separate health check, after confirming the intended target.

**What this demonstrates:** real MCP discovery, resource inspection and service diagnosis without a restart or shell mutation. A SKILL.md guides the workflow, but its installation does not grant access; users must separately connect their own authorized server to the hosted OpsTether service with OAuth.

## Submission checklist

- [x] Source skill published in public GitHub
- [x] ZIP downloadable and checksum verified
- [x] No credentials, tokens or executable installers in ZIP
- [x] Free listing / external MCP dependency disclosed
- [x] Claude Code plugin and server-side OAuth flows verified
- [ ] Agensi creator account authorized in browser
- [ ] ZIP and logo uploaded to Agensi Creator Studio
- [ ] Pricing = Free; needs-access-to = OpsTether MCP
- [ ] Submission confirmed and under review
- [ ] Agensi listing publicly approved

**Submission page:** https://www.agensi.io/dashboard/submit

Agensi's Joeri Brons explicitly confirmed by email on 2026-11-13 that a free skill depending on separately hosted OpsTether MCP is allowed. Do not imply Agensi hosts the MCP server or that marketplace approval has occurred before confirmation.
