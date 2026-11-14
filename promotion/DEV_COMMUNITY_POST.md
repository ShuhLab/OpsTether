---
title: "Managing Linux servers from an AI assistant: what the MCP connection actually does"
description: "A practical look at outbound agents, OAuth, persistent terminals and the risks of root-level AI administration."
tags: mcp, linux, devops, ai
published: false
---

There is a practical gap between asking an AI assistant *what* to do on a Linux server and letting it inspect or change the server itself.

Copying terminal output into a chat works for one-off troubleshooting. It becomes awkward when a task spans multiple commands: checking a service, reading its logs, inspecting a Docker container and restarting a unit after a configuration change. It is also easy to lose the working directory or process state between steps.

We are building **OpsTether**, a hosted Model Context Protocol (MCP) service for administering Linux systems from ChatGPT and other compatible clients. Here is how the design works, what it enables and where the security boundaries really are.

## The architecture: client, control plane, agent

There are three components:

1. **The AI client** connects to the hosted MCP endpoint using OAuth. The access token identifies the authenticated OpsTether account.
2. **The OpsTether control plane** maps the request to a Linux device paired with that account, dispatches an operation and returns bounded output.
3. **The Linux agent** initiates an outbound connection to the service and executes authorized operations on the host.

The agent's outbound connection means you do not need to expose an inbound SSH port *for OpsTether*. That does not eliminate network risk or replace normal host hardening.

The MCP endpoint is:

```text
https://opstether.m2g.pro/mcp
```

A compatible client still needs an approved OAuth configuration. Not every ChatGPT account or workspace has access to custom remote MCP connectors.

## Why persistent terminals matter

Many terminal integrations start a new shell for each request. In a multi-step workflow, that can silently reset the working directory and environment or lose process state.

OpsTether supports terminal sessions that keep state between tool calls. It also exposes operations for:

- inspecting CPU, memory, disk and processes;
- reading systemd status and logs, and managing services;
- inspecting and operating Docker containers;
- working with files and directories;
- running HTTP health checks;
- observing usage and audit metadata.

For example, an operator could ask:

> List my connected servers, show which are online, and inspect memory and disk usage on the server I select.

Then, after identifying the correct host:

> Show the status of nginx and the last 50 relevant journal entries. Do not restart anything yet.

These are examples of requests, not a claim that the assistant will always interpret an ambiguous instruction correctly. Verify the target device and read the result.

## OAuth is not a sandbox

This distinction is important. OAuth authenticates and authorizes access to the **service account**. It does not magically restrict what a root process can do on Linux.

The agent installation requires an explicit acceptance of root access. A connected assistant may be able to modify files, stop services, change configuration or run arbitrary commands using those host privileges. An allowlist on a particular file tool cannot sandbox an unrestricted root shell.

That is why our documentation is explicit about the risk: connect only machines you are authorized to administer, review consequential commands, keep pairing credentials private, and do not ask the assistant to print secrets. Commands and their output pass through the hosted service and the connected AI client.

Audit records and bounded outputs are useful operational controls. They are not substitutes for backups, host security or human review.

## Trying it

1. Open the [OpsTether dashboard](https://opstether.m2g.pro/dashboard) and sign in.
2. Select **Connect server**, inspect the generated Linux installation command and its root-access acknowledgement, then pair a server you control.
3. Add the [remote MCP endpoint](https://opstether.m2g.pro/mcp) to an AI client that supports custom remote MCP with OAuth. For ChatGPT, follow the documented [client ID, scopes and callback requirements](https://github.com/ShuhLab/OpsTether/blob/main/docs/GETTING_STARTED.md).
4. Start with **“List my connected servers”**. Verify the host identity before requesting an operation.

If a device is missing, check that the dashboard and client use the same OpsTether account and that the agent can make its outbound connection.

OpsTether is currently a **public beta**. The [GitHub repository](https://github.com/ShuhLab/OpsTether) contains documentation and public assets, not the proprietary service or agent source code; it is not a self-hosting distribution.

## What would you want from an AI server-operations tool?

I would particularly like feedback from Linux and DevOps users on three questions:

- Which operations should always require an additional human approval?
- What audit details help you investigate a failed or unintended command?
- When should a multi-step task resume automatically after a connection loss, and when should it stop?

**Links:** [Website](https://opstether.m2g.pro/) · [Documentation](https://opstether.m2g.pro/docs) · [Security model](https://github.com/ShuhLab/OpsTether/blob/main/SECURITY.md) · [Support](https://opstether.m2g.pro/support)
