---
title: "How to Add MCP Servers to OpenCode"
description: "Add local and remote MCP servers to OpenCode — extend your agent with Sentry, Context7, Grep, and custom tools via the Model Context Protocol."
slug: opencode-mcp-servers
date: 2026-09-06
image: cover.jpg
author: F9XR Team
keywords:
    - OpenCode
    - MCP
    - Model Context Protocol
    - MCP server
    - AI coding agent
    - tools
categories:
    - Tutorials
tags:
    - opencode
    - ai-tools
    - developer-setup
    - mcp
draft: false
math: false
faq:
    - question: "What is an MCP server in OpenCode?"
      answer: "An MCP (Model Context Protocol) server is an external tool that adds capabilities to OpenCode's agent. It can be local (runs on your machine) or remote (a hosted API), and its tools appear alongside OpenCode's built-in tools like bash, edit, and grep."
    - question: "Do MCP servers consume context tokens?"
      answer: "Yes. Every MCP server registers its tools in the agent's context, which uses tokens. Enable only the servers you need, and consider disabling servers globally and enabling them per-agent to keep context lean."
    - question: "Can I use OAuth with MCP servers in OpenCode?"
      answer: "Yes. OpenCode supports automatic OAuth flows for remote MCP servers. It detects 401 responses, handles Dynamic Client Registration (RFC 7591), and stores tokens securely in ~/.local/share/opencode/mcp-auth.json."
---

OpenCode ships with strong built-in tools — file read/write, bash, search, grep — but real development work touches external systems: issue trackers, documentation search, error monitoring. The Model Context Protocol (MCP) is how you bridge that gap. Once you configure an MCP server, its tools appear alongside OpenCode's native tools, and the agent can call them without any extra prompting.

This guide walks through adding local and remote MCP servers, managing OAuth, and controlling which agents can use which tools.

<!--more-->

## What Is an MCP Server

An MCP server is an external process or API that exposes tools through the Model Context Protocol. OpenCode connects to the server, discovers its available tools, and makes them accessible to the LLM in the same way it accesses built-in tools like `bash` or `edit`.

Think of it as a plugin system: instead of reimplementing functionality inside OpenCode, you point the agent at an existing server that already knows how to query your Sentry issues, search documentation, or grep GitHub code.

There are two types:

- **Local servers** — run as a child process on your machine. The command starts when OpenCode starts and stops when it stops.
- **Remote servers** — hosted HTTP endpoints. OpenCode connects over the network and can authenticate via API keys or OAuth.

## Adding a Local MCP Server

Local servers run on your machine. You define the command that starts them, and OpenCode manages the process lifecycle.

Add this to your `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "my-local-server": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-everything"],
      "enabled": true
    }
  }
}
```

The `command` field takes an array — the executable followed by its arguments. OpenCode spawns this process and communicates with it over stdin/stdout.

### Environment Variables

Pass environment variables to the server with the `environment` field:

```json
{
  "mcp": {
    "my-server": {
      "type": "local",
      "command": ["python", "mcp_server.py"],
      "environment": {
        "API_KEY": "your-key-here",
        "DEBUG": "true"
      }
    }
  }
}
```

### Working Directory

Use `cwd` to set the server's working directory. Relative paths resolve from your workspace root:

```json
{
  "mcp": {
    "project-server": {
      "type": "local",
      "command": ["./scripts/mcp-bridge"],
      "cwd": "./tools"
    }
  }
}
```

### Timeouts

By default, OpenCode waits 5 seconds for a local server to register its tools. For slower servers, increase the timeout:

```json
{
  "mcp": {
    "slow-server": {
      "type": "local",
      "command": ["npx", "my-heavy-mcp"],
      "timeout": 15000
    }
  }
}
```

## Adding a Remote MCP Server

Remote servers live on the network. You point OpenCode at a URL, and it connects over HTTP.

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "enabled": true
    }
  }
}
```

### Authentication with Headers

For servers that use API keys, pass them in `headers`:

```json
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "CONTEXT7_API_KEY": "{env:CONTEXT7_API_KEY}"
      }
    }
  }
}
```

The `{env:CONTEXT7_API_KEY}` syntax reads from an environment variable at runtime — the key never appears in your config file.

### OAuth Authentication

OpenCode handles OAuth automatically for remote servers. When a server requires authentication, OpenCode detects the 401 response and initiates the OAuth flow. It uses Dynamic Client Registration (RFC 7591) when the server supports it, then stores tokens in `~/.local/share/opencode/mcp-auth.json`.

For servers where you already have client credentials:

```json
{
  "mcp": {
    "my-oauth-server": {
      "type": "remote",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "clientId": "{env:MY_CLIENT_ID}",
        "clientSecret": "{env:MY_CLIENT_SECRET}",
        "scope": "tools:read tools:execute"
      }
    }
  }
}
```

Disable OAuth entirely (for API-key-only servers) with `"oauth": false`.

### Managing OAuth Credentials

OpenCode provides CLI commands for OAuth management:

```bash
# Authenticate with a server
opencode mcp auth my-oauth-server

# List all servers and their auth status
opencode mcp list

# Remove stored credentials
opencode mcp logout my-oauth-server

# Debug connection and OAuth flow
opencode mcp debug my-oauth-server
```

## Managing MCP Tools

MCP tools register as named tools alongside OpenCode's built-in tools. You control their availability at the global and per-agent level.

### Disable Globally

If you have multiple MCP servers but only want some available to all agents:

```json
{
  "mcp": {
    "my-mcp-foo": {
      "type": "local",
      "command": ["bun", "x", "my-mcp-command-foo"]
    },
    "my-mcp-bar": {
      "type": "local",
      "command": ["bun", "x", "my-mcp-command-bar"]
    }
  },
  "tools": {
    "my-mcp*": false
  }
}
```

The glob pattern `my-mcp*` disables all tools whose names start with `my-mcp`.

### Enable Per Agent

Disable globally, then enable for specific agents. This keeps context lean — only the agents that need a server get its tools:

```json
{
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "oauth": {},
      "enabled": true
    }
  },
  "tools": {
    "sentry_*": false
  },
  "agent": {
    "code-reviewer": {
      "tools": {
        "sentry_*": true
      }
    }
  }
}
```

MCP server tools are registered with the server name as prefix. To disable all tools for a server, use `"servername_*": false`.

## Real-World Examples

Here are three MCP servers that pair well with OpenCode in practice.

### Sentry — Error Monitoring

Query issues, projects, and error data directly from your agent:

```json
{
  "mcp": {
    "sentry": {
      "type": "remote",
      "url": "https://mcp.sentry.dev/mcp",
      "oauth": {}
    }
  }
}
```

After adding the config, authenticate:

```bash
opencode mcp auth sentry
```

Then in your prompts:

```
Show me the latest unresolved issues in my project. use sentry
```

### Context7 — Documentation Search

Search through library and framework documentation:

```json
{
  "mcp": {
    "context7": {
      "type": "remote",
      "url": "https://mcp.context7.com/mcp"
    }
  }
}
```

```
Configure a Cloudflare Worker script to cache JSON API responses for five minutes. use context7
```

You can also add this to your `AGENTS.md` rules file:

```
When you need to search docs, use context7 tools.
```

### Grep by Vercel — Code Search on GitHub

Search through code snippets across open-source repositories:

```json
{
  "mcp": {
    "gh_grep": {
      "type": "remote",
      "url": "https://mcp.grep.app"
    }
  }
}
```

```
What's the right way to set a custom domain in an SST Astro component? use the gh_grep tool
```

## Context Budget Warning

MCP servers add to your context window. Each tool's description and schema consume tokens, and those tokens are available for every turn. A single well-designed server usually adds a few hundred tokens. A server with dozens of tools can add thousands.

The practical impact: if you enable too many servers, you hit context limits faster, compaction kicks in more aggressively, and the agent has less room for your actual code.

A good rule of thumb — enable the servers you need for the current task. Disable them globally and enable per-agent when the same server isn't relevant to every workflow.

> [!TIP]
> Use `"tools": { "my-mcp*": false }` globally and enable per-agent with `"tools": { "my-mcp*": true }` in your agent config. This keeps context lean while giving specific agents the tools they need.

## Overriding Remote Defaults

Organizations can provide default MCP servers through `.well-known/opencode`. These servers may be disabled by default. To opt in locally:

```json
{
  "mcp": {
    "jira": {
      "type": "remote",
      "url": "https://jira.example.com/mcp",
      "enabled": true
    }
  }
}
```

Your local config overrides the remote defaults. See the [config precedence order](https://opencode.ai/docs/config/#precedence-order) for the full chain.

## Security Considerations for MCP Servers

Adding an MCP server is like granting the agent a new permission, so treat it that way. A remote server can pass your prompts through a third-party endpoint, and a local server runs as a child process on your machine. Before you trust one, check three things:

- **Who runs the endpoint?** For remote servers, prefer first-party endpoints from the tool vendor (Sentry, GitHub, Context7). A community-hosted server is effectively a proxy into your prompts and your data.
- **What secrets can the server reach?** Never put long-lived credentials in `opencode.json`. Use `{env:VAR}` or the OAuth flow so tokens never land in the repository.
- **What can the tools do?** Read each tool's description. A single server can expose read, write, and destructive actions behind one name — disable the ones you don't need.

MCP servers only add attack surface when you enable ones you don't need. The discipline is the same one that keeps agents safe in general, covered in our explainer on [AI coding agents](/p/ai-coding-agents-explained/): trust comes from being able to see what runs, when, and with which credentials.

## Key Takeaways

- MCP servers extend OpenCode with external tools via the Model Context Protocol — local (child process) or remote (HTTP endpoint).
- Use `environment` and `{env:VAR}` to keep secrets out of config files.
- OAuth is handled automatically for remote servers; manage credentials with `opencode mcp auth` and `opencode mcp list`.
- Disable servers globally with `"tools": { "servername*": false }` and enable per-agent to control context usage.
- Start with one or two servers. Monitor context consumption before adding more.

## Conclusion

MCP is the bridge between OpenCode's agent and the rest of your toolchain. Start with one integration — Context7 for docs search or Sentry for error monitoring — and expand from there. The key constraint is context: each server you enable costs tokens, so be intentional about which agents get which tools.

Teams like F9XR use MCP to connect documentation search and error tracking without leaving the terminal, keeping context focused on the code that matters. To learn more about OpenCode's extensibility, see our [skills guide](/p/opencode-skills-guide/) and the [VS Code setup](/p/opencode-vscode-setup/). Every article we publish goes through the review standards in our [editorial policy](/editorial-policy/) — and if you have a tooling question of your own, the [contributor guide](/contribute/) is open.
