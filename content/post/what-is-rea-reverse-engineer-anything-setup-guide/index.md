---
title: "What is REA? Reverse Engineer Any App with AI"
description: "Learn what REA (Reverse Engineer Anything) is, how the morluto/rea repo works, and how to set it up with Claude, Codex, or Cursor to reverse engineer any app."
slug: what-is-rea-reverse-engineer-anything-setup-guide
date: 2026-10-17
image: cover.jpg
author: F9XR Team
keywords: rea, reverse engineer, morluto rea, ai reverse engineering, mcp, claude code, ghidra, hopper, ai coding agents
categories:
    - Tutorials
tags:
    - ai-tools
    - mcp
    - developer-setup
    - ai-coding-agents
draft: false
math: false
faq:
    - question: "What does REA stand for?"
      answer: "REA stands for Reverse Engineer Anything. The official repository is morluto/rea on GitHub."
    - question: "Does REA decompile code itself?"
      answer: "No. REA is a connector and orchestration layer. It drives existing tools such as Ghidra, Hopper, IDA, and JADX, then returns structured results with evidence to your AI agent."
    - question: "Which AI agents work with REA?"
      answer: "Claude Code, Codex, Cursor, Gemini CLI, Grok Build, and any other agent that supports local MCP servers. The setup command detects and configures the ones you have installed."
    - question: "Is analysis performed in the cloud?"
      answer: "No. All analysis runs on your machine. Findings and evidence stay local."
    - question: "Do I need Ghidra or Hopper installed?"
      answer: "For pure JavaScript and Electron static analysis you do not. For native binaries you need at least one of Hopper, Ghidra, or IDA. REA can optionally help install Hopper during setup if you approve it."
    - question: "Is REA free and open source?"
      answer: "Yes. It is released under the MIT license. The official sources are the morluto/rea GitHub repository and the rea-agents npm package."
---
<!--more-->

If you've spent any time on GitHub Trending recently, you've likely seen **morluto/rea**. It quickly climbed past hundreds of thousands of stars and became one of the most talked-about open-source projects of 2026.

REA stands for **Reverse Engineer Anything**. It is not another decompiler. It is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server and CLI that hands your [AI coding agent](/p/ai-coding-agents-explained/) the tools it needs to inspect real software without source code. Native binaries, Electron apps, JavaScript bundles, .NET assemblies, Android packages, and even live websites all become fair game.

## What Exactly Is REA?

REA is an open-source toolkit created by the GitHub user **morluto**. The official repository is [github.com/morluto/rea](https://github.com/morluto/rea), and the npm package is called **rea-agents**.

At its core, REA does three things:

1. Registers itself as an MCP server with your coding agent (Claude Code, Codex, Cursor, Gemini CLI, Grok Build, and others).
2. Connects that agent to existing reverse-engineering tools such as [Ghidra](https://ghidra-sre.org), [Hopper](https://www.hopperapp.com), IDA, JADX, and browser instrumentation.
3. Returns every finding with explicit evidence and a clear list of what is still unknown.

The project's tagline captures the idea perfectly: "See a feature you like. Understand how it works, down to the binary level."

REA does not invent a new decompiler. It orchestrates the tools you already have (or can install) and lets the agent drive them through a clean, structured interface. Analysis stays local, and nothing is sent to a remote server for disassembly.

## Why REA Went Viral So Fast

Traditional reverse engineering is slow and specialized. You open Ghidra or Hopper, set breakpoints, dig through assembly, and manually piece the logic together. REA turns that process into a conversation with an AI agent.

You can say something like: *"Look at the Windows Calculator binary and explain how the percentage button is implemented."*

The agent then uses REA to open the binary, extract relevant procedures, return pseudocode and assembly with evidence, and keep asking follow-up questions until the behavior is clear. This loop is what made the project explode.

## What You Can Analyze with REA

| Target Type | Tools / Approach Used | What You Get |
|---|---|---|
| Native binaries | Ghidra, Hopper, IDA, Rizin | Pseudocode, assembly, strings, symbols, call graphs |
| JavaScript / Electron | Static analysis + source-map recovery | Modules, imports, routes, IPC, native add-ons |
| .NET assemblies | Metadata + CIL inspection | Types, methods, dependencies, build comparisons |
| Android packages | JADX and related tooling | Decompiled Java/Kotlin, resources, manifests |
| Websites / web apps | Browser instrumentation | Runtime behavior, network calls, DOM structure |
| Firmware / other formats | Binwalk, Unblob, and specialized paths | File system extraction, binary analysis |

Static JavaScript analysis works without any native decompiler. Native binary work needs Hopper, Ghidra, or IDA installed.

## How REA Works Under the Hood

1. Your agent decides it needs to inspect a target.
2. It calls the REA MCP tools.
3. REA launches or reuses the appropriate analysis engine locally.
4. Findings come back with evidence (addresses, strings, code snippets) and a list of remaining unknowns.
5. The agent uses that evidence to ask better questions or to start implementing a recreated version.

Because everything stays local and every claim is backed by evidence, the agent is less likely to hallucinate how a feature works.

## How to Set Up REA

### Requirements

- Node.js 22.19 or newer
- An AI coding agent that supports local MCP servers (Claude Code, Codex, Cursor, etc.)
- Optional but recommended for native work: Hopper, Ghidra, or IDA already installed

### One-Command Setup

The official and recommended way is:

`ash
npx rea-agents@latest setup
`

Or with Bun:

`ash
bunx rea-agents@latest setup
`

The setup wizard will detect the agents you have installed, show you the exact configuration changes it plans to make, create backups of existing MCP config, register the REA MCP server, and install the matching agent workflow instructions and skills.

### Verify the Installation

Once your agent restarts, ask it:

> "What REA tools do you currently have available?"

The agent should list tools related to binary analysis, JavaScript application inspection, and evidence retrieval.

## Practical Tips for Getting Good Results

- Start with a clear, narrow question. "Explain how the save dialog works" is better than "reverse engineer this entire app."
- Always ask the agent to show the evidence. REA is designed to surface it.
- For Electron apps, extract the ASAR first or point REA at the unpacked resources folder.
- Keep Hopper or Ghidra open in the background if you plan to do a lot of native analysis. REA reuses running instances when possible.
- Treat the output as a starting point, not gospel. Cross-check critical findings.
- Respect software licenses and terms of service. REA is a research tool, not a license to steal code.

## Common Workflows

1. **Feature recreation** – See a nice UI interaction in a closed-source app, reverse the relevant code paths, and re-implement it cleanly.
2. **Security research** – Trace how a binary handles input or stores secrets, with full evidence trails.
3. **Migration help** – Understand how an old .NET or Electron app is structured so you can rebuild it in a modern stack.
4. **Learning** – Use REA as a tutor that walks you through real-world binaries instead of toy examples.

## Key Takeaways

- REA is an MCP server and CLI that lets AI agents reverse engineer software without source code.
- It does not replace Ghidra or Hopper. It connects your agent to them and returns evidence-backed findings.
- Setup is a single command: 
px rea-agents@latest setup.
- Analysis runs completely locally.
- Always verify critical results and respect legal boundaries.

## Conclusion

REA changes the speed at which a competent developer can understand closed-source software. Used carefully and legally, it's one of the most useful tools in the AI agent ecosystem this year. If you're looking to extend your agent setup further, check out our guides on [connecting MCP servers to OpenCode](/p/opencode-mcp-servers/) and [setting up an AI coding agent](/p/ai-coding-agents-explained/). For more educational content like this, see our [Contributor Guide](/contribute/) and [Editorial Policy](/editorial-policy/).
