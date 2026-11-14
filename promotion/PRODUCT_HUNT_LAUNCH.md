# OpsTether — Product Hunt launch materials

**Status:** preparation only. Do not schedule or publish before verifying the maker account and checking production signup. No paid promotion.

## Product details

**Name:** OpsTether

**Product URL:** https://opstether.m2g.pro/

**Tagline (42/60 characters):** Operate Linux servers from ChatGPT via MCP

**Description (485/500 characters):**

OpsTether connects AI assistants to Linux servers through a hosted MCP service and an outbound agent. Sign in with OAuth to inspect CPU, memory and disk, use persistent terminals, manage systemd services and Docker containers, work with files, and check HTTP endpoints. The agent connects outward, so no inbound SSH port is needed for OpsTether. Installation requires explicit root-access consent. Public beta; proprietary backend. Use only on servers you are authorized to administer.

**Topics / categories to consider:** Developer Tools, DevOps, Productivity, AI Agents. Use only available categories in the current Product Hunt form.

**Logo asset:** https://raw.githubusercontent.com/ShuhLab/OpsTether/main/assets/opstether-icon.png (1024×1024 PNG)

**Gallery candidate (real site screenshot):** https://raw.githubusercontent.com/ShuhLab/OpsTether/main/assets/opstether-website.jpg (1348×926; Product Hunt recommends a wider gallery asset, so check cropping in the editor)

**Documentation:** https://github.com/ShuhLab/OpsTether/blob/main/docs/GETTING_STARTED.md

## First maker comment — draft

I'm working on OpsTether because server administration often turns into a chain of small, related diagnostic steps. AI assistants can explain those steps, but turning an explanation into controlled execution takes a reliable connection to the host.

OpsTether uses a hosted MCP endpoint, OAuth sign-in and a Linux agent that initiates an outbound connection. The beta supports persistent terminals, Linux resource inspection, systemd and Docker operations, file management and HTTP checks.

An important caveat: the installation requires root access. OAuth protects access to an OpsTether account; it does not sandbox the root privileges of the agent. Users should verify the target host and review consequential commands. Our documentation describes those limits explicitly.

We are looking for feedback from Linux users and teams that maintain their own infrastructure. Which actions would you trust an AI assistant to complete independently? Which need approval every time? And what should happen if a multi-step operation loses connection halfway through?

The public docs are available on GitHub, and the service is accessible through the website. The backend and agent code are proprietary.

## Product Hunt submission limits (checked 2026-11-15)

- Personal profile only; new accounts must be at least seven days old and email verified.
- Product name ≤40 characters, tagline ≤60, description ≤500. The values above fit these limits.
- The product URL and logo + at least one real gallery image are required.
- Save as **draft** first. Do **not** schedule a launch until onboarding has been tested with a new account and a human maker approves the date.
- Source: https://help.producthunt.com/en/articles/17834537-4-build-your-product-page

## Launch checklist

- [ ] Sign in using a **personal Product Hunt profile**, not a company/brand account.
- [ ] Verify the account email and confirm that the account is eligible to post; new accounts may have a waiting period.
- [ ] Check whether OpsTether is already listed, to avoid a second product page.
- [ ] Test the live onboarding flow and OAuth connection with a test user.
- [ ] Upload the product logo and at least one real product screenshot; do not fabricate a screenshot.
- [ ] Enter the product name, website, tagline, description and tags, and identify the maker accurately.
- [ ] Review the draft and schedule a launch date with the owner's approval; never silently activate paid promotions.
- [ ] Ask for genuine feedback, never buy or coordinate artificial upvotes.

**Source of product claims:** README.md, SECURITY.md and docs/GETTING_STARTED.md in this repository.
