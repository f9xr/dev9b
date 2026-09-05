---
title: "How to Add OpenCode to Your VS Code"
description: "Step-by-step guide to install and configure OpenCode AI coding agent in VS Code, Cursor, and other VS Code forks for agentic AI-assisted development."
slug: opencode-vscode-setup
date: 2026-09-04
image: cover.png
author: F9XR Team
keywords:
    - OpenCode
    - VS Code
    - AI coding agent
    - VS Code extension
    - opencode CLI
    - agentic coding
categories:
    - Tutorials
tags:
    - opencode
    - vscode
    - ai-tools
    - developer-setup
draft: false
math: false
faq:
    - question: "Why does the OpenCode extension not install automatically?"
      answer: "OpenCode must run inside VS Code's integrated terminal (not an external one). Verify the CLI is available with where opencode (Windows) or which opencode (macOS/Linux), and confirm VS Code has permission to install extensions."
    - question: "OpenCode works in my terminal but VS Code says the CLI is not found - why?"
      answer: "VS Code can use a different PATH than your interactive shell. Find the full path with Get-Command opencode, then set it manually in the opencodeVisual.opencodePath VS Code setting."
    - question: "What should I check when OpenCode gives no response from the agent?"
      answer: "Verify your API key is set correctly, confirm your internet connection when using cloud providers, and open the Output panel (View > Output) selecting OpenCode from the dropdown to inspect the logs."
---

OpenCode is an open-source, terminal-based AI coding agent that supports over 75 models and runs entirely locally. It integrates natively into VS Code through its official extension — bringing agentic AI workflows directly into your editor without leaving the terminal environment you already work in.

In this guide, we will walk through installing the OpenCode CLI, enabling the VS Code extension, and configuring your environment so OpenCode can work with your preferred AI provider.

<!--more-->

## Prerequisites

Before installing OpenCode, make sure you have the following:

1. **VS Code** (any recent stable version). OpenCode runs in the integrated terminal, so no special extension is required for basic functionality.
2. **Terminal access.** OpenCode installs through your terminal — PowerShell, Command Prompt, or Windows Terminal all work.
3. **At least one AI provider.** You need access to a model. This can be a free local model through Ollama, or a cloud provider like OpenAI, Anthropic, or Google.

If you plan to use cloud providers only, you do not need to install Ollama or Go — just the pre-built binary and your API key.

## Step 1: Install the OpenCode CLI

OpenCode offers several installation methods. Pick the one that fits your setup.

### Method 1: One-Line Install (Recommended)

This works on macOS, Linux, and Windows (with WSL or PowerShell):

```bash
curl -fsSL https://opencode.ai/install | bash
```

This downloads the pre-built binary for your platform and places it in `~/.opencode/bin`.

### Method 2: npm Install

If you have Node.js installed:

```bash
npm install -g opencode-ai@latest
```

### Method 3: Homebrew (macOS/Linux)

```bash
brew install anomalyco/tap/opencode
```

### Verifying the Installation

After installation, confirm OpenCode is available:

```bash
opencode --version
```

If the command is not found, add the install directory to your PATH:

```powershell
# PowerShell (Windows)
$env:PATH += ";$env:USERPROFILE\.opencode\bin"

# Or permanently via System Properties → Environment Variables
```

On macOS/Linux, add to your shell profile:

```bash
echo 'export PATH="$HOME/.opencode/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Step 2: Configure Your AI Provider

Before OpenCode can help you write code, it needs access to a model. Run OpenCode and use the built-in setup:

```bash
opencode
```

Then run:

```
/connect
```

Select your provider and enter your API key. Supported providers include:

| Provider | Model Examples | Free Tier |
|----------|---------------|-----------|
| Anthropic | Claude 3.5 Sonnet, Claude 4 | No |
| OpenAI | GPT-4o, o1, o3 | No |
| Google | Gemini 2.5 Pro, Gemma 4 | Yes (limited) |
| Ollama (local) | DeepSeek Coder, Llama 3.3 | Yes (local) |

For a completely free, offline setup, install [Ollama](https://ollama.com) and pull a coding model:

```bash
ollama pull deepseek-coder-v2
```

Then configure OpenCode to use it via the `/connect` menu.

## Step 3: Install the VS Code Extension

The OpenCode VS Code extension integrates the full agent experience into your editor. There are two ways to install it.

### Automatic Install (Easiest)

1. Open VS Code
2. Open the integrated terminal (`Ctrl+Backtick`)
3. Run `opencode`

The extension installs automatically on first run. That is it — no manual steps needed.

### Manual Install

If the automatic install fails or you prefer the marketplace:

1. Open VS Code
2. Press `Ctrl+Shift+X` to open Extensions
3. Search for **"OpenCode"**
4. Click **Install** on the extension by SST (publisher: `sst-dev`)

Or from the command line:

```powershell
code --install-extension sst-dev.opencode
```

## Step 4: Using OpenCode in VS Code

Once installed, OpenCode lives in your terminal panel. Here are the key shortcuts:

| Action | Shortcut |
|--------|----------|
| Open OpenCode (split terminal) | `Ctrl+Esc` |
| Start new session | `Ctrl+Shift+Esc` |
| Insert file reference | `Alt+Ctrl+K` |

You can also click the **OpenCode button** in the terminal toolbar to launch it.

### How It Works in Practice

OpenCode runs as a terminal agent inside your editor. When you ask it to modify a file, it reads the file, generates the change, and applies it — all through the terminal. The extension adds context awareness, so your current file or selection is automatically shared with the agent.

For example, you can ask OpenCode to:

- Refactor a function and explain the changes
- Write unit tests for a specific file
- Debug an error by reading logs and suggesting fixes
- Generate boilerplate code based on your project structure

The agent has access to your filesystem through built-in tools, so it can read, write, and execute commands on your behalf.

## Step 5: Workspace Configuration

OpenCode reads configuration from an `opencode.json` file in your project root. Create one to set project-specific defaults:

```json
{
  "model": "anthropic/claude-sonnet-4-20250514",
  "permissions": {
    "bash": "auto-approve"
  }
}
```

This tells OpenCode which model to use and what permissions to grant automatically. You can also configure MCP servers, custom agents, and plugin settings in this file.

The global configuration lives at `~/.config/opencode/opencode.json` and applies to all projects.

## Works With Other VS Code Forks

OpenCode works identically in Cursor, Windsurf, and VSCodium. The installation process is the same — just make sure the CLI command for your IDE is available:

- **Cursor:** `cursor` command
- **Windsurf:** `windsurf` command
- **VSCodium:** `codium` command

If the CLI is not on your PATH, run `Ctrl+Shift+P` and search for "Shell Command: Install 'code' command in PATH" (or the equivalent for your IDE).

## Troubleshooting

### Extension fails to install automatically

- Make sure you are running `opencode` in the **integrated terminal**, not an external one.
- Confirm the CLI is available: run `where opencode` (Windows) or `which opencode` (macOS/Linux).
- Ensure VS Code has permission to install extensions.

### CLI not found in VS Code but works in terminal

VS Code may use a different PATH than your interactive shell. Find the full path:

```powershell
Get-Command opencode
```

Then set it in VS Code settings under `opencodeVisual.opencodePath`.

### No response from the agent

- Verify your API key is set correctly.
- Check your internet connection if using cloud providers.
- Open the Output panel (`View → Output`) and select "OpenCode" from the dropdown to see logs.

## Key Takeaways

- OpenCode installs via a one-liner and integrates into VS Code's terminal automatically.
- The official extension gives you context-aware shortcuts and file references.
- Works with 75+ models, including free local models through Ollama.
- Configuration lives in `opencode.json` per project or globally in `~/.config/opencode/`.
- Compatible with VS Code, Cursor, Windsurf, and VSCodium.

## Conclusion

Adding OpenCode to your VS Code setup takes less than five minutes. Once configured, you get an agentic AI assistant that reads your code, writes changes, runs commands, and explains its reasoning — all from within the terminal you already use. Teams like F9XR use this kind of setup to speed up code review and prototyping without introducing new tools into the workflow.

Ready to contribute? Check the [Contributor Guide](/contribute/) to submit your own article to Dev9b.
