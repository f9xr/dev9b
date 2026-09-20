---
title: "AI Coding Agents Explained: How They Work"
description: "AI coding agents explained: how they plan, use tools, and learn from your codebase — with real examples from OpenCode."
slug: ai-coding-agents-explained
date: 2026-09-05
image: cover.png
author: F9XR Team
keywords:
    - AI coding agent
    - agentic coding
    - OpenCode
    - LLM
    - tools
categories:
    - Tutorials
tags:
    - opencode
    - ai-tools
    - introduction
draft: false
math: false
faq:
    - question: "What is the difference between a chatbot and an AI coding agent?"
      answer: "A chatbot answers questions. An agent also acts — it reads files, runs commands, edits code, and checks its own results, using the terminal and your workspace as its hands."
    - question: "Are AI coding agents safe to grant file and command access?"
      answer: "Most agents gate every action behind permission prompts and deny rules. You stay in control of what is read, written, and executed on your machine."
    - question: "Do AI coding agents learn from your code over time?"
      answer: "Agents do not persist learning between sessions by default. Instead they re-read your files each session, and tools like OpenCode skills store conventions you define for them to follow."
---
Every few months someone packages the same idea under a new name — autocomplete became pair-programmers, became agents. But an AI coding agent is a genuinely different thing from the chat window you are used to: it does not just answer, it does.

Understanding how these agents are built changes how you use them, how you prompt them, and how much you can safely trust them. This guide breaks down the anatomy of an agent — no marketing, no hype.

<!--more-->

## The Core Loop: Plan, Act, Check

Strip away the branding and an AI coding agent is a loop with three repeating phases:

1. **Plan** — the model asks what it needs to do, in what order, and what it does not know yet.
2. **Act** — it calls tools: reading a file, running a search, executing a terminal command, writing an edit.
3. **Check** — it inspects output, errors, and diffs, then decides whether the goal is met or the plan needs another pass.

Each iteration feeds back into the next. The agent never leaves the terminal in the way the plan expects, so it notices — that is what makes it an agent instead of a script.

## The Five Parts of Any Agent

```mermaid
mindmap
  root((AI coding agent))
    Model core
        LLM reasoning
        Context window
        Provider access
    Memory
        Project context
        Session state
        Skills and rules
    Tools
        Read and write files
        Run terminal commands
        Search codebase
    Permission layer
        Ask before acting
        Deny rules
        Allowed commands
    Feedback loop
        Inspect output
        Parse errors
        Revise plan
```

And as plain text, the same map:

```
AI coding agent
  - Model core
    - LLM reasoning
    - Context window
    - Provider access
  - Memory
    - Project context
    - Session state
    - Skills and rules
  - Tools
    - Read and write files
    - Run terminal commands
    - Search codebase
  - Permission layer
    - Ask before acting
    - Deny rules
    - Allowed commands
  - Feedback loop
    - Inspect output
    - Parse errors
    - Revise plan
```

### 1. The Model Core

Every agent is an LLM at heart, wrapped in scaffolding. The same model can behave completely differently depending on how much of your codebase fits in its context and how the agent formats its thinking. This is why OpenCode supports 75+ models — the scaffolding is stable, and you choose the brain.

### 2. Memory

Agents have no lifelong memory. Each session re-reads what it needs. Three things do persist: your project files, the session's own edits, and **skills** — reusable instruction files you write once so the agent keeps following your conventions. That is the trick behind the [OpenCode skills guide](/p/opencode-skills-guide/): you encode memory, the agent applies it.

### 3. Tools

Tools are how an agent touches the real world. The standard set: file reads and edits, terminal commands, codebase search, and sometimes web fetches or issue lookups. Tools are where most of the practical difference between agents lives — a tool layer that understands git and package managers behaves like a developer, not a typist.

### 4. The Permission Layer

Safe agents gate every dangerous action behind a consent prompt or a deny rule. Our own denial experience: you set permissions in `opencode.json`, allow trusted commands, and deny the rest. The agent asks; you approve; nothing runs silently. This is the single most important feature to verify before letting an agent near a repository you care about.

### 5. The Feedback Loop

The final piece reads the outcomes. Did the command succeed? Does the test pass? Instead of assuming, the agent parses stderr, re-runs, and revises. Agents that skip this step are just autocomplete with extra steps.

## A Real Session, Top to Bottom

In practice a session looks like: you ask OpenCode to add a feature across two files. It lists the files it wants to read, reads them, writes a sketch, runs the build, notices a broken import it introduced, fixes it, replaces a hardcoded value with a config lookup, and hands you a diff. Every step was visible, every command was approved, and the agent corrected its own mistake without being asked.

## Why Context Is the Real Constraint

The myth is that agents fail because the model is weak. In practice the bottleneck is context. An LLM reasons over whatever fits in its context window, so an agent's quality tracks how well it feeds the model the right information at the right time. Three techniques separate good agents from average ones:

- **Selective reads.** The agent reads only the files relevant to the current step instead of dumping the whole repository into the window.
- **Search before read.** Codebase search finds the relevant symbols first, then the agent opens a handful of files rather than dozens.
- **Summarization.** Long outputs are compressed before they feed back in, keeping useful signal inside a shrinking window.

This is why the tool layer matters as much as the model: a search tool that understands your framework produces better decisions than a larger model with a blind toolset.

## When Agents Get It Wrong

Agents fail in predictable ways, and knowing them makes you a better operator:

- **Stale context.** The agent reasons from an earlier file version and edits code that has moved. The fix is a fresh read — most agents re-read on their own if you tell them what changed.
- **Missing feedback.** An agent that skips parsing its own output "succeeds" on wrong results. Verify it actually inspects output before you trust it in production.
- **Permission clutter.** Over-permissioned agents run more, break more, and are harder to audit. Start deny-by-default and add commands only as the work demands.

Each failure is a clue about the tool, not the technology. A mature agent makes these failures visible and rare; a sloppy one hides them behind a confident summary.

## Evaluating an Agent for Your Team

Before you standardize on any agent, run the same five-question test:

1. Can it read and edit files, run commands, and search the codebase?
2. Does every dangerous action go through a permission prompt or a deny rule?
3. Does it inspect the output of what it ran, or only report what it intended?
4. Can your conventions be encoded (skills or rules) and versioned in the repository?
5. What happens when the model you use today gets worse, pricier, or discontinued?

This site has a recommended path for every part of the stack: the [OpenCode TUI setup](/p/how-to-setup-opencode-tui/), the [VS Code setup](/p/opencode-vscode-setup/), and the [skills guide](/p/opencode-skills-guide/) for encoding your conventions.

## Key Takeaways

- An agent is a plan-act-check loop, not a chat box.
- Five components decide capability and safety: model, memory, tools, permissions, feedback.
- Agents re-read your codebase each session — skills are how you give them lasting conventions.
- Permission gating is a feature, not a nuisance; check it before trusting any agent.

## Conclusion

Agents are young, but the mental model is stable: a reasoning model wrapped in tools, bounded by permissions, that checks its own work. Try it on a small project first — install [OpenCode in VS Code](/p/opencode-vscode-setup/), watch it work, and keep our [contributor guide](/contribute/) in mind if you want to write up what you learn. Guides like this one are reviewed against the standards in our [editorial policy](/editorial-policy/).