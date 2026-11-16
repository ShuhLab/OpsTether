---
name: opstether-linux-ops
description: Diagnose authorized Linux servers with the separately connected OpsTether remote MCP. Use for server status, systemd, Docker, files, logs and persistent shell workflows.
---

# OpsTether for Claude Code

This repository includes the complete, portable OpsTether Agent Skill at [`skills/opstether-linux-ops/SKILL.md`](../../../skills/opstether-linux-ops/SKILL.md).

**Before using this skill, read `skills/opstether-linux-ops/SKILL.md` and its relevant `references/` files.** Follow all operational safeguards there, including explicit target-server selection and approval before state-changing root operations.

The skill **does not connect MCP by itself**. Users must separately create an account, pair their own authorized Linux server and configure the OpsTether remote MCP URL `https://opstether.m2g.pro/mcp` with OAuth.

Claude Code OAuth is not yet confirmed end-to-end; follow [Claude setup](../../../docs/CLAUDE.md) and contact support for client registration rather than assuming it works. Never request passwords or tokens in chat.

Free ZIP for Agensi or manual installation: https://opstether.m2g.pro/downloads/opstether-linux-ops-1.0.0.zip
