---
title: Set Up n8n Nod Agent on Hostinger VPS
published: false
description: Step-by-step guide to self-host n8n Labs Nod personal AI agent on Hostinger VPS with Docker Compose. Keep it private, connect models, and run 24/7.
tags: n8n, aiagents, selfhosting, automation
cover_image: https://raw.githubusercontent.com/f9xr/dev9b/master/content/post/how-to-set-n8n-nod-agent-on-hostinger-vps/cover.jpg
canonical_url: https://f9xr.org/dev9b/p/how-to-set-n8n-nod-agent-on-hostinger-vps/
---

Most AI agents still live in a chat window. You ask, they answer, and you still have to do the actual work. Nod from n8n Labs flips that. It is a personal agent with its own Linux workspace and browser. You tell it to cancel a trial, chase an invoice, or prep a call brief, and it goes and does the job on real websites and in your connected apps. It asks before anything sensitive, and it runs on hardware you control.

Nod is a research preview from n8n Labs (released November 2026). It is completely separate from the n8n workflow tool and from the Agents feature inside n8n. You do not need an n8n account to use it. The app is free and open source under Apache 2.0. You bring your own model provider (OpenAI, Anthropic, OpenRouter, Gemini, local Ollama, or ChatGPT Plus/Pro).

Running Nod on a laptop works for testing. Running it on a Hostinger VPS keeps the agent online 24/7 so scheduled tasks and background checks actually fire. This guide walks through the practical path: pick the right plan, install Docker, clone the official self-host kit, generate secrets, start the stack, and reach it safely via SSH tunnel or HTTPS.

> **NOTE** â€” Disclosure
>
> Some links in this guide, including the Hostinger signup link, are affiliate or referral links. If you buy through them the price is unchanged and it supports the site.
>

## Key Takeaways

- Nod is a standalone personal AI agent from n8n Labs. It has its own sandbox, browser, and permission model. It is not the n8n AI Agent node and not Managed n8n.
- The official self-host method uses Docker Compose from the n8n-io/nod repository. The recommended starting point is 2 vCPU, 8 GB RAM, 50 GB disk.
- Hostinger KVM 2 matches the recommended specs and is the practical choice for most developers.
- Always keep the server port bound to localhost (127.0.0.1). Reach it with an SSH tunnel or put Caddy in front for HTTPS. Never expose the port directly.
- Back up the Vault key the moment you generate it. Without that key, saved credentials are unrecoverable even if you have a perfect database dump.
- After the stack is up, finish onboarding in the web UI, connect a model, and optionally link n8n if you already run it.

## What Is Nod Exactly?

Nod is described by the team as "an open source personal agent with its own computer." It:

- Runs commands and keeps files in a private Linux workspace
- Browses the web in its own Chromium instance (you can take over when a site needs human input)
- Connects to Gmail, Calendar, Slack, Notion, Linear and other apps
- Supports scheduled jobs and background checks
- Asks for confirmation before actions that are not clearly covered by your request
- Stores credentials encrypted with a Vault key that lives outside the database

Because it is a research preview, expect rough edges and occasional breaking changes. Treat it as a powerful tool you still supervise, not a fully autonomous employee. If you want a gentler starting point with a desktop agent, our [Grok Bot setup guide](https://f9xr.org/dev9b/p/how-to-setup-grokbot/) is a good warm-up.

## Why Hostinger VPS for Nod?

Hostinger already has a popular one-click n8n template. The same KVM plans work cleanly for Nod because the official self-host kit is just Docker Compose. If you prefer a desktop install, our walkthrough on [installing n8n locally on a PC](https://f9xr.org/dev9b/p/how-to-install-n8n-locally-on-pc/) covers that route. On a VPS you get:

- Predictable pricing and NVMe storage
- Easy root/SSH access
- Docker Manager if you want to keep an eye on containers from the panel
- Enough headroom on KVM 2 for the browser and workspace containers

Other providers work too. Hostinger is simply convenient if you already use it or want a single bill for both n8n and Nod.

### Recommended Hostinger Plan

| Plan  | vCPU | RAM  | Storage | Best For                          | Notes                          |
|-------|------|------|----------|-----------------------------------|--------------------------------|
| KVM 1 | 1    | 4 GB | 50 GB    | Light testing only                | Tight once browser starts      |
| KVM 2 | 2    | 8 GB | 100 GB   | Daily use, schedules, one browser | Recommended starting point     |
| KVM 4 | 4    | 16 GB| 200 GB   | Heavier concurrent tasks          | Comfortable headroom           |
| KVM 8 | 8    | 32 GB| 400 GB   | Multiple agents or local models   | Overkill for most solo use     |

Start with KVM 2. The official docs suggest two cores and 8 GB. The Compose file caps the server, browser, and workspace containers so they do not starve the host.

Grab a Hostinger VPS here if you need one: [Hostinger VPS plans](https://www.hostinger.com/in?REFERRALCODE=INAKMM).

## Prerequisites

- A Hostinger VPS (Ubuntu 24.04 preferred) with at least 2 vCPU and 8 GB RAM
- SSH access (key preferred over password)
- Docker Engine 25 or newer with Compose v2
- Git, OpenSSL, and basic tools
- A domain (optional, only if you want public HTTPS access)
- An AI model provider key or ChatGPT Plus/Pro plan (you connect this after the server starts)

No model key is required just to install and start the stack.

## Step-by-Step: Deploy Nod on Hostinger VPS

### 1. Provision the VPS

Log into Hostinger hPanel, create or select a KVM 2 (or higher) plan, and choose Ubuntu 24.04. Add your SSH public key during setup. Note the IP address.

Once the server is ready, SSH in as root (or the user you created).

### 2. Install Docker and Required Tools
```bash
apt update && apt upgrade -y
apt install -y ca-certificates curl git openssl
curl -fsSL https://get.docker.com | sh
systemctl enable --now docker
```

Verify:
```bash
docker version
docker compose version
```

You want Docker Engine 25+ and Compose v2. Add your user to the docker group if you prefer not to run everything as root:
```bash
usermod -aG docker yourusername
# log out and back in
```

### 3. Clone the Official Nod Self-Host Kit

Pin to a known tag so the build is reproducible. At the time of writing, recent tags include nod-v0.8.1 and newer. Check the [GitHub releases page](https://github.com/n8n-io/nod/releases) for the latest stable tag.
```bash
git clone https://github.com/n8n-io/nod.git
cd nod
git checkout nod-v0.8.1   # or the latest tag you prefer
cd deployment/self-host
ls
```

You should see `setup.sh`, `compose.yaml`, `Caddyfile`, `backup.sh`, `restore.sh`, and `.env.example`.

### 4. Generate Secrets with setup.sh
```bash
sh setup.sh
```

This script:

- Creates a private `.env` from the example
- Generates a Compose project name
- Creates `NOD_AUTH_TOKEN` (hex)
- Creates `NOD_VAULT_KEY` (base64)
- Creates a Postgres password
- Sets permissions to 600 on `.env`

**Immediately copy the Vault key somewhere safe** (password manager, encrypted note, offline). Without this key, every saved login becomes unreadable even if you restore the database.
```bash
grep NOD_VAULT_KEY .env
grep NOD_AUTH_TOKEN .env
```

### 5. Build and Start the Stack
```bash
docker compose up -d --build --wait
docker compose ps
```

The first build takes time because it compiles the workspace tools and browser image. `--wait` blocks until the health-checked services report healthy. When it finishes you should see the server, postgres, browser, workspace and related services running.

Check logs if anything looks off:
```bash
docker compose logs --tail 100 server
```

### 6. Reach Nod Safely

The server binds to `127.0.0.1:4310` by default. Do not change this to `0.0.0.0`. Docker published ports bypass ufw, so the loopback binding is what keeps the port private.

**Option A – SSH tunnel (simplest and safest for personal use)**

On your local machine:
```bash
ssh -L 4310:127.0.0.1:4310 user@YOUR_VPS_IP
```

Keep the tunnel open and open `http://localhost:4310` in your browser. Paste the `NOD_AUTH_TOKEN` when asked.

**Option B – HTTPS with the Caddy profile**

If you have a domain pointing at the VPS:

1. Edit `.env` and set:
```bash
NOD_PUBLIC_URL=https://nod.yourdomain.com
```

2. Start with the https profile:
```bash
docker compose --profile https up -d --build --wait
```

Open the HTTPS URL and paste the access token. Ports 80 and 443 will be published. Make sure your provider firewall allows them.

### 7. Finish Onboarding and Connect a Model

Once you are in the web UI:

1. Complete the short onboarding flow.
2. Connect a model provider (OpenAI, Anthropic, OpenRouter, Gemini, Azure, local OpenAI-compatible endpoint, or ChatGPT plan).
3. Optionally connect apps (Gmail, Slack, Notion, etc.).
4. Optionally connect an existing n8n instance if you want Nod to build and run workflows for you.

Nod can now take tasks in plain language. It will ask for confirmation when an action is outside the scope of your request. If you are still choosing a provider, our roundup of the [best coding models on OpenRouter](https://f9xr.org/dev9b/p/best-coding-models-openrouter/) is a useful shortcut.

## Security and Operational Tips

- Keep `NOD_BIND_ADDRESS` at `127.0.0.1`. Never expose the server port directly to the internet.
- Back up the Vault key and run the official `backup.sh` regularly. The database alone cannot recover credentials.
- Set `NOD_ANALYTICS_ENABLED=false` (already the default in recent kits) if you want no usage sharing.
- Treat Nod as a research preview. Give it access only to accounts you are comfortable testing with.
- Monitor memory. The browser and workspace containers can use several GB when doing real web work. KVM 2 is the practical minimum for comfortable daily use.
- When you update, check the official server operations docs, take a backup first, then pull the new tag and rebuild.

## Common Use Cases After Setup

- Daily call briefs that pull calendar, email threads and recent client news
- Invoice chasing and filing from supplier portals
- Price or stock monitoring with notifications only when something changes
- Drafting and sending replies after you approve them
- Building and testing n8n workflows by describing them in chat (if you connected n8n)

## Troubleshooting Quick Hits

| Symptom                         | Likely Cause                          | Fix                                      |
|---------------------------------|---------------------------------------|------------------------------------------|
| Build fails or OOM              | Not enough RAM                        | Move to KVM 2+ or raise container limits |
| Cannot reach the UI             | Port not bound to loopback or tunnel  | Check SSH tunnel or Caddy profile        |
| "Run setup.sh first"            | Missing or incomplete .env            | Re-run `sh setup.sh`                     |
| Lost credentials after restore  | Missing Vault key                     | You need the original `NOD_VAULT_KEY`    |
| High memory on idle             | Browser/workspace still warm          | Restart containers or lower limits       |

## Comparing Self-Hosted Agents

Nod is one option in a fast-moving category. If you want a one-click Docker template instead of a manual Compose clone, our guide to [deploying Hermes Agent on Hostinger VPS](https://f9xr.org/dev9b/p/how-to-set-hermes-agent-on-hostinger-vps/) shows the Docker Manager route. If you want a free, open coding agent to pair with Nod, the [Freebuff free AI coding agent overview](https://f9xr.org/dev9b/p/what-is-freebuff-free-ai-coding-agent/) explains what it does and where it fits.

## Frequently Asked Questions

### Do I need n8n to run Nod?

No. Nod is a standalone app. You only need n8n if you want Nod to create and run workflows inside an existing n8n instance.

### What is the minimum VPS size for Nod?

Official guidance is two CPU cores, 8 GB RAM and 50 GB disk. KVM 2 on Hostinger matches this and is the recommended starting point.

### How do I keep Nod private?

Leave the bind address at 127.0.0.1 and reach it through an SSH tunnel. For public access use the official Caddy HTTPS profile with a domain you control.

### Is the Vault key recoverable?

No. If you lose `NOD_VAULT_KEY`, saved credentials cannot be decrypted even with a full database backup. Back it up immediately after `setup.sh`.

### Can I run Nod and n8n on the same Hostinger VPS?

Yes. Many developers run both. Just make sure you have enough RAM (KVM 2 or higher) and keep the ports and volumes separate.

### How do I update Nod later?

Take a backup with the provided script, check out the newer tag, rebuild with `docker compose up -d --build --wait`, and keep the same Compose project name so volumes stay attached.

## Conclusion

Deploy the stack, protect the Vault key, keep the port on loopback, and let Nod handle the repetitive browser and app work while you stay in control of every sensitive action. The research-preview nature means you should still review what it does, but the architecture (own workspace, browser and permission checks) is already more practical than most chat-only agents.

If you spot an error or want to add a step, read the [contributor guide](https://f9xr.org/dev9b/contribute/) and our [editorial policy](https://f9xr.org/dev9b/editorial-policy/). Corrections with a reproducible case are always welcome.
