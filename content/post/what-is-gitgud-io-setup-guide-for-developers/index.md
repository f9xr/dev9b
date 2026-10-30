---
title: "GitGud.io Explained: Free Git Hosting Setup Guide"
description: "Learn what GitGud.io is, how its free GitLab-powered hosting works, and how to set up your next project step by step, from SSH keys to CI and Pages."
slug: what-is-gitgud-io-setup-guide-for-developers
date: 2026-10-30
image: cover.jpg
author: F9XR Team
keywords: GitGud.io, what is GitGud, GitGud setup, free Git hosting, GitLab hosting, GitGud.io vs GitLab, GitGud Pages, Git repository hosting, free private repositories, GitLab CI free
categories:
    - Tutorials
tags:
    - developer-tools
    - developer-setup
    - static-site
    - custom-domain
draft: false
math: false
faq:
    - question: "What is GitGud.io?"
      answer: "GitGud.io is a free Git hosting service built on GitLab and run by Sapphire since 2014. It offers public and private repositories, CI/CD, Pages hosting, a container registry, and project tools without a subscription fee."
    - question: "Is GitGud.io free?"
      answer: "Yes. GitGud.io advertises unlimited private repositories for users and groups with no stated repository size limit for code. Shared CI runner access is reported as available on request. Check about.gitgud.io for current terms."
    - question: "Is GitGud.io the same as GitLab?"
      answer: "No. GitGud.io runs the GitLab software, but Sapphire operates it as an independent installation. The workflow feels familiar, while accounts, hosting, and support stay separate from GitLab.com."
    - question: "How do I create a project on GitGud.io?"
      answer: "Sign up through Sapphire Accounts, add an SSH key to your profile, click New project, choose Create blank project, set a name and visibility, then click Create project. Clone the repo or add it as a remote and push your first commit."
    - question: "Does GitGud.io support CI/CD?"
      answer: "Yes. It uses GitLab CI, so you define pipelines in a .gitlab-ci.yml file. Shared runner access has been described as free on request, and you can connect your own runner if you prefer."
    - question: "Can I host a static website on GitGud.io?"
      answer: "Yes. GitGud.io offers Pages hosting on GitGud.site with custom domain support. Add a pages job that publishes your built files from a public folder, then set the domain in the project settings."
---

Most developers pick a Git host once and never think about it again. That works until you hit a storage cap, a CI minutes limit, or a pricing page that suddenly matters.

GitGud.io is one of the quieter alternatives. It's a free Git host that runs on GitLab, launched in 2014, and advertises unlimited private repos with no stated size limit for code. If you want a GitLab-style workflow without a bill, it's worth 10 minutes.

This guide covers what GitGud is, who it suits, and how to set up a real project. You'll go from your first SSH key to a working pipeline and a static site on a custom domain.

<!--more-->

> [!NOTE] Quick answer
> **GitGud.io is a free Git hosting service built on GitLab software and run by an independent company called Sapphire.** You can host public and private repos, run CI/CD pipelines, publish static sites, and manage issues without paying. The operator is Sapphire, and GitLab Inc. doesn't run the hosting. Your repos still use standard Git.

## What is GitGud.io?

GitGud.io is a hosted instance of GitLab. Think of it as a community-run version of GitLab.com with its own rules, servers, and accounts.

The name causes some confusion. "GitGud" also names an npm CLI that wraps everyday Git commands and an experimental Elixir platform on GitHub. This article is about GitGud.io, the hosted service.

### Who runs it

Sapphire, a user-supported open source company, has run GitGud.io since October 2014. The operators say they built it to focus on features and technology instead of user politics on other hosts. You sign up through Sapphire Accounts.

Public forum posts from the operators say they no longer depend on donations and pay for hosting out of their own pockets. That's good news for your bill today. It's also the first thing to weigh when you plan backups.

### Is GitGud.io the same as GitLab?

No. It runs the GitLab software, but it's a separate installation. A commenter on the Cloudron forum put it plainly: GitGud is somebody else's install of GitLab.

The interface, merge requests, issue boards, and `.gitlab-ci.yml` pipelines will feel familiar if you've used GitLab. Your account, projects, and support channel stay with GitGud's operators.

## Features at a glance

The table below sums up what the service and third-party directories report. Terms can change, so confirm the details on the [official GitGud.io site](https://about.gitgud.io) before you move anything important.

| Feature | What you get | Practical note |
|---|---|---|
| Private repositories | Unlimited for users and groups | Good for side projects and client work |
| Repository size | No stated limit for code and development content | Still keep large binaries out of Git |
| CI/CD | GitLab CI with free shared runner access | Reported as available on request |
| Static hosting | Free Pages hosting on GitGud.site with custom domains | Works well for docs and portfolios |
| Container registry | Free, served from a dedicated domain | Handy for Docker projects |
| Project tools | Issues, wikis, Kanban boards, snippets, service desk | The same toolset GitLab users know |
| Support | Direct contact with the administrators | Smaller scale than a big vendor |
| Privacy stance | Operators state no tracking, no user analytics, and no external IP logging | A claim to read, not a guarantee to assume |

## GitGud.io vs GitLab.com vs GitHub vs Codeberg

Choosing a host is mostly about trade-offs. Here's a fair side-by-side.

| Platform | Software | Cost model | Best for |
|---|---|---|---|
| GitGud.io | GitLab | Free, community funded | Free private repos, GitLab workflow, static sites |
| GitLab.com | GitLab | Free tier with caps, paid plans | Teams that want a full DevSecOps platform and a clear upgrade path |
| GitHub | Proprietary | Free plan, paid tiers | Open source reach, a huge ecosystem, Actions |
| Codeberg | Forgejo | Free, non-profit | Open source projects that prefer a non-profit host |
| SourceHut | Custom | Low cost | Email-driven workflows and minimalists |

One review site framed the GitGud versus GitLab.com question well. GitGud fits if you want an unlimited free Git host. GitLab.com wins if you need broader features, published CI minutes, and an enterprise upgrade path.

[Codeberg](https://codeberg.org) sits in a similar spot to GitGud on cost, with a non-profit structure and a European hosting story. We walked through its static hosting in our [Codeberg Pages guide](/p/how-to-host-static-websites-codeberg-pages/).

## Who should use GitGud.io?

**A good fit if you are:**

- A solo developer or hobbyist who wants unlimited private repos
- A student or maintainer who wants a GitLab-style workflow at zero cost
- Someone who wants free static hosting with a custom domain
- A developer who prefers a small, independent host

**Think twice if you need:**

- Formal enterprise controls, documented SSO, or a service level agreement
- A paid upgrade path with guaranteed support
- Compliance paperwork for regulated work
- The largest possible audience for an open source project

## How to set up your next project on GitGud.io

The flow below follows the standard GitLab workflow. Menu names can shift between GitLab versions, so treat the labels as a guide.

```mermaid
flowchart LR
    A[Create account] --> B[Add SSH key]
    B --> C[Create project]
    C --> D[Push code]
    D --> E[Add .gitlab-ci.yml]
    E --> F[Pages or registry]
```

### Step 1: Create your account

Go to the GitGud.io sign-up page and register through Sapphire Accounts. Use an email address you can access, then turn on two-factor authentication as soon as your account is active. Do that first, not later.

### Step 2: Install and configure Git locally

If Git isn't installed, get it from [git-scm.com](https://git-scm.com/book) or your package manager. Then set your identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

Use the same email you added to your GitGud profile so your commits link to your account.

### Step 3: Generate and add an SSH key

SSH keys let you push without typing a password every time.

```bash
ssh-keygen -t ed25519 -C "you@example.com"
cat ~/.ssh/id_ed25519.pub
```

Copy the output. Open your profile settings on GitGud.io, find the SSH Keys section, paste the key, and save. Then test the connection:

```bash
ssh -T git@gitgud.io
```

A welcome message with your username means it worked. The [GitLab SSH documentation](https://docs.gitlab.com/ee/user/ssh.html) covers extra options if you already manage several keys.

### Step 4: Create a new project

1. Click **New project** from the dashboard.
2. Choose **Create blank project**.
3. Enter a project name and let the slug generate.
4. Pick visibility: **Private** if you aren't ready to share, **Public** otherwise.
5. Tick the README option if you plan to clone first.
6. Click **Create project**.

### Step 5: Connect your local code

If you started on GitGud.io, clone the project. Copy the exact URL from the **Clone** button on the project page.

```bash
git clone git@gitgud.io:YOUR-USERNAME/YOUR-PROJECT.git
cd YOUR-PROJECT
```

If you already have code on your machine, connect it instead:

```bash
cd existing-project
git init -b main
git add .
git commit -m "Initial commit"
git remote add origin git@gitgud.io:YOUR-USERNAME/YOUR-PROJECT.git
git push -u origin main
```

### Step 6: Work in branches and open merge requests

Even on a solo project, branches keep your main line clean.

```bash
git checkout -b feature/login-form
# make changes
git add .
git commit -m "Add login form validation"
git push -u origin feature/login-form
```

GitGud.io usually prints a link in the terminal to open a merge request. Review your own diff there before you merge. It catches more mistakes than you'd expect.

### Step 7: Add a CI/CD pipeline

Create a `.gitlab-ci.yml` file in the root of your repo. Here's a small Node.js example:

```yaml
image: node:20

stages:
  - test

test:
  stage: test
  script:
    - npm ci
    - npm test
```

Commit and push. Shared runner access has been described as free but available by request. If your pipeline stays stuck in a pending state, contact the administrators and ask for runner access. You can also register your own runner.

### Step 8: Publish a static site with Pages

GitGud.io offers Pages hosting on GitGud.site with custom domain support. A minimal pipeline looks like this:

```yaml
pages:
  image: alpine:latest
  script:
    - mkdir -p public
    - cp -r site/* public/
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

After the job succeeds, open the Pages settings in your project to find the site address and add a custom domain. For static site generators such as Hugo or Astro, replace the script with your build command and publish the output folder as `public`.

The [GitLab Pages documentation](https://docs.gitlab.com/ee/user/project/pages/) explains the artifact rules in more detail. If you're wiring up DNS for the first time, our [GitHub Pages custom domain guide](/p/github-pages-custom-domain-cloudflare/) covers the Cloudflare side, and our [Hugo on GitHub Pages walkthrough](/p/hugo-github-pages-setup/) shows the same build shape for a generator. No domain yet? Start with our [free subdomains for developers](/p/free-subdomains-for-developers-list/) list.

### Step 9: Use the container registry (optional)

If your project ships as a Docker image, the project's Container Registry page shows the exact login and push commands for the registry domain. Copy them from there instead of guessing the address.

## A project layout that ages well

A clean repo saves you and your collaborators time. A solid starting layout:

```text
my-project/
  .gitignore
  .gitlab-ci.yml
  README.md
  LICENSE
  src/
  tests/
  docs/
```

Add a `.gitignore` before your first commit so you never push `node_modules`, `.env` files, build output, or editor settings by accident.

## Common problems and fixes

| Problem | Likely cause | Fix |
|---|---|---|
| `Permission denied (publickey)` | SSH key not added or the wrong key is used | Re-add the public key, then run `ssh -T git@gitgud.io` |
| Push rejected | The remote has commits you don't have | Run `git pull --rebase`, then push again |
| Pipeline stuck on pending | No runner assigned | Ask the administrators for shared runner access or register your own |
| Pages site shows 404 | Output isn't in `public` or the job didn't run | Check the artifact path and the branch rule |
| Commits not linked to your profile | Email mismatch | Match `user.email` to your profile email |

## Practical tips from our workflow

We haven't moved Dev9b onto GitGud.io. We did read the operators' own posts, the official feature list, and third-party directories before writing this. If we were moving a client repo tomorrow, we'd test four things first: an SSH push, a runner, Pages on a throwaway project, and a project export. The export matters because a small host can change terms or close.

A few habits apply to any host:

- **Mirror your repo.** Push a copy to Codeberg, GitLab.com, or GitHub. Two remotes take one command: `git remote set-url --add --push origin <second-url>`.
- **Use deploy tokens and project access tokens** in CI instead of your personal credentials. Our [GitHub security setup guide](/p/what-is-gh-secure-setup-guide/) covers the same token hygiene on the other side.
- **Never commit secrets.** Store keys in CI variables and mark them as masked.
- **Keep large files out of Git.** No stated size limit still has practical costs. Use Git LFS or a storage service for big assets.
- **Protect your main branch** so nobody, including you on a late night, pushes straight to it.
- **Write a useful README.** Search engines, AI assistants, and new contributors all read it first.
- **Export a backup now and then** using the project export option in settings.

## The honest limits

GitGud.io is a small, independently run service. That brings real advantages: direct access to the people running it and no usage anxiety. It also means you shouldn't expect the redundancy, compliance certifications, or round-the-clock support of a large vendor.

Treat it as a good home for personal and community projects. Keep a mirror for anything you can't afford to lose.

## Key Takeaways

- GitGud.io is a free Git host built on GitLab and run independently by Sapphire since October 2014.
- It advertises unlimited private repos, no stated size limit for code, free Pages hosting with custom domains, and a free container registry.
- Your account and support live with GitGud's own operators, separate from GitLab.com and GitHub.
- Setup follows the standard GitLab flow: create an account, add an SSH key, create a project, push code, then add `.gitlab-ci.yml`.
- CI runner access is reported as free on request, so ask if pipelines stay pending.
- Keep a mirror on a second host.

## Frequently Asked Questions

### What is GitGud.io?

GitGud.io is a free Git hosting service built on GitLab and run by Sapphire since 2014. It offers public and private repositories, CI/CD, Pages hosting, a container registry, and project tools without a subscription fee.

### Is GitGud.io free?

Yes. GitGud.io advertises unlimited private repositories for users and groups with no stated repository size limit for code. Shared CI runner access is reported as available on request. Check about.gitgud.io for current terms.

### Is GitGud.io the same as GitLab?

No. GitGud.io runs the GitLab software, but Sapphire operates it as an independent installation. The workflow feels familiar, while accounts, hosting, and support stay separate from GitLab.com.

### How do I create a project on GitGud.io?

Sign up through Sapphire Accounts, add an SSH key to your profile, click New project, choose Create blank project, set a name and visibility, then click Create project. Clone the repo or add it as a remote and push your first commit.

### Does GitGud.io support CI/CD?

Yes. It uses GitLab CI, so you define pipelines in a `.gitlab-ci.yml` file. Shared runner access has been described as free on request, and you can connect your own runner if you prefer.

### Can I host a static website on GitGud.io?

Yes. GitGud.io offers Pages hosting on GitGud.site with custom domain support. Add a `pages` job that publishes your built files from a `public` folder, then set the domain in the project settings.

## Conclusion

GitGud.io fills a useful gap. It gives you the GitLab workflow and unlimited private repos without a subscription, and it keeps a small-team feel that big platforms lost years ago. The setup is the same flow you already know, which means the move takes an afternoon rather than a migration project.

Start with a throwaway repo and prove the SSH push, CI, and Pages path before you move anything real. Then keep a mirror, protect your main branch, and export a backup now and then.

If you want to share your own hosting notes, read our [contributor guide](/contribute/) and check the [editorial policy](/editorial-policy/) before you submit. The F9XR Team reviews every guide against official docs before it ships.

*Disclosure: This article was drafted with AI assistance and reviewed and edited by the F9XR Team. Product details come from the operators' own description and third-party directory listings reviewed in October 2026, not from a hands-on test of the service. Confirm current terms at about.gitgud.io before relying on them for important work.*
