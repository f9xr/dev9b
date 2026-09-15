---
title: "OpenCode TUI Setup: Full Terminal Guide for Devs"
description: "Learn how to install, configure, and master the OpenCode TUI. Step-by-step setup, keybinds, commands, and tips for terminal-based AI coding."
slug: how-to-setup-opencode-tui
date: "2026-09-14T00:10:00+05:30"
image: cover.jpg
author: F9XR Team
keywords:
    - OpenCode
    - terminal user interface
    - AI coding agent
    - developer tools
    - terminal development
categories:
    - Tutorials
tags:
    - opencode
    - terminal-user-interface
    - tui
    - ai-coding-agent
    - developer-tools
    - cli-tools
    - terminal-development
    - coding-assistant
    - devops
    - software-development
draft: false
math: false
faq:
    - question: "What is the OpenCode TUI?"
      answer: "The OpenCode TUI is the interactive terminal interface for OpenCode, an open-source AI coding agent. It lets you chat with an LLM, reference project files, run shell commands, and manage coding sessions entirely inside your terminal."
    - question: "How do I install OpenCode?"
      answer: "Run 'curl -fsSL https://opencode.ai/install | bash' on macOS or Linux, or install it through a package manager like npm install -g opencode-ai@latest, Homebrew (brew install sst/tap/opencode), or the AUR on Arch Linux. Windows users should install it inside WSL for the best experience."
    - question: "How do I start the OpenCode TUI?"
      answer: "Navigate to your project folder and run 'opencode' in your terminal. To launch it against a specific directory without changing your current path, run 'opencode /path/to/project' instead."
    - question: "How do I connect an API key to OpenCode?"
      answer: "Run /connect inside the TUI, or opencode auth login from your terminal outside the TUI. Both open a provider picker where you can select Anthropic, OpenAI, Google, or another supported provider and enter your API key."
    - question: "Does OpenCode require a paid subscription?"
      answer: "No. OpenCode is open source and works with your own API keys from any supported provider. OpenCode Zen offers a curated, usage-based model list as an alternative for those who prefer not to manage individual provider keys."
    - question: "Why doesn't undo or redo work in the OpenCode TUI?"
      answer: "Undo and redo are backed by Git internally, so your project folder must be an initialized Git repository. Run git init in the project directory if it isn't one already."
    - question: "Can I customize the OpenCode TUI's appearance and keybinds?"
      answer: "Yes. Create a tui.json file to set your theme, leader key, scroll behavior, diff style, cursor style, and notification settings. Use the OPENCODE_TUI_CONFIG environment variable to point OpenCode at a custom config file path."
---

If you spend most of your day in a terminal anyway, switching to a browser tab every time you need help from an AI coding assistant feels like a waste of a keystroke. That's the whole pitch behind OpenCode: an open-source coding agent that lives right where you already work, with a terminal user interface (TUI) built for real development workflows instead of chat-window busywork.

This guide walks through everything you need to get the OpenCode TUI running: installation, connecting your first LLM provider, the commands and keybinds you'll actually use daily, and the config tweaks that make the interface feel like it was built for your setup specifically. Whether you're coming from Cursor, Copilot, or plain old vim plus a browser tab, you'll have a working session in a few minutes.

<!--more-->

## What Is the OpenCode TUI?

OpenCode is an open-source coding agent that runs directly in your terminal and supports dozens of LLM providers, including Anthropic, OpenAI, Google, and local models. The TUI is the interactive front end: a full-screen terminal interface where you chat with the model, review diffs, run shell commands, and manage sessions, all without leaving your keyboard.

Unlike a plain CLI tool where you run one command and get one output, the TUI keeps a persistent, scrollable conversation open. You can reference files, run bash commands inline, switch models mid-session, and undo changes with full Git-backed history. It's closer to an IDE panel than a traditional command-line utility, just rendered entirely in text.

### TUI vs CLI Mode

It helps to separate the two ways you can use OpenCode:

| Mode | Command | Use case |
|---|---|---|
| CLI (one-shot) | `opencode run "explain this function"` | Quick, scriptable, non-interactive tasks |
| TUI (interactive) | `opencode` | Ongoing sessions, multi-turn conversations, code edits |

Most day-to-day work happens in the TUI, since that's where session history, undo/redo, and file context management actually live. If you're still deciding whether OpenCode is the right agent for you, our [AI Coding Agents Explained](https://f9xr.org/p/ai-coding-agents-explained/) piece and the [OpenCode vs Cursor](https://f9xr.org/p/opencode-vs-cursor/) comparison cover the trade-offs in detail.

## Prerequisites Before You Start

Before installing, make sure you have:

* A modern terminal emulator with truecolor support (iTerm2, Kitty, Alacritty, Windows Terminal, or the default terminals on most current Linux distros all work fine)
* macOS, Linux, or Windows via WSL (WSL is strongly recommended over native Windows for the smoothest experience)
* At least one LLM provider account and API key, such as Anthropic, OpenAI, or Google, or a plan through OpenCode Zen if you'd rather not juggle separate keys
* Git installed, since undo and redo inside the TUI rely on Git to track file changes

You can check truecolor support quickly with:

```bash
echo $COLORTERM
```

If that returns `truecolor`, you're set. If it returns nothing, look up how to enable 24-bit color for your specific terminal before moving on, since the TUI's diff rendering and themes depend on it.

## Installing OpenCode

There are several ways to install OpenCode depending on your platform and preferences. Pick whichever fits your existing toolchain.

### Quick Install Script

The fastest route on macOS or Linux:

```bash
curl -fsSL https://opencode.ai/install | bash
```

### Using a Package Manager

If you'd rather manage it through a package manager you already use:

```bash
npm install -g opencode-ai@latest
```

```bash
bun install -g opencode-ai@latest
```

```bash
pnpm add -g opencode-ai@latest
```

```bash
yarn global add opencode-ai@latest
```

macOS and Linux users can also go through Homebrew:

```bash
brew install sst/tap/opencode
```

Arch Linux users have an AUR package available:

```bash
paru -S opencode-bin
```

### Windows Setup

Native Windows support is limited, so WSL is the recommended path. Install WSL2 with a Linux distro of your choice, then run the same curl or npm install command inside that WSL environment. If you'd rather stay on native Windows tooling, Scoop and Chocolatey packages are also available.

Once installed, confirm it worked with:

```bash
opencode --version
```

## Launching the TUI for the First Time

Navigate into any project directory and start OpenCode:

```bash
cd ~/your-project
opencode
```

This launches the TUI scoped to that folder. You can also point it at a specific path without changing directories first:

```bash
opencode /path/to/project
```

The first time it opens, you'll land on a blank prompt. Try something simple to confirm everything is wired up correctly:

```
Give me a quick summary of the codebase.
```

If the model responds with a coherent summary of your project structure, your setup is working end to end.

## Connecting Your LLM Provider

Before OpenCode can do anything useful, it needs an API key. The cleanest way to do this is from inside the TUI itself:

```
/connect
```

This opens a provider picker where you select Anthropic, OpenAI, Google, or any other supported provider and paste in your API key. Credentials are saved locally to `~/.local/share/opencode/auth.json`, so you only need to do this once per machine. The full list of supported providers lives in the [official providers docs](https://opencode.ai/docs/providers/).

You can also run the same flow from outside the TUI:

```bash
opencode auth login
```

Once connected, use `/models` inside the TUI to browse and switch between the models available to your account. If you don't want to manage individual provider keys, OpenCode Zen offers a curated, pay-as-you-go model list as an alternative.

## Core Commands and Keybinds

Everything inside the TUI is accessible through slash commands, and most of them have a matching keybind built on a leader key (`ctrl+x` by default). Learning even five or six of these will noticeably speed up your workflow. The full, current keybind reference is maintained in the [official keybinds docs](https://opencode.ai/docs/keybinds/).

| Command | What it does | Default keybind |
|---|---|---|
| `/connect` | Add or switch an LLM provider | — |
| `/models` | List and switch available models | `ctrl+x m` |
| `/new` | Start a fresh session (alias `/clear`) | `ctrl+x n` |
| `/sessions` | List and switch between saved sessions | `ctrl+x l` |
| `/undo` | Revert the last message and any file changes | `ctrl+x u` |
| `/redo` | Reapply an undone change | `ctrl+x r` |
| `/compact` | Summarize a long session to save context | `ctrl+x c` |
| `/themes` | Switch the TUI color theme | `ctrl+x t` |
| `/editor` | Open your `$EDITOR` for composing a longer message | `ctrl+x e` |
| `/export` | Export the conversation to Markdown | `ctrl+x x` |
| `/init` | Generate or update an `AGENTS.md` file for your project | — |
| `/details` | Toggle tool execution details on or off | — |
| `/help` | Open the full command list | — |
| `/exit` | Quit OpenCode (alias `/quit`, `/q`) | `ctrl+x q` |

A quick tip: `/undo` and `/redo` both rely on Git under the hood, so they only work correctly inside an initialized Git repository. If you're testing OpenCode in a throwaway folder, run `git init` first or you'll lose that safety net.

## Working Inside the TUI: Files, Bash, and Modes

### Referencing Files with @

Type `@` followed by a path (or a partial name for fuzzy search) to pull a file's contents directly into the conversation:

```
How is auth handled in @packages/functions/src/api/index.ts?
```

The model reads the actual file content, so there's no need to copy-paste code manually. If you've configured named references, typing `@alias/` will autocomplete files inside that reference root, which is handy for large monorepos where the file you want is buried a few directories deep.

### Running Shell Commands Inline

Prefix any message with `!` to execute it as a shell command, with the output automatically added back into the conversation:

```
!ls -la
```

This is genuinely useful for quick checks, running tests, or grepping logs, without breaking your flow to open a second terminal pane.

### Plan Mode vs Build Mode

Use `Tab` to switch between two working modes:

* **Plan mode**: read-only, the model proposes changes but doesn't touch your files
* **Build mode**: the model applies edits directly, after showing you the diff and asking for confirmation on anything destructive

Sticking to Plan mode for exploratory or risky refactors, then flipping to Build mode once you're confident in the approach, is a solid habit for anyone still building trust with an AI agent's judgment.

## Setting Up AGENTS.md for Your Project

Run `/init` from inside the TUI to generate an `AGENTS.md` file at your project root. This file gets analyzed automatically in future sessions and teaches the model your project's conventions, folder structure, testing setup, and any house rules you want it to follow. It's roughly the equivalent of onboarding documentation, except the model actually reads it every time.

If your project already has strong conventions (a specific commit message format, a preferred testing library, strict linting rules), spelling those out in `AGENTS.md` cuts down significantly on back-and-forth corrections later.

Once the TUI basics are comfortable, the natural next step is teaching OpenCode your project's reusable workflows — check out our [OpenCode Skills Guide](https://f9xr.org/p/opencode-skills-guide/) for that.

## Customizing the TUI

Once the basics are working, you can tune the interface through a `tui.json` (or `tui.jsonc`) config file. Here's a reasonable starting point:

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "opencode",
  "leader_timeout": 2000,
  "keybinds": {
    "leader": "ctrl+x",
    "command_list": "ctrl+p"
  },
  "scroll_speed": 3,
  "diff_style": "auto",
  "cursor": {
    "style": "block",
    "blinking": true
  },
  "mouse": true,
  "attention": {
    "enabled": true,
    "notifications": true,
    "sound": true,
    "volume": 0.4
  }
}
```

A few settings worth knowing about:

* `diff_style` set to `stacked` forces a single-column diff view, which is easier to read on narrower terminal windows
* `scroll_acceleration.enabled` gives you macOS-style scrolling that speeds up on rapid gestures and stays precise on slow ones; when it's on, it overrides `scroll_speed` entirely
* `attention.enabled` turns on desktop notifications and sounds when OpenCode needs your input or finishes a long-running task, which is genuinely useful if you tab away while a big refactor runs

This config file is separate from `opencode.json`, which handles server and runtime behavior rather than the interface itself, so don't mix the two up when troubleshooting. The [official TUI docs](https://opencode.ai/docs/tui/) are the primary reference for every current option.

## Practical Tips for a Smoother Workflow

* **Initialize Git before your first session.** Undo and redo depend on it, and you'll want that safety net from day one, not after your first bad edit.
* **Use `/compact` on long sessions.** Once a conversation gets long, context quality can degrade. Summarizing periodically keeps responses sharp.
* **Set a real `$EDITOR`.** Both `/editor` and `/export` use it, so point it at something you're comfortable in, and remember GUI editors like VS Code need the `--wait` flag.
* **Write a proper `AGENTS.md`.** Five minutes spent documenting your conventions saves much more time correcting AI-generated code that doesn't match your style.
* **Check terminal color support early.** A terminal without truecolor will render themes and diffs incorrectly, and it's an easy thing to rule out before assuming OpenCode itself is broken.
* **Keep Plan mode as your default for unfamiliar codebases.** It costs nothing to review a proposed change before letting the agent touch files directly.

In our own workflow at F9XR, the Git-first habit is the one we'd press hardest. A `/undo` you can trust changes how freely you let the agent experiment, and that safety net comes entirely from a two-second `git init`.

## Troubleshooting Common Setup Issues

**The TUI opens but input doesn't respond.** This is often caused by a plugin listed in your config that isn't actually installed in `node_modules`. Remove the unused plugin entry or install it properly, then restart.

**Colors or diffs look broken.** Almost always a terminal truecolor issue. Confirm with `echo $COLORTERM` and switch terminal emulators if needed.

**Undo or redo doesn't do anything.** Your project folder needs to be a Git repository for either command to function, since both are backed by Git history.

**Model responses feel slow or context feels off.** Try `/compact` to summarize the session, or start a fresh one with `/new` if the conversation has drifted far from the current task.

## Key Takeaways

* OpenCode's TUI is a full-screen, interactive terminal interface for AI-assisted coding, distinct from its one-shot CLI mode.
* Install it with the official curl script, or through npm, bun, pnpm, yarn, Homebrew, or the AUR, depending on your platform.
* Connect a provider with `/connect` inside the TUI, or `opencode auth login` from the command line; credentials are stored locally.
* Learn the core commands: `/models`, `/new`, `/sessions`, `/undo`, `/redo`, `/compact`, and `/init` cover most daily workflows.
* Reference files with `@`, run shell commands with `!`, and toggle between Plan and Build mode with `Tab` for safer edits.
* Customize behavior through `tui.json`, including themes, keybinds, scroll settings, and attention notifications.
* Undo, redo, and a smooth workflow all depend on your project being a proper Git repository, so initialize Git before you start.

## Frequently Asked Questions

### What is the OpenCode TUI?

The OpenCode TUI is the interactive terminal interface for OpenCode, an open-source AI coding agent. It lets you chat with an LLM, reference project files, run shell commands, and manage coding sessions entirely inside your terminal.

### How do I install OpenCode?

Run `curl -fsSL https://opencode.ai/install | bash` on macOS or Linux, or install it through a package manager like `npm install -g opencode-ai@latest`, Homebrew (`brew install sst/tap/opencode`), or the AUR on Arch Linux. Windows users should install it inside WSL for the best experience.

### How do I start the OpenCode TUI?

Navigate to your project folder and run `opencode` in your terminal. To launch it against a specific directory without changing your current path, run `opencode /path/to/project` instead.

### How do I connect an API key to OpenCode?

Run `/connect` inside the TUI, or `opencode auth login` from your terminal outside the TUI. Both open a provider picker where you can select Anthropic, OpenAI, Google, or another supported provider and enter your API key.

### Does OpenCode require a paid subscription?

No. OpenCode is open source and works with your own API keys from any supported provider. If you'd rather not manage keys directly, OpenCode Zen offers a curated, usage-based model list as an alternative.

### Why doesn't undo or redo work in the OpenCode TUI?

Undo and redo are backed by Git internally, so your project folder must be an initialized Git repository. Run `git init` in the project directory if it isn't one already.

### Can I customize the OpenCode TUI's appearance and keybinds?

Yes. Create a `tui.json` file to set your theme, leader key, scroll behavior, diff style, cursor style, and notification settings. Use `OPENCODE_TUI_CONFIG` if you want to point OpenCode at a custom config file path.

---

*This guide was researched and drafted with the assistance of an AI coding assistant, then reviewed by the F9XR Review Board before publishing. Have feedback or want to contribute your own article? See our [Contributor Guide](/contribute/) and [Editorial Policy](/editorial-policy/).*