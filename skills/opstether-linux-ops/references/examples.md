# Example requests

## Inventory and diagnostics

User: "List my Linux servers and show which are online."

Expected behavior: call `devices_list`. Show actual returned devices only. Ask the user to choose a target when several are relevant; do not invent hostnames.

User: "Why is nginx unhealthy on my server?"

Expected behavior: identify target, inspect `service_status`, `service_logs`, and `system_status` as necessary. Summarize evidence and propose a specific minimal fix. Do not restart nginx until the user approves the change.

## Docker

User: "Find the container that is restarting and explain why."

Expected behavior: identify the authorized host; inspect container and recent logs through supported tools or a bounded, approved read-only command. Do not claim a fix before verification.

## Persistent terminal

User: "Open a terminal in my project and keep the directory across commands."

Expected behavior: after target approval use `terminal_start`, then `terminal_write` and `terminal_read` to preserve shell state. Never transfer the terminal session between users. Close it when requested.

## Update with confirmation

User: "Update the config and restart the service."

Expected behavior: ask which service/config if missing, inspect, show proposed changes, get explicit confirmation, perform the authorized edit/restart, then verify service health.

## When MCP isn't connected

User: "Use this skill to list my servers."

Expected behavior: if OpsTether tools are absent, explain that installing this skill does not connect the hosted service. Refer to `connect.md`. Never simulate a tool result or ask for their account password in chat.
