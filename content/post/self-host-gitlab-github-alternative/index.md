---
title: "Self-Host GitLab as Your GitHub Alternative"
description: "Learn how to self-host GitLab CE and build a private GitHub alternative with full CI/CD, registries, and complete data ownership."
slug: self-host-gitlab-github-alternative
date: 2026-10-31
image: cover.jpg
author: F9XR Team
keywords: self-host GitLab, GitLab CE, GitHub alternative, self-hosted Git, GitLab Runner, GitLab CI/CD, Omnibus install
categories:
    - Tutorials
tags:
    - gitlab
    - self-hosting
    - devops
    - developer-tools
draft: false
math: false
faq:
    - question: "How much RAM does self-hosted GitLab really need?"
      answer: "GitLab's official baseline for a single-node install is 16 GB. It can run on 8 GB for small teams with light usage, but performance and reliability improve significantly with more memory. Avoid running it on less than 8 GB in production."
    - question: "Is GitLab CE free forever?"
      answer: "Yes. The Community Edition is open source, with an MIT-licensed core, and free to self-host indefinitely. Paid features exist in the Enterprise Edition, but CE already includes the core Git hosting, CI/CD, registry, and issue tracking most teams need."
    - question: "Can I run GitLab on a home lab or low-cost VPS?"
      answer: "Yes, provided the machine meets the minimum specs. Many developers successfully run small instances on 8 to 16 GB VPS plans or home servers. Just monitor resources and keep backups off-site."
    - question: "How do I update GitLab safely?"
      answer: "Run sudo apt update && sudo apt install gitlab-ce followed by sudo gitlab-ctl reconfigure. Always read the official upgrade notes for major version jumps, as intermediate versions are sometimes required."
    - question: "GitLab vs Gitea: which should I pick?"
      answer: "Choose Gitea or Forgejo if you want something lightweight that feels like a simple GitHub clone. Choose GitLab when you need mature CI/CD, a container registry, package registry, and advanced permission models out of the box."
---

Your source code is the most valuable thing your team owns, and most of it sits on someone else's servers under someone else's pricing page. That works until a per-seat bill doubles, a CI minute cap bites, or a policy change forces a migration you did not plan for.

Self-hosting GitLab Community Edition puts the whole toolchain back under your control. You get repositories, merge requests, issues, a container registry, a package registry, and CI/CD on hardware you own. You also get the bill for that hardware, which is the part most guides skip.

This walkthrough covers a production-ready Omnibus install on Ubuntu, the settings worth changing on day one, and the operational habits that keep an instance alive after the novelty wears off.

<!--more-->

> [!NOTE] Quick answer
> GitLab CE is a full DevOps platform you can run on your own server. The Omnibus package installs GitLab, PostgreSQL, Redis, and Nginx in one shot, and a single-node instance needs roughly 8 GB of RAM to be useful and 16 GB to be comfortable. You trade a subscription fee for server cost and maintenance work.

## What GitLab CE Actually Gives You

GitLab is not a thin Git wrapper. It ships with the tools a small engineering team would otherwise assemble from five vendors:

- **Git hosting** with protected branches, merge request approvals, and fine-grained roles
- **GitLab CI/CD** driven by a `.gitlab-ci.yml` file in each repository
- **Container registry** for Docker images, scoped per project
- **Package registry** for npm, Maven, PyPI, NuGet, and Composer packages
- **Issue boards, epics in paid tiers, wikis, and snippets**
- **Security scanning** in CE, with deeper coverage in Enterprise Edition

The registry and pipeline pieces matter more than they sound. Once your images and packages live beside the code that produces them, access control stops being a separate problem.

## GitLab vs Gitea and Forgejo

Gitea and Forgejo are excellent when you want Git hosting with a clean interface and almost no operational weight. A small instance runs comfortably in 1 to 2 GB of RAM. GitLab asks for several times that, and gives you several tools in return.

| Feature | GitLab CE | Gitea / Forgejo | Bare Git + SSH |
|---|---|---|---|
| Merge requests | Yes | Yes | Manual |
| Built-in CI/CD | Full pipelines | Lightweight Actions | External only |
| Container registry | Yes | Limited | No |
| Package registry | Yes | Yes | No |
| Security scanning | Included | Limited | No |
| Resource needs | 8 GB+ RAM | 512 MB to 2 GB | Minimal |
| Best fit | Full DevOps teams | Small teams | One developer |

Pick GitLab when your team already thinks in pipelines, registries, and role-based permissions. Pick Gitea or Forgejo when you want a private GitHub clone that you can forget about. If you only need a place to push commits, bare Git over SSH is still the cheapest option, and it is not a joke.

If you would rather rent a GitLab instance than run one, the [GitGud.io setup guide](/p/what-is-gitgud-io-setup-guide-for-developers/) covers a free hosted GitLab that skips the server maintenance entirely.

## System Requirements That Actually Matter

GitLab's own documentation is blunt about this: a single-node install is happiest with 8 vCPU, 16 GB of RAM, and fast SSD storage. The minimum workable floor is around 4 vCPU and 8 GB, and you will feel it on the first big pipeline.

- **CPU**: 4 vCPU minimum, 8 recommended
- **RAM**: 8 GB minimum, 16 GB recommended
- **Disk**: 40 GB for the application, plus room for repositories, artifacts, and backups
- **OS**: Ubuntu 22.04 or 24.04 LTS
- **Domain**: a subdomain such as `git.yourdomain.com`, pointed at the server before you install

> [!WARNING] Swap is not a substitute for RAM
> GitLab degrades badly once it starts swapping. Puma workers, Sidekiq jobs, PostgreSQL, and Redis all compete for memory at the same time. If the box is swapping during a CI run, the run is already lost.

## Install GitLab CE on Ubuntu with Omnibus

The Omnibus package is the recommended path for most teams. It bundles GitLab and every service it depends on, then manages them through `gitlab-ctl`. You do not need to install PostgreSQL or Redis yourself, and upgrades stay predictable.

### 1. Prepare the server

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl ca-certificates tzdata perl openssh-server
```

### 2. Add the official repository

```bash
curl -fsSL https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
```

### 3. Install GitLab CE

Replace the URL with your real domain. Set the root password here so you do not have to hunt for the temporary one later.

```bash
sudo EXTERNAL_URL="https://git.yourdomain.com" \
  GITLAB_ROOT_PASSWORD="YourStrongPasswordHere" \
  apt install gitlab-ce
```

If DNS already resolves to the server and ports 80 and 443 are open, the installer requests a Let's Encrypt certificate during the first reconfigure. That first run compiles and starts every service, so give it several minutes and do not interrupt it.

### 4. Open the instance

Browse to `https://git.yourdomain.com` and sign in as `root`. If you did not pass a root password, the installer writes one to `/etc/gitlab/initial_root_password`, and that file is deleted automatically after 24 hours. Change the password on first login either way.

## Configure the Instance After Install

Every setting lives in `/etc/gitlab/gitlab.rb`. Edit it, then apply changes with `gitlab-ctl`. Do not edit the generated files under `/var/opt/gitlab`, because the next reconfigure overwrites them.

```bash
sudo nano /etc/gitlab/gitlab.rb
```

The settings below are the ones worth changing before you invite anyone:

```ruby
external_url 'https://git.yourdomain.com'

# Outbound email for password resets and notifications
gitlab_rails['smtp_enable'] = true
gitlab_rails['smtp_address'] = "smtp.yourprovider.com"
gitlab_rails['smtp_port'] = 587
gitlab_rails['smtp_user_name'] = "your-smtp-user"
gitlab_rails['smtp_password'] = "your-smtp-password"
gitlab_rails['smtp_domain'] = "yourdomain.com"
gitlab_rails['smtp_authentication'] = "login"
gitlab_rails['smtp_enable_starttls_auto'] = true

# Close public sign-up on a private instance
gitlab_rails['gitlab_signup_enabled'] = false
```

Apply the changes and check the result:

```bash
sudo gitlab-ctl reconfigure
sudo gitlab-ctl status
```

Day-to-day commands you will actually use:

```bash
sudo gitlab-ctl restart
sudo gitlab-ctl tail
sudo gitlab-rake gitlab:check SANITIZE=true
```

If SMTP is wrong, password resets fail silently and new users never receive invitations. Send yourself a test reset email before the first teammate joins. The [Omnibus configuration reference](https://docs.gitlab.com/omnibus/settings/) documents every SMTP key, including the `smtp_tls` and `smtp_openssl_verify_mode` options that trip people up on internal mail relays.

## Connect a GitLab Runner

CI/CD is the main reason to choose GitLab over a simpler Git host. The server schedules jobs. A runner executes them. Put the runner on a separate machine if you can, so a heavy pipeline cannot starve the GitLab web UI.

```bash
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
sudo apt install gitlab-runner
sudo gitlab-runner register
```

The registration wizard asks for your GitLab URL and a token. Find the token under **Settings > CI/CD > Runners** in the project or group you want to serve. Choose the Docker executor for most modern projects, and pick a default image such as `ruby:3.3` or `node:22`.

A minimal `.gitlab-ci.yml` proves the runner works end to end:

```yaml
stages:
  - test
  - build

test:
  stage: test
  image: node:22
  script:
    - npm ci
    - npm test

build:
  stage: build
  image: docker:27
  services:
    - docker:27-dind
  script:
    - docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA" .
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" "$CI_REGISTRY"
    - docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA"
```

The `$CI_REGISTRY_*` variables are injected by GitLab, so the job can push to the built-in registry without extra credentials. The [GitLab Runner documentation](https://docs.gitlab.com/runner/) covers executors, caching, and autoscaling when one runner stops being enough.

If you build static sites in CI, the workflow is the same one described in the [Codeberg Pages guide](/p/how-to-host-static-websites-codeberg-pages/) and the [Astro on GitHub Pages tutorial](/p/how-to-deploy-astro-github-pages/). Only the deploy target changes.

## Move Repositories Off GitHub

GitLab ships an importer. Go to **New project > Import project > GitHub**, authenticate with a personal access token, and choose the repositories to bring over. Issues, pull requests, labels, and wikis usually survive the trip, though review comments and Actions workflows do not.

For repositories you would rather move by hand, a mirror push is faster:

```bash
git clone --mirror git@github.com:yourorg/project.git
cd project.git
git push --mirror git@git.yourdomain.com:yourgroup/project.git
```

Then update your working copy so future pushes land on the new host:

```bash
git remote set-url origin git@git.yourdomain.com:yourgroup/project.git
```

GitHub Actions do not translate to GitLab CI. Expect to rewrite each workflow as a pipeline job, and budget real time for that step. It is the largest hidden cost of any migration.

## Keep the Instance Healthy

A GitLab instance fails in predictable ways: full disks, stale backups, and forgotten upgrades. Handle those three and you avoid most outages.

- **Back up on a schedule.** Run `sudo gitlab-backup create` from cron and copy the archive off the server.
- **Back up the secrets separately.** `/etc/gitlab/gitlab.rb` and `/etc/gitlab/gitlab-secrets.json` are required to restore. Without the secrets file, encrypted values in the database are unreadable.
- **Watch disk usage.** CI artifacts, container layers, and job logs grow faster than repositories. Set artifact expiry in project settings.
- **Enable two-factor authentication** for every account, and keep sign-up disabled.
- **Move heavy storage to object storage** once local disk hurts. S3-compatible buckets work for artifacts, LFS, uploads, and the registry.
- **Test a restore.** A backup you have never restored is a hope, not a backup.

For a home lab build, pair the instance with stable DNS so the external URL never changes. The [No-IP DynDNS guide](/p/noipat-dyndns-what-is-it-setup-guide/) covers the dynamic DNS side, and a reverse proxy with a real certificate keeps GitLab's built-in Let's Encrypt automation simple.

## When Self-Hosting Is the Wrong Choice

Self-hosting is a maintenance commitment, not a one-time install. If nobody on the team wants to own upgrades, backups, and certificate renewals, a managed Git host is cheaper than the hours you will spend.

It is also the wrong choice when compliance requires a vendor with a support contract. GitLab CE has a community forum, not a phone number. Enterprise Edition adds support, and it costs money.

The honest trade is this: you gain data ownership, unlimited private repositories, and no per-seat fee. You take on patching, monitoring, and the 2 a.m. disk-full alert.

## Key Takeaways

- GitLab CE is a full DevOps platform, not just a Git host, and it needs real hardware: 8 GB RAM minimum, 16 GB recommended.
- The Omnibus package is the simplest reliable install path on Ubuntu, and `gitlab-ctl` manages every bundled service.
- Set the external URL and DNS before installing so Let's Encrypt works on the first try.
- Register a runner early, ideally on a separate host, so CI/CD is available from day one.
- Back up both the archive and `gitlab-secrets.json`, or a restore will not work.
- Gitea and Forgejo win on weight. GitLab wins on built-in registries, pipelines, and permissions.

## Conclusion

Self-hosting GitLab is a trade, not a free lunch. You spend server cost and maintenance hours to gain ownership of your code, your pipelines, and your access rules. For a team that already depends on CI/CD and container images, that trade is often worth it. For a solo developer pushing commits once a week, a lighter host will serve you better.

Start with the Omnibus install, get backups running before you invite anyone, and add a runner when the first real pipeline arrives. Everything else can wait.

The [F9XR Team](/p/hello-world/) publishes these guides as part of its open-source developer education work. If you want to improve this article or write your own, read the [Contributor Guide](/contribute/) and the [Editorial Policy](/editorial-policy/) before you pitch.

## Frequently Asked Questions

### How much RAM does self-hosted GitLab really need?

GitLab's official baseline for a single-node install is 16 GB. It can run on 8 GB for small teams with light usage, but performance and reliability improve significantly with more memory. Avoid running it on less than 8 GB in production.

### Is GitLab CE free forever?

Yes. The Community Edition is open source, with an MIT-licensed core, and free to self-host indefinitely. Paid features exist in the Enterprise Edition, but CE already includes the core Git hosting, CI/CD, registry, and issue tracking most teams need.

### Can I run GitLab on a home lab or low-cost VPS?

Yes, provided the machine meets the minimum specs. Many developers successfully run small instances on 8 to 16 GB VPS plans or home servers. Just monitor resources and keep backups off-site.

### How do I update GitLab safely?

Run `sudo apt update && sudo apt install gitlab-ce` followed by `sudo gitlab-ctl reconfigure`. Always read the [official upgrade notes](https://docs.gitlab.com/update/) for major version jumps, as intermediate versions are sometimes required.

### GitLab vs Gitea: which should I pick?

Choose Gitea or Forgejo if you want something lightweight that feels like a simple GitHub clone. Choose GitLab when you need mature CI/CD, a container registry, package registry, and advanced permission models out of the box.

---

*This guide was researched and drafted with the assistance of an AI coding assistant, then reviewed by the F9XR Review Board before publishing. GitLab's requirements and pricing change over time, so confirm details against the [official installation docs](https://about.gitlab.com/install/) and the [system requirements](https://docs.gitlab.com/install/requirements/) before you provision hardware.*
