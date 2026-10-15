---
title: "Write & Run Batch Files on Windows and Mac"
description: "Learn how developers write and run batch files (.bat/.cmd) on Windows and shell scripts (.sh/.command) on Mac. Step-by-step commands, tips, and examples."
slug: write-run-batch-files-windows-mac
date: 2026-10-15
image: cover.jpg
author: F9XR Team
keywords:
    - batch file
    - windows batch
    - .bat
    - .cmd
    - shell script
    - mac shell script
    - zsh
    - bash
    - command prompt
    - terminal automation
categories:
    - Tutorials
tags:
    - automation
    - developer-setup
    - developer-tools
draft: false
math: false
faq:
    - question: "What is the difference between .bat and .cmd on Windows?"
      answer: "Both run under cmd.exe. The main practical difference is how some built-in commands update ERRORLEVEL. .cmd files set ERRORLEVEL to 0 on success for commands such as set and path. Most developers can treat them as interchangeable."
    - question: "Do I need administrator rights to run a batch file?"
      answer: "Only if the commands inside the file require elevated privileges, such as writing to protected folders or changing system settings. Right-click the file and choose Run as administrator when you need it."
    - question: "Why does my Mac script say Permission denied?"
      answer: "The execute bit is missing. Run chmod +x yourscript.sh in Terminal. If the script itself needs root, prefix the run command with sudo."
    - question: "Can I run a Windows batch file on Mac or vice versa?"
      answer: "No. The languages and interpreters are different. You would need to rewrite the commands for the target platform or use a cross-platform language such as Python."
    - question: "How do I pass arguments to a batch or shell script?"
      answer: "On Windows, call myscript.bat arg1 arg2 and read %1 and %2 inside the file. On Mac, call ./myscript.sh arg1 arg2 and read $1 and $2 inside the file."
    - question: "Is it safe to double-click unknown .bat or .command files?"
      answer: "No. Treat them like any other executable. Only run scripts you wrote yourself or fully trust, because a batch file or shell script can run any command your user account is allowed to run."
---

Every developer eventually needs to automate a few repetitive tasks: clear temp folders, launch a set of tools, rename a pile of files, or kick off a build sequence. On Windows that usually means writing a batch file. On Mac it means writing a shell script. Both are plain text files that hold a list of commands the system runs in order.

This guide shows you exactly how to create, save, and execute batch files on Windows and their shell-script equivalents on Mac. We keep it practical, with the steps that work in 2026 on current Windows 10 and 11 and on recent macOS releases. We also call out the small differences that trip people up, such as the shebang line on macOS and the `ERRORLEVEL` quirks that make `.cmd` a better default than `.bat`.

<!--more-->

If you would rather watch the idea first, this short walkthrough covers the same ground on camera:

<iframe width="100%" height="400" src="https://www.youtube.com/embed/DtlrxaP3PhQ?si=ts2iROxVZ8UZIHSX" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## What Is a Batch File (and Its Mac Equivalent)?

A Windows batch file is a text file with a `.bat` or `.cmd` extension. Windows hands it to `cmd.exe`, which executes each line as if you typed it into Command Prompt. There is no separate compile step and no runtime to install: the interpreter already ships with the operating system.

On Mac the closest equivalent is a shell script, usually ending in `.sh` or `.command`. It starts with a shebang line that tells the system which interpreter to use, such as bash or zsh. You make the file executable with `chmod +x` and run it from Terminal.

Both give you the same core power: store a sequence of commands once and run it any time with a double-click or a single terminal line. The rest of this guide builds a working example on each platform, then compares them directly.

## How to Write and Run Batch Files on Windows

### Create Your First .bat File

1. Open Notepad (search for it in the Start menu).
2. Type these three lines:

```bat
@echo off
echo Hello from my first batch file.
pause
```

3. Go to **File → Save As**.
4. In the "Save as type" dropdown choose **All files (*.*)**.
5. Name the file `hello.bat` (include the extension).
6. Save it somewhere easy to find, such as the Desktop or a `Scripts` folder.

The `@echo off` line hides the commands themselves so you only see the output. The `pause` command keeps the window open so you can actually read the result before it disappears.

### Run the Batch File

You have three reliable ways to launch it:

| Method               | How to do it                                       | Best for               |
|----------------------|----------------------------------------------------|------------------------|
| Double-click         | Click the .bat file in File Explorer               | Quick tests            |
| Command Prompt       | Type the full path, or `cd` to the folder and run  | Seeing errors clearly  |
| Run as Administrator | Right-click → Run as administrator                 | Tasks that need elevation |

From Command Prompt, call the file by its full path:

```cmd
"C:\Users\YourName\Desktop\hello.bat"
```

Or change directory first and run it by name:

```cmd
cd Desktop
hello.bat
```

### Useful Windows Batch Commands Developers Actually Use

Here is a slightly more realistic script that copies logs into a backup folder:

```bat
@echo off
setlocal
set "PROJECT=myapp"
echo Current folder: %CD%
dir /b *.txt
mkdir backup 2>nul
copy *.log backup\
echo Done.
pause
```

A few points that matter in day-to-day use:

- Use `set "VAR=value"` with quotes to avoid accidental trailing spaces in the value.
- `%1`, `%2`, and so on hold the command-line arguments passed to the script.
- `if errorlevel 1` checks for a failure after a command runs.
- Prefer `.cmd` over `.bat` when you care about consistent `ERRORLEVEL` behavior after built-in commands such as `set` or `path`.

Microsoft's [Windows Commands reference](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands) documents every built-in command, and [SS64's Windows CMD reference](https://ss64.com/nt/) is a faster lookup when you just need the syntax.

### Run from PowerShell or Windows Terminal

You can still launch a batch file from PowerShell without leaving your session:

```powershell
cmd /c "C:\Scripts\hello.bat"
```

Or just type the path if the current directory is already correct. This is handy when a tool ships a `.bat` launcher but you live in PowerShell. If you spend your day in a terminal, our setup guide for the [OpenCode terminal UI](/p/how-to-setup-opencode-tui/) is worth a look once the basics here click.

## How to Write and Run Shell Scripts on Mac

### Create Your First Script

1. Open TextEdit, or any plain-text editor. Make sure it is set to plain text mode (**Format → Make Plain Text**).
2. Type:

```bash
#!/bin/zsh
echo "Hello from my first Mac script"
```

3. Save the file as `hello.sh`, or `hello.command` if you want double-click support.

The first line is the shebang. You can read Apple's [introduction to shell scripts in Terminal](https://support.apple.com/guide/terminal/intro-to-shell-scripts-apd53500956-7c5b-496b-a362-2845f2aab4bc/mac) for the official explanation, but the short version is that it tells the system which interpreter to use. On modern macOS the default shell is zsh, so `#!/bin/zsh` is the safest choice. You can also use `#!/bin/bash` or `#!/bin/sh`.

### Make It Executable and Run It

Open Terminal and navigate to the folder:

```bash
cd ~/Desktop
chmod +x hello.sh
./hello.sh
```

`chmod +x` adds the execute permission. The `./` tells the shell to look in the current directory rather than searching `PATH`.

Alternative ways to run the same file:

- `sh hello.sh` or `zsh hello.sh` works even without the execute bit set.
- Rename the file to `hello.command` and double-click it in Finder, and Terminal opens and runs it.
- Drag the file onto an open Terminal window after typing `sh` or `./`.

### Useful Mac Shell Script Patterns

A small backup helper looks like this:

```bash
#!/bin/zsh
# Simple backup helper
PROJECT="myapp"
echo "Working in $(pwd)"
mkdir -p backup
cp *.log backup/ 2>/dev/null
echo "Done."
```

Tips that save time:

- Always start with a shebang.
- Use `#` for comments.
- Quote your variables: `"$PROJECT"`.
- Check exit status with `$?`, or wrap it: `if [ $? -eq 0 ]; then ...`.
- Add the script's folder to your `PATH` so you can call it from anywhere:

```bash
export PATH="$PATH:$HOME/scripts"
```

Put that line in `~/.zshrc` so it persists across sessions. For deeper topics, the [Apple Developer Shell Scripting Primer](https://developer.apple.com/library/archive/documentation/OpenSource/Conceptual/ShellScripting/Introduction/Introduction.html) and [SS64's macOS Bash reference](https://ss64.com/osx/) are both solid references.

## Side-by-Side Comparison

The two platforms look different on the surface, but the concepts line up almost one to one:

| Feature           | Windows (.bat / .cmd)          | Mac (.sh / .command)              |
|-------------------|--------------------------------|-----------------------------------|
| Editor            | Notepad or any text editor     | TextEdit, VS Code, vim            |
| Interpreter       | cmd.exe                        | zsh / bash / sh                   |
| Make executable   | Not required                   | `chmod +x`                        |
| Double-click run  | Yes                            | Yes (with .command extension)     |
| Arguments         | `%1 %2 ...`                    | `$1 $2 ...`                       |
| Comments          | `rem` or `::`                  | `#`                               |
| Variables         | `set "VAR=value"` then `%VAR%` | `VAR=value` then `$VAR`           |
| Admin / root      | Run as Administrator           | `sudo`                            |

If you ever find yourself maintaining the same logic on both sides, that is usually the signal to move the shared part into a cross-platform tool rather than duplicating it.

## Practical Tips for Developers

These come from scripts we have broken and fixed more than once.

- Keep scripts in a dedicated folder (`C:\Scripts` or `~/scripts`) and add it to `PATH`.
- Never hard-code passwords. Batch and shell files are plain text and easy to leak.
- Test every new script in a throwaway folder before you point it at real files.
- On Windows, enable "File name extensions" in File Explorer so you can see whether Notepad secretly saved your file as `hello.bat.txt`.
- On Mac, confirm the file uses Unix (LF) line endings. Windows-style CRLF can break the shebang.
- For more complex logic, graduate to PowerShell on Windows or Python on either platform. Batch and basic shell scripts stay excellent for short, reliable automation.
- Use Task Scheduler on Windows, or `launchd` and crontab on Mac, when the script needs to run on a schedule.

If your automation grows past a handful of one-off scripts, a visual workflow layer such as [n8n running locally on your PC](/p/how-to-install-n8n-locally-on-pc/) can replace a folder of brittle batch files with something you can actually inspect and debug.

A common pattern is to keep the heavy lifting in a real program and use the batch file only as a launcher. Wrapping a Node script, like the [transactional SMTP sender we set up with Node.js](/p/programmatic-transactional-smtp-nodejs-setup/), in a one-line batch file is a clean way to give non-developers a single icon to click without exposing the underlying command.

## Common Problems and Fixes

**Windows window closes too fast**
Add `pause` at the end, or run the file from an already-open Command Prompt so the window stays put.

**"Access denied" on Mac**
You forgot `chmod +x`, or the script needs `sudo` for the action it performs.

**Command not found**
The executable is not in `PATH`, or you typed the wrong relative path. Use the full path or prefix with `./`.

**Script works in Terminal but fails on double-click**
Environment variables or the current working directory differ between the two launch methods. Print `pwd` or `%CD%` at the top of the script to debug.

**The shebang is ignored on Mac**
Check for CRLF line endings and a leading space or BOM before `#!`. Both break the interpreter lookup.

## Key Takeaways

- Windows batch files are `.bat` or `.cmd` files run by `cmd.exe`. Create them in Notepad, save with the **All files** type, and double-click or call them from Command Prompt.
- Mac shell scripts need a shebang and `chmod +x`, and are run with `./script.sh` or by renaming the file to `.command`.
- Both are plain text. Start simple, and add `pause` or keep the terminal open so you can read output.
- Prefer quoted variables and explicit paths, and never embed secrets in a script.
- When the logic grows, move to PowerShell, Python, or a workflow tool such as n8n rather than stacking more lines into a batch file.

## Frequently Asked Questions

### What is the difference between .bat and .cmd on Windows?

Both run under `cmd.exe`. The main practical difference is how some built-in commands update `ERRORLEVEL`. `.cmd` files set `ERRORLEVEL` to 0 on success for commands such as `set` and `path`. Most developers can treat them as interchangeable.

### Do I need administrator rights to run a batch file?

Only if the commands inside the file require elevated privileges, such as writing to protected folders or changing system settings. Right-click the file and choose Run as administrator when you need it.

### Why does my Mac script say "Permission denied"?

The execute bit is missing. Run `chmod +x yourscript.sh` in Terminal. If the script itself needs root, prefix the run command with `sudo`.

### Can I run a Windows batch file on Mac or vice versa?

No. The languages and interpreters are different. You would need to rewrite the commands for the target platform or use a cross-platform language such as Python.

### How do I pass arguments to a batch or shell script?

On Windows, call `myscript.bat arg1 arg2` and read `%1` and `%2` inside the file. On Mac, call `./myscript.sh arg1 arg2` and read `$1` and `$2` inside the file.

### Is it safe to double-click unknown .bat or .command files?

No. Treat them like any other executable. Only run scripts you wrote yourself or fully trust, because a batch file or shell script can run any command your user account is allowed to run.

## Conclusion

Batch files and shell scripts are the smallest useful automation you can build, and they are worth learning because they turn a repeated ritual into a single command. Learn the Windows side with `.cmd`, learn the Mac side with a shebang and `chmod +x`, and you can automate the boring parts on either machine by the end of an afternoon.

From there the same habits carry into bigger systems. Teams like F9XR keep small scripts for local chores and reach for a proper workflow tool or an AI coding agent once the logic grows, which is the same division of labor we describe in our [guide to AI coding agents](/p/ai-coding-agents-explained/). If you want to share your own automation setup, the [Contributor Guide](/contribute/) explains how to submit an article to Dev9b, and everything we publish is reviewed against the standards in our [Editorial Policy](/editorial-policy/).

---

*This guide was researched and drafted with the assistance of an AI coding assistant, then reviewed by the F9XR Review Board before publishing. Have feedback or want to contribute your own article? See our [Contributor Guide](/contribute/) and [Editorial Policy](/editorial-policy/).*
