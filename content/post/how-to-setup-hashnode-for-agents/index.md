---
title: "Hashnode for Agents: Auto-Publish Setup Guide"
description: "Set up Hashnode MCP for Claude, Cursor & ChatGPT. Auto-publish posts to your Pro blog with one command. No tokens, full agent control."
slug: how-to-setup-hashnode-for-agents
date: 2026-10-24
image: cover.jpg
author: F9XR Team
keywords: hashnode mcp, ai agents auto publish, hashnode claude cursor, graphql blogging automation
categories:
  - Tutorials
tags:
  - hashnode
  - mcp
  - ai-tools
  - automation
draft: false
math: false
faq:
  - question: "Do I need Hashnode Pro?"
    answer: "Yes. The MCP server and the GraphQL API both require an active Pro plan on the publication you write to. Free publications can still be read, but writes are blocked."
  - question: "Do I need an API token for the MCP server?"
    answer: "No. You log in with your Hashnode account through the browser. The client never receives or stores a personal access token."
  - question: "Which clients work with the Hashnode MCP server?"
    answer: "Any client that supports remote MCP servers, including Claude Code, Cursor, and ChatGPT. Other MCP-compatible tools that accept an HTTP transport URL also work."
  - question: "Can a contributor role publish posts through the agent?"
    answer: "No. Contributors can create and submit drafts for review. Only owners and admins can publish directly. The agent respects the same role rules as the dashboard."
  - question: "What is the difference between the MCP server and the GraphQL skill?"
    answer: "The MCP server gives chat and coding clients ready-made tools with OAuth login. The GraphQL skill teaches a coding agent the full schema so it can write the requests itself and still needs a Personal Access Token."
  - question: "How do I revoke access for a client?"
    answer: "Open Hashnode Developer Settings. Connected clients are listed there. Disconnect any client and access stops immediately."
  - question: "Can I schedule posts through the agent?"
    answer: "Scheduling is available through the underlying API when the publication is on Pro. Ask the agent to create a draft and then schedule it, or use the CLI for timed jobs."
---

## Introduction

You already write in Markdown. Your AI coding agent already lives in the terminal or the IDE. The missing piece is a clean way to push that content straight onto your Hashnode publication without opening a browser or pasting tokens.

Hashnode now ships an official MCP server that closes that gap. Add one URL, log in once with your Hashnode account, and Claude, Cursor, ChatGPT, or any MCP client can draft, publish, edit, search, and upload images on your blog. No personal access token to copy. No local server to run. Just a remote endpoint and a browser approval flow.

One important requirement up front: the target publication must be on Hashnode Pro. Free publications cannot accept write operations through the API or MCP.

This guide walks through the exact setup, the tools your agent gains, safe publishing patterns, and how the MCP server fits alongside the GraphQL agent skill and the Hashnode CLI. 

<!--more-->

## What Is Hashnode for Agents?

Hashnode for Agents is the set of official interfaces that let AI clients manage a Hashnode publication:

- **MCP server** – remote endpoint at `https://mcp.hashnode.com/mcp`. Chat clients and coding agents call tools for posts, drafts, series, comments, and image uploads. Authentication is browser-based OAuth. No token handling.
- **Agent skill** – the GraphQL skill (`npx skills add Hashnode/gql-skill`). Coding agents learn the full schema, Pro gating rules, and safe request patterns so they can write the GraphQL themselves.
- **CLI** – every API operation exposed as a terminal command for scripts and cron jobs.

All three surfaces respect the same rules: the publication must be on Pro for writes, and role permissions (owner, admin, contributor) still apply.

## Why This Matters for Developers

Before the official MCP, people either pasted a personal access token into every client or ran a third-party local MCP server. Both approaches carried friction and risk. The official server removes the token from the equation. You approve access once per client, and you can revoke that client from Hashnode Developer Settings at any time.

Typical workflows that become one-sentence requests:

- "Publish docs/launch.md to my blog as a draft, with cover.png as the cover."
- "Update the slug and tags on the IndexNow guide."
- "List my drafts waiting for review."
- "Upload this screenshot and give me the CDN URL."

You stay in the editor or the chat. The agent does the rest.

## Prerequisites

- A Hashnode account
- A publication on **Hashnode Pro** (required for any write operation)
- An MCP-compatible client: Claude Code, Cursor, ChatGPT, or similar
- Optional: the GraphQL skill if you prefer the agent to construct requests itself

If your publication is still on the free plan, upgrade in the dashboard under Billing before continuing. The MCP server will refuse write tools until Pro is active.

## Step-by-Step: Connect the Hashnode MCP Server

### 1. Claude Code

Run a single command:

```bash
claude mcp add --transport http hashnode https://mcp.hashnode.com/mcp
```

Your browser opens Hashnode. Log in and approve access. That is the entire setup.

### 2. Cursor

Add the remote server to your `mcp.json` (or the Cursor MCP settings UI):

```json
{
  "mcpServers": {
    "hashnode": {
      "url": "https://mcp.hashnode.com/mcp"
    }
  }
}
```

Save, restart if needed, then approve the Hashnode login when the client prompts you.

### 3. ChatGPT and Other Clients

Paste the same URL wherever the client asks for a remote MCP server:

```
https://mcp.hashnode.com/mcp
```

Complete the browser login and approval. No token is generated or stored by you.

### 4. Verify the Connection

Ask the agent a simple read or list command:

- "List my recent posts."
- "Show drafts on my publication."

If the tools appear and respond, the connection is live. Connected clients also show up in Hashnode Developer Settings so you can audit or revoke them later.

## What Your Agent Can Do

The MCP server exposes tools that map to everyday publishing tasks:

| Capability              | What the agent can do                                      |
|-------------------------|------------------------------------------------------------|
| Publish posts           | Publish Markdown with tags, cover image, and series in one request |
| Edit published posts    | Change title, subtitle, slug, or tags without rewriting the body |
| Draft first             | Save a draft, review it, then publish when ready           |
| Upload images           | Upload a local image and receive a CDN URL                 |
| Search and read         | Search your posts, open one by slug, list drafts and series |
| Team review             | Submit a draft for review and list items waiting on the team |

Example natural-language requests that work well:

- "Publish the Markdown in docs/indexnow.md to my Hashnode blog. Use the title from the front matter, add the tags api and seo, and set cover.png as the cover image."
- "Save this as a draft first so I can review it."
- "Update the slug of the IndexNow post to setup-and-ping-indexnow-api-key."
- "Find every post tagged with mcp and list their titles and URLs."

Because posts go live immediately when you ask to publish, the safest default is to create a draft, inspect it in the Hashnode dashboard, then publish.

## Hashnode Agent Skill (GraphQL)

If you work primarily inside a coding agent and want the full GraphQL surface, install the official skill:

```bash
npx skills add Hashnode/gql-skill
```

The skill teaches the agent:

- Endpoint and authentication patterns
- Which operations require a Pro publication
- Pagination limits and common error codes
- How to build safe publish, draft, and update flows

You still need a Personal Access Token for the skill (stored as an environment variable, never pasted into chat). The MCP server remains the better choice when you want zero token management.

## Hashnode CLI

For scripts, CI, or cron jobs, the CLI exposes every API operation as a command. Install and authenticate according to the current Hashnode CLI documentation, then call the same publish, draft, and update operations from a terminal or pipeline. The CLI is the natural fit when the agent is not involved and you want deterministic automation.

## Practical Tips for Safe Auto-Publishing

- Always prefer "save as draft" first when the content is new or sensitive.
- Keep cover images and Markdown files in the same working directory so the agent can locate them easily.
- Use consistent front matter (title, tags, series) so the agent can extract metadata without guessing.
- Revoke unused clients from Hashnode Developer Settings on a regular schedule.
- Remember that contributor roles cannot publish directly; the agent will submit for review instead.
- If you hit a Pro-plan error, the publication (not the user account) needs the upgrade. Do not retry until Pro is active.

## Common Issues and Fixes

**"Publication does not have an active Pro plan"**  
Upgrade the target publication in the Hashnode dashboard. Writes are blocked on free publications.

**Client does not show Hashnode tools**  
Confirm the MCP URL is exactly `https://mcp.hashnode.com/mcp` and that you completed the browser approval. Restart the client after adding the server.

**Agent publishes instead of drafting**  
Be explicit: "Save as a draft" or "Create a draft, do not publish."

**Image upload fails**  
Make sure the local path is correct and the file is a supported image type. The tool returns a CDN URL on success.

**Team drafts stay in review**  
Only owners and admins can publish submitted drafts. The agent can list waiting items and submit, but final publish needs the right role.

## Key Takeaways

- Hashnode's official MCP server lets Claude, Cursor, ChatGPT and other clients manage your blog with a single remote URL and a browser login.
- No API token is required or stored by you. Access is managed and revocable from Developer Settings.
- The target publication must be on Hashnode Pro for any write operation.
- Prefer drafting first, then publishing, to keep control over what goes live.
- Use the GraphQL agent skill when you want the agent to construct full API requests itself, and the CLI for pure scripted automation.
- The same role permissions you already use in the dashboard still apply to every agent action.

Once the MCP server is connected, publishing a finished Markdown file becomes a single natural-language request. That is the real productivity win.

## Conclusion

Hashnode's MCP server turns your AI agent into a proper publishing assistant. For developers who live in the terminal or IDE, this means less context switching and faster delivery without sacrificing control. If you're looking to expand your agent workflows further, consider pairing this with automation tools like [How to Install n8n Locally on PC](/p/how-to-install-n8n-locally-on-pc/) or learning more about MCP setups like [Connect Mobbin AI Agent MCP](/p/connect-mobbin-ai-agent-mcp/). For those getting started with agent skills, [What Is Arena Skill: Install and Use AI Agents](/p/what-is-arena-skill-install-use-ai-agents/) is also a great read. As always, read our [Contributor Guide](/contribute/) and [Editorial Policy](/editorial-policy/) to learn more about how we publish at the F9XR Team.

*Written for developers who already live in the terminal or the IDE and want their Hashnode publication to feel like just another tool the agent can call. Connect the MCP server once, keep the publication on Pro, and publish becomes a natural-language request.*
