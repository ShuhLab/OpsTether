# OpsTether updates without reinstalling

OpsTether has three distinct components. They update differently. **A free skill is instructions, not a remotely installed MCP server.** Nothing in our ZIP silently downloads or executes code.

## Claude Code plugin: native automatic updates

Existing installations keep the stable plugin ID `opstether@shuhlab-ops`. Install once:

```sh
claude plugin marketplace add ShuhLab/OpsTether
claude plugin install opstether@shuhlab-ops
```

Then **enable auto-update once per user** in Claude Code: `/plugin` → **Marketplaces** → **shuhlab-ops** → **Enable auto-update**. Anthropic deliberately keeps auto-update disabled by default for third-party marketplaces; a plugin publisher cannot remotely force this preference. Once enabled, Claude Code checks the marketplace after sessions start and obtains new versions when the published plugin version changes. Restart Claude Code or reload plugins to apply the update.

To verify or update manually without uninstalling:

```sh
claude plugin update opstether@shuhlab-ops
claude plugin list
```

**Verified on 18 November 2026:** an existing Claude Code test installation updated from **v1.1.0 to v1.1.1** with `claude plugin update`, without uninstall or reinstall.

## Claude.ai and Cowork: GitHub marketplace sync

The Shuh Lab marketplace has already been added to a personal Claude account. Its plugin is a text-only skill. In **Plugins / Marketplaces**, the owner must perform the one-time steps shown by Claude: **Grant access** to the Claude GitHub App and enable **Sync automatically**. This allows Claude to refresh versions from `ShuhLab/OpsTether` without a new marketplace installation. Installed skills reflect updates after sync and session/plugin refresh; exact availability depends on the account or organization.

**Note:** This plugin alone does not connect OAuth to the hosted MCP service. Do not confuse a plugin version refresh with a Linux server-agent binary upgrade.

## Agensi: buyers do not reinstall

Agensi automatically serves each user the **newest approved live skill version** the next time their agent loads it. The creator must publish an updated ZIP with a higher version into **the same existing listing**. Agensi runs security and approval checks before a new version becomes live. The previous live version continues serving buyers until approval; if an update is rejected, the previous version stays live.

Publishing to Agensi is **not** currently unattended: no authenticated Agensi creator connector is connected to the release pipeline. Upload the new ZIP in Creator Studio or connect Agensi's `update_skill` creator tool for a future fully automated submission flow. Do not claim a new skill version is live until Agensi confirms approval.

Current approved version depends on the listing's actual status; the GitHub and ZIP version can be newer while an Agensi submission is pending.

## Website: stable links to latest build

- [Latest standalone ZIP](https://opstether.m2g.pro/downloads/opstether-linux-ops-latest.zip)
- [Latest Agensi-format ZIP](https://opstether.m2g.pro/downloads/opstether-linux-ops-agensi-latest.zip)
- [Release version + SHA-256 checksums](https://opstether.m2g.pro/downloads/opstether-skill-latest.json)

A GitHub Actions pipeline watches the canonical `skills/opstether-linux-ops/` source and automatically bumps the patch version when its contents change, syncs the Claude plugin copy and creates two checked archives. A restricted, unprivileged VDSKA service checks the published GitHub version every **15 minutes**. It atomically replaces the latest ZIPs only when the mirror/version validation and SHA-256 checks succeed, refuses downgrades or immutable version conflicts, and leaves the previous files intact on a failure.

This is **artifact delivery**, not automatic modification of users' locally downloaded SKILL.md files. Use native marketplace updates above to avoid reinstalling.

## Hosted MCP backend

All compatible clients continue using `https://opstether.m2g.pro/mcp`; this stable URL points to the centrally maintained hosted OpsTether service. No client reinstall is needed when we update the hosted MCP backend. The separately paired Linux **agent** has its own deployment lifecycle, which is not changed by a skill/Claude plugin update.

## Evidence and rollback

- [Successful auto-release run for v1.1.1](https://github.com/ShuhLab/OpsTether/actions/runs/44308470415)
- [Release builder](../tools/release_opstether_skill.py)
- [Release workflow](../.github/workflows/opstether-skill-release.yml)
- [Downloads updater](../deploy/skills/publish_latest.py)
- [Claude Code marketplace update policy](https://code.claude.com/docs/en/plugins/host-marketplace)
- [Agensi skill update policy](https://www.agensi.io/docs/updates)

To fix a bad release, revert the canonical skill source, publish a new higher patch version and allow the native update mechanism to distribute that fix. An Agensi update rejected by moderation never replaces the last live version.
