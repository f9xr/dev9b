---
title: "Diátaxis Framework: Fix Your Docs With 4 Types"
description: "Learn the Diátaxis documentation framework: tutorials, how-to guides, reference, and explanation, plus how to apply it to a real repository."
slug: diataxis-documentation-framework-guide
date: 2026-10-05
image: cover.jpg
author: F9XR Team
keywords: Diátaxis documentation framework, technical documentation structure, docs as code, tutorials vs how-to guides, developer documentation
categories:
    - Tutorials
tags:
    - developer-setup
    - hugo
    - seo
    - skills
draft: false
math: false
faq:
    - question: "What is the Diátaxis framework?"
      answer: "The Diátaxis framework organizes technical documentation into four types: tutorials, how-to guides, reference, and explanation. Each type serves one distinct reader need, which keeps pages focused and easier to use. It was created by Daniele Procida."
    - question: "What are the four types of documentation in Diátaxis?"
      answer: "The four types are tutorials (learning-oriented lessons), how-to guides (goal-oriented task steps), reference (information-oriented technical facts), and explanation (understanding-oriented background and reasoning)."
    - question: "What is the difference between a tutorial and a how-to guide?"
      answer: "A tutorial teaches a beginner through a guided experience so they can learn a skill. A how-to guide helps someone who already knows the basics complete a specific task at work. Tutorials focus on learning, how-to guides focus on getting work done."
    - question: "What is the difference between reference and explanation?"
      answer: "Reference provides neutral and accurate facts such as parameters, commands, and return values. Explanation discusses context, design choices, and trade-offs so the reader understands why the system works the way it does."
    - question: "Do I need to rewrite all my documentation to use Diátaxis?"
      answer: "No. The framework is designed for incremental adoption. Identify one mixed page, split it into focused pages, then repeat. Most teams start by separating a single page that is doing two jobs at once."
    - question: "Is Diátaxis useful for AI agents and RAG systems?"
      answer: "Yes. Single-purpose pages produce cleaner chunks for retrieval, and a doc type field in front matter gives retrieval pipelines an easy filter. That tends to improve the accuracy of AI assistant answers."
---

You have probably been here before. A new developer joins the team, opens the docs, and gets lost within five minutes. The "Getting Started" page explains the architecture, the API page tells them to run a command nobody mentioned earlier, and the one thing they actually need is buried in the middle of a long README.

Nothing is technically wrong with that content. The problem is how it is organized. This is exactly the problem the **Diátaxis documentation framework** was built to solve, and fixing it is usually a few hours of work rather than a rewrite.

<!--more-->

Diátaxis is a lightweight, practical way to structure technical documentation around what readers are actually trying to do. It is used by projects and companies you already know, and it has become a go-to mental model for developers, technical writers, and teams building documentation for AI agents and retrieval systems.

In this guide you will learn what Diátaxis is, how its four types work, how to apply it to a real repository, and which mistakes to avoid. By the end you will have a plan you can use on your own docs this week.

## What Is the Diátaxis Documentation Framework?

**Diátaxis** (pronounced roughly "dee-uh-TAK-sis") is a framework for organizing technical documentation, created by Daniele Procida. The name comes from Ancient Greek and means "across arrangement."

The core idea is simple. Readers arrive at documentation with one of four distinct needs, and each need deserves its own type of content. Instead of mixing everything into one long page, you separate the content into four forms:

1. Tutorials
2. How-to guides
3. Reference
4. Explanation

Canonical, the company behind Ubuntu, publicly adopted Diátaxis as the foundation of its documentation work and described it as a map and compass for quality. Other well-known projects such as Django and Cloudflare are commonly cited as users of the approach, which shows it scales from open source libraries to large product suites.

> **Quick definition:** The Diátaxis framework is a documentation structure that divides technical content into four types (tutorials, how-to guides, reference, and explanation) so each page serves one clear reader need.

## The Two Axes That Make Diátaxis Work

Most explanations jump straight to the four boxes. It is more useful to understand the two questions behind them.

**Axis 1: Action or knowledge?**
Tutorials and how-to guides are about what the reader *does*. Reference and explanation are about what the reader *knows*.

**Axis 2: Study or work?**
Tutorials and explanation help someone *learn* a skill. How-to guides and reference help someone *apply* a skill while working.

Put those two axes together and you get the familiar four-quadrant grid:

| | **Action (doing)** | **Knowledge (understanding)** |
|---|---|---|
| **Study (learning)** | **Tutorials** | **Explanation** |
| **Work (applying)** | **How-to guides** | **Reference** |

This grid is the entire framework. Everything else is detail on how to write each quadrant well.

## The Four Types of Documentation Explained

### 1. Tutorials: Learning by Doing

A tutorial is a guided lesson. The reader is new, they do not yet know what they do not know, and your job is to give them a successful first experience.

**Good tutorials:**
- Take the reader through a sequence of concrete steps
- Produce a visible result early and often
- Work every single time, so test them like code
- Avoid explaining theory in the middle of the steps

**Example title:** "Build your first REST API with FastAPI in 15 minutes"

Think of a tutorial as a cooking class for a beginner. You do not stop to explain the chemistry of the Maillard reaction while they are chopping onions.

### 2. How-to Guides: Solving a Specific Problem

A how-to guide is a recipe for someone who already knows the basics and has a real task in front of them.

**Good how-to guides:**
- Start from a clear goal, such as "How to rotate API keys"
- Assume some competence from the reader
- Focus on the steps that matter, nothing more
- Handle realistic variations and edge cases

**Example title:** "How to configure a custom domain for GitHub Pages with Cloudflare"

The key difference from a tutorial is intent. A tutorial teaches, a how-to guide helps get work done. Mixing the two is the most common documentation mistake there is.

### 3. Reference: The Facts, Accurately

Reference documentation describes the machinery. It is the page a developer scans while in the middle of coding.

**Good reference:**
- Mirrors the structure of the code or product
- Is complete, accurate, and consistent
- Uses neutral, factual language
- Includes parameters, return types, defaults, and error codes

**Example:** API endpoint listings, CLI flag tables, configuration schemas, and function signatures.

Reference should not give opinions or tell stories. It should be boring in the best possible way.

### 4. Explanation: The Why Behind the What

Explanation provides context, background, and reasoning. It answers questions like "why does this system work this way?" and "what are the trade-offs?"

**Good explanation:**
- Discusses design decisions and alternatives
- Connects concepts to each other
- Can include history and opinion, as long as it is clearly labeled
- Is read away from the keyboard, often with a coffee

**Example title:** "Why we chose event sourcing for our order service"

## Diátaxis Types Compared at a Glance

| Type | Reader's question | Orientation | Tone | Typical format |
|---|---|---|---|---|
| Tutorial | "Can you teach me?" | Learning | Encouraging, guiding | Step-by-step lesson |
| How-to guide | "How do I do X?" | Goal | Direct, practical | Numbered task steps |
| Reference | "What exactly is X?" | Information | Neutral, precise | Tables, lists, API specs |
| Explanation | "Why is it like this?" | Understanding | Discursive, thoughtful | Articles, essays, ADRs |

## Why Developers Should Care

Diátaxis is often introduced as a tool for technical writers, but developers benefit just as much. Here is why it matters in practice:

- **Faster onboarding.** New contributors find the right page without asking in chat.
- **Fewer support questions.** Clear how-to guides cut repetitive issues.
- **Easier maintenance.** When a function changes, you know exactly which reference page to update.
- **Better search visibility.** Pages with a single clear intent match search queries more precisely, which helps both Google and AI answer engines. Our [Hugo SEO guide](/p/hugo-seo-guide/) covers the on-page side of this.
- **Cleaner pull requests.** Contributors know where new docs belong.

The framework also pairs naturally with **docs as code**, where documentation lives in the same repository as the source and goes through the same review process.

## How to Apply Diátaxis to a Real Project

You do not need to rewrite everything. The framework's creator has been clear that the best approach is incremental: find one problem, fix it, then repeat.

### Step 1: Audit What You Already Have

List every documentation page and tag it with one of the four types. You will quickly spot pages that are doing two or three jobs at once.

### Step 2: Ask the Compass Questions

For each page, ask:

1. Does this page describe actions or knowledge?
2. Does it serve someone who is studying or someone who is working?

The answers point to the correct type.

### Step 3: Split Mixed Pages

If a tutorial contains a long architectural digression, move that part into an explanation page and link to it. If a reference page contains advice, move the advice to a how-to or explanation page.

### Step 4: Create a Simple Folder Structure

Here is a minimal layout that works well for Markdown-based docs sites, including Hugo, MkDocs, Docusaurus, and Astro Starlight:

```text
docs/
|-- tutorials/
|   `-- getting-started.md
|-- how-to/
|   |-- configure-auth.md
|   `-- deploy-to-production.md
|-- reference/
|   |-- api.md
|   |-- cli.md
|   `-- configuration.md
`-- explanation/
    |-- architecture.md
    `-- design-decisions.md
```

A matching navigation config for MkDocs might look like this:

```yaml
nav:
  - Tutorials:
      - Getting started: tutorials/getting-started.md
  - How-to guides:
      - Configure authentication: how-to/configure-auth.md
      - Deploy to production: how-to/deploy-to-production.md
  - Reference:
      - API: reference/api.md
      - CLI: reference/cli.md
      - Configuration: reference/configuration.md
  - Explanation:
      - Architecture: explanation/architecture.md
      - Design decisions: explanation/design-decisions.md
```

### Step 5: Add a Doc Type to Front Matter

Tagging each page with its type makes audits, linting, and AI retrieval easier:

```markdown
---
title: "How to rotate API keys"
doc_type: how-to
audience: backend-developers
last_reviewed: 2026-10-05
---
```

### Step 6: Add a Quick Lint Check (Optional)

If you want your CI pipeline to enforce the structure, a tiny script is enough:

```bash
#!/usr/bin/env bash
# Fail the build if a doc is missing a valid doc_type
valid="tutorial|how-to|reference|explanation"
status=0

for file in $(find docs -name "*.md"); do
  type=$(grep -m1 '^doc_type:' "$file" | awk '{print $2}')
  if ! echo "$type" | grep -Eq "^($valid)$"; then
    echo "Missing or invalid doc_type: $file"
    status=1
  fi
done

exit $status
```

### Step 7: Link Between Types

Good Diátaxis docs are well connected. A tutorial links to reference for details and to explanation for background. A how-to guide links to reference for parameters. This keeps every page focused without leaving readers stranded.

## Common Mistakes (and How to Avoid Them)

| Mistake | Why it hurts | Fix |
|---|---|---|
| Explaining theory inside a tutorial | Breaks the learning flow and overwhelms beginners | Link out to an explanation page |
| Writing a how-to that teaches basics | Wastes the time of experienced users | Assume competence, state prerequisites |
| Adding opinions to reference | Users scanning for facts get confused | Move advice to explanation |
| Creating empty section folders | Scaffolding without content looks unfinished | Write content first, let structure grow |
| Treating the four types as rigid rules | Real docs need judgment | Use Diátaxis as a guide, not a law |
| Rewriting everything at once | Burnout and stalled projects | Improve one page at a time |

## Diátaxis and AI: Why It Matters for AEO and RAG

Here is the part that makes Diátaxis more relevant in 2026 than ever. Documentation is no longer read only by humans. It is also consumed by AI coding assistants, answer engines, and retrieval-augmented generation systems. Our primer on [AI coding agents explained](/p/ai-coding-agents-explained/) covers why these consumers behave the way they do.

When each page has a single, clear purpose, both people and machines benefit:

- **Better chunking.** A focused how-to page produces cleaner embeddings than a page mixing five topics.
- **More accurate answers.** An AI agent asked "how do I configure X?" can pull from a how-to guide instead of guessing from a mixed page.
- **Clear intent signals.** A `doc_type` field in front matter gives retrieval pipelines an easy filter.
- **Stronger featured snippet potential.** Question-style headings with direct answers match how Google and AI search engines extract content.

If you are building agent instructions, skill files, or design system docs for AI tools, the same separation helps. Keep instructions (how-to), specifications (reference), and rationale (explanation) in distinct files. The same idea drives how we structure [OpenCode agent skills](/p/opencode-skills-guide/) and [design system docs for AI agents](/p/what-is-getdesign-md-ai-agents-design-system/).

## Actionable Tips for Better Docs Today

1. **Start with your most visited page.** Check analytics, then classify it. Fixing one high-traffic page beats a perfect plan that never ships.
2. **Test tutorials like code.** Run through them on a clean machine every release.
3. **Title pages by intent.** Use "How to..." for guides, "Tutorial:" for lessons, "Reference:" for specs, and "Understanding..." or "Why..." for explanation.
4. **Keep one page, one job.** If you write the word "also" too often, you may be mixing types.
5. **Use consistent templates.** A short template per type saves time and keeps contributors aligned.
6. **Put reference close to code.** Generate it from docstrings or OpenAPI specs where possible.
7. **Review docs in pull requests.** Treat outdated documentation as a bug.
8. **Link generously, but purposefully.** Cross-links replace the temptation to cram everything into one page.

## Is Diátaxis Right for Every Project?

Honestly, not always in its full form. A tiny script with a single README does not need four folders. Even then, the thinking still helps: keep a short quickstart (tutorial), a usage section (how-to), an options table (reference), and a "Why this exists" paragraph (explanation).

For larger products, SDKs, platforms, and open source ecosystems, Diátaxis pays off quickly because the number of pages and contributors grows over time. If you are publishing docs as a site rather than a repo, our walkthrough on [publishing a Hugo site on GitHub Pages](/p/hugo-github-pages-setup/) covers the hosting side.

## Frequently Asked Questions

### What is the Diátaxis framework?

The Diátaxis framework is a method for organizing technical documentation into four types: tutorials, how-to guides, reference, and explanation. Each type serves a different reader need, which keeps pages focused and easier to use. It was created by Daniele Procida.

### What are the four types of documentation in Diátaxis?

The four types are tutorials (learning-oriented lessons), how-to guides (goal-oriented task steps), reference (information-oriented technical facts), and explanation (understanding-oriented background and reasoning).

### What is the difference between a tutorial and a how-to guide?

A tutorial teaches a beginner through a guided experience so they can learn a skill. A how-to guide helps someone who already has basic knowledge complete a specific real-world task. Tutorials focus on learning, while how-to guides focus on getting work done.

### What is the difference between reference and explanation?

Reference provides neutral, accurate facts about the system, such as parameters, commands, and return values. Explanation discusses context, design choices, and trade-offs to help the reader understand why it works the way it does.

### Where does the name Diátaxis come from?

Diátaxis comes from Ancient Greek and roughly means "across arrangement." It reflects the idea of arranging documentation across the different needs of its readers.

### Do I need to rewrite all my documentation to use Diátaxis?

No. You can adopt it gradually. Identify one problem in your existing docs, improve it, and repeat. Many teams begin by separating one mixed page into two or more focused pages.

### Is Diátaxis good for AI and RAG systems?

Yes. Single-purpose pages create cleaner chunks for retrieval, and a doc type label in front matter helps filter content. This tends to produce more accurate answers from AI assistants and search tools.

### Which tools work with Diátaxis?

Any docs tool that supports Markdown and a folder-based navigation structure works, incluDiátaxis is a way of organizing content, so it does not depend on a specific tool.

## Key Takeaways

- Diátaxis is a documentation framework by Daniele Procida that splits content into **tutorials, how-to guides, reference, and explanation**.
- Two questions drive it: is the content about **action or knowledge**, and does it serve **study or work**?
- Each page should do **one job**. Mixing types is the root cause of most confusing docs.
- You can adopt it **incrementally**. Fix one page at a time instead of rewriting everything.
- A simple folder structure, a `doc_type` front matter field, and a small CI check make the framework stick.
- Clear, single-purpose pages also improve **SEO, featured snippets, AI answer engine citations, and RAG accuracy**.
- Treat Diátaxis as a **guide for thinking**, not a rigid rulebook.

## Conclusion

Great documentation rarely fails because of bad writing. It fails because the right information sits in the wrong place. Diátaxis gives you a simple way to put it in the right place, using nothing more than two questions and four page types.

Pick one confusing page in your project today. Decide which of the four types it should be, split it if needed, and publish the improvement. That single change is already Diátaxis in action.

If you want to write about the results, the [contributor guide](/contribute/) explains how the F9XR Team reviews submissions, and the [editorial policy](/editorial-policy/) covers how we verify claims before publishing.


