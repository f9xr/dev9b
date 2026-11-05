Every developer who has shipped an AI feature knows the sinking feeling. You launch, a few people share it, traffic jumps, and then you open the billing page. Model calls, storage, database reads, egress. All of it lands on your card, and all of it grows with every new user.

Puter.js tries to flip that arrangement. It is a JavaScript SDK that gives a frontend app authentication, cloud storage, a key-value database, an AI gateway, hosting and serverless workers, with no servers to run and no API keys to manage. The unusual part is who pays: each user covers their own usage through their own Puter account.

This guide explains what Puter.js is, how the **user-pays model** works, where it fits, where it does not, and how to build and deploy a small SaaS app with it from scratch.

> **NOTE** â€” Quick answer
>
> Puter.js is an open-source, serverless JavaScript SDK that adds auth, cloud storage, a KV database, AI models, hosting and workers to web apps without a traditional backend. Under its user-pays model, every user's usage is billed to their own Puter account, so the developer's infrastructure bill stays at $0 at any user count.
>

## What Is Puter.js?

Puter.js is the developer SDK of Puter, a platform and web-based "internet operating system" built by Puter Technologies Inc. (founded in 2022, based in Vancouver). The core Puter platform is open source under AGPL-3.0, and its GitHub repository has passed 42,000 stars according to a public tool listing.

The SDK works in the browser through a script tag or npm, in Node.js, and inside Puter's serverless workers. It is framework agnostic, with starter templates for React, Next.js, Vue, Angular, Svelte, Astro, vanilla JavaScript and Node.js with Express.

### What You Get Out of the Box

| Capability | API namespace | What it does |
|---|---|---|
| Authentication | `puter.auth` | Users sign in with a Puter account, no auth server to build |
| Cloud storage | `puter.fs` | Per-user file storage with an app directory |
| Key-value database | `puter.kv` | Serverless NoSQL store, sandboxed per app and user |
| AI gateway | `puter.ai` | Chat, image, video, speech and OCR APIs, with 500+ models listed on the developer portal |
| Hosting | `puter.hosting` | Publish static sites to a `puter.site` subdomain |
| Serverless workers | Workers | HTTP endpoints and backend logic on `puter.work` |
| Networking and peers | `puter.net` | TCP sockets and real-time peer connections in the browser |

### Related Terms You Will See

- **User-Pays Model:** Users cover their own cloud and AI usage instead of the developer.
- **Keyless architecture:** No provider API keys live in your code, so there is nothing to leak.
- **Serverless Workers:** Small backend routes you deploy as a single JavaScript file.
- **AI gateway:** One interface to models from OpenAI, Anthropic, Google, xAI and others.
- **BaaS (backend as a service):** The category that includes Supabase and Firebase, where Puter.js competes.

## How the User-Pays Model Works

This is the idea that makes Puter.js different, so it deserves a close look.

In a traditional stack, you create the backend, pay for every user's database rows and AI calls, and then build rate limiting, quotas and abuse protection to stop anyone from running up the bill. In Puter.js:

1. A user signs in with their Puter account when your app first touches a cloud feature.
2. Every call, whether AI, storage or KV, is metered against that user's allowance, not yours.
3. Each Puter account includes a free monthly allowance. A heavy user who runs out can top up with Puter directly.

According to the official docs, you also pay for your own usage when you use your own app, just like any other user.

| | Traditional backend | Puter.js |
|---|---|---|
| Servers and databases | You provision and pay | None needed |
| API keys | You manage and secure them | No API keys |
| Billing | You pay for all users | Each user pays their own |
| Scaling cost | Grows with users | Does not grow for you |
| Abuse protection | Rate limits, CAPTCHAs, quotas | Mostly handled by per-user limits |

There is a security angle worth noting. If you have read about the [AI token black market](https://f9xr.org/dev9b/p/ai-token-black-market-how-it-works/), where stolen provider keys get resold, a keyless design removes one of the biggest causes of that problem for your project. There is simply no provider key in your frontend to steal.

## When Puter.js Is a Good Fit

Puter.js shines for projects where infrastructure cost and setup time are the main pain.

- **AI-powered tools and wrappers.** Chat assistants, summarizers, image generators and writing tools where inference cost would otherwise eat your margin.
- **MVPs and weekend projects.** You can go from idea to a hosted app in an afternoon.
- **Vibe-coded apps.** Puter publishes an `llms.txt` file with its full API so coding agents can read it, and offers a hosted MCP server. See our take on [vibe coder vs vibe engineer](https://f9xr.org/dev9b/p/vibe-coder-vs-vibe-engineer/) for the trade-offs of building this way.
- **Utility apps for individuals.** Notes, trackers, file tools and editors where each person's data is private anyway.

## When Puter.js Is Not the Right Choice

Be honest with yourself about these limits before you commit.

| Limitation | Why it matters |
|---|---|
| Users need a Puter account | Extra sign-up friction compared with a plain email or Google login |
| Data lives in each user's account | Cross-user features need a Serverless Worker acting on your own resources |
| You do not control pricing to users | Puter bills users for resource usage, so a classic "per seat" SaaS model needs extra work |
| Platform dependence | Your app relies on Puter's availability, limits and policies |
| Strict per-call limits | Values in KV are capped (about 399 KB each), and free accounts have lower rate limits |
| Self-hosting license | The core platform is AGPL-3.0, which matters if you modify and host it |

On monetization specifically, the user-pays model removes your cost, but it does not by itself give you revenue. If you want to charge for premium features, you would typically add your own payment layer (for example a worker that verifies a subscription) on top. Check the current Puter docs and terms on this before you plan a business around it.

## How to Build a SaaS App With Puter.js (Step by Step)

We will build a small SaaS-style tool called **QuickNotes AI**. Users sign in, save notes, and get an AI summary of each note. It needs auth, storage and AI, which is exactly where Puter.js is strongest.

### Step 1: Set Up Your Project

You have two options. For the simplest start, use the CDN:
```html
<script src="https://js.puter.com/v2/"></script>
```

For a framework project, install the package:
```bash
npm install @heyputer/puter.js
```
```javascript
import puter from "@heyputer/puter.js";
```

If you use Next.js, add the `"use client"` directive to components that call Puter, because the SDK needs browser APIs. On Next.js 15 or earlier, enable Turbopack. Version 16 and later has it on by default.

**Important:** serve the page from a real origin. Puter identifies your app by its origin, so opening an HTML file straight from disk (`file:///`) will fail with an "Unsupported Origin" message. Run a local server instead:
```bash
python3 -m http.server
# then open http://localhost:8000
```

### Step 2: Add Authentication

You do not need to build a login system. Puter.js prompts users to sign in the first time your code touches a cloud service. You can also trigger it yourself:
```javascript
async function login() {
  if (!puter.auth.isSignedIn()) {
    await puter.auth.signIn();
  }
  const user = await puter.auth.getUser();
  console.log("Signed in as", user.username);
}
```

### Step 3: Store Data With the KV Database

Each app gets its own sandboxed key-value store inside the user's account. Other apps cannot read it.
```javascript
async function loadNotes() {
  const raw = await puter.kv.get("notes");
  return raw ? JSON.parse(raw) : [];
}

async function saveNotes(notes) {
  await puter.kv.set("notes", JSON.stringify(notes));
}
```

For larger content such as documents or exports, use `puter.fs` to write files into the user's app directory instead.

### Step 4: Add AI Features

Here is the part that normally costs money. With Puter.js, the call is one line, and the user's allowance pays for it.
```javascript
async function summarize(text) {
  const res = await puter.ai.chat(
    `Summarize this note in two sentences:\n\n${text}`,
    { model: "gpt-5-nano" }
  );
  // Different providers return slightly different shapes
  return typeof res === "string"
    ? res
    : res?.message?.content?.[0]?.text ?? String(res);
}
```

Model names and prices change. Call `puter.ai.listModels()` or check the AI model directory on the developer portal before you hard-code a model.

### Step 5: Put It Together

Here is a compact single-file version of QuickNotes AI.
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>QuickNotes AI</title>
</head>
<body>
  <h1>QuickNotes AI</h1>
  <button id="login">Sign in with Puter</button>
  <textarea id="note" rows="4" cols="50" placeholder="Write a note"></textarea>
  <button id="save">Save and summarize</button>
  <ul id="list"></ul>

  <script src="https://js.puter.com/v2/"></script>
  <script>
    const list = document.getElementById("list");

    async function loadNotes() {
      const raw = await puter.kv.get("notes");
      return raw ? JSON.parse(raw) : [];
    }

    async function render() {
      const notes = await loadNotes();
      list.innerHTML = "";
      notes.forEach((n) => {
        const li = document.createElement("li");
        li.textContent = n.text + " | Summary: " + n.summary;
        list.appendChild(li);
      });
    }

    async function summarize(text) {
      const res = await puter.ai.chat(
        "Summarize in two sentences: " + text,
        { model: "gpt-5-nano" }
      );
      return typeof res === "string"
        ? res
        : res?.message?.content?.[0]?.text ?? String(res);
    }

    document.getElementById("login").onclick = async () => {
      await puter.auth.signIn();
      render();
    };

    document.getElementById("save").onclick = async () => {
      const text = document.getElementById("note").value.trim();
      if (!text) return;
      try {
        const summary = await summarize(text);
        const notes = await loadNotes();
        notes.push({ text, summary, at: Date.now() });
        await puter.kv.set("notes", JSON.stringify(notes));
        document.getElementById("note").value = "";
        render();
      } catch (err) {
        // Handles 402 (out of credit), 429 (rate limit) and similar
        alert("Something went wrong: " + (err.message || err.code));
      }
    };
  </script>
</body>
</html>
```

### Step 6: Add a Shared Backend With Workers

Per-user storage is private. If you need data that all users share, such as a public leaderboard, a global counter or admin settings, use a **Serverless Worker**. Workers run your own JavaScript and can act on your resources.
```javascript
// api.js (deployed as a Puter worker)
router.get("/api/hello", async ({ request }) => {
  return { message: "Hello, World!" };
});

router.post("/api/vote", async ({ request }) => {
  const body = await request.json();
  // me.puter points at your own developer resources
  const total = await me.puter.kv.incr("votes");
  return { ok: true, total };
});
```

The docs describe a dual-context model in workers: `me.puter` for your own resources and `user.puter` for the current user's resources, billed to that user. Read the Workers documentation for the exact current API before building on this.

### Step 7: Deploy

You can deploy from the Puter CLI. It needs Node 18 or newer.
```bash
npm install -g @heyputer/cli
puter login

# Deploy a static build to my-app.puter.site
puter site deploy ./dist my-app

# Deploy a worker to my-api.puter.work
puter worker deploy ./api.js my-api
```

The CLI is in beta, so behavior may change between releases. For CI, set the `PUTER_AUTH_TOKEN` environment variable and the CLI skips interactive login.

If you want a branded URL, you can also host the front end elsewhere. Our guides on [hosting static sites with Codeberg Pages](https://f9xr.org/dev9b/p/how-to-host-static-websites-codeberg-pages/), [GitHub Pages with a Cloudflare custom domain](https://f9xr.org/dev9b/p/github-pages-custom-domain-cloudflare/) and [free subdomains for developers](https://f9xr.org/dev9b/p/free-subdomains-for-developers-list/) cover those options. Puter.js still works from any website, since it identifies your app by origin.

## Using AI Coding Agents With Puter.js

Puter leans into agent-driven development. Two things are useful here:

- **`llms.txt`:** Puter publishes its documentation in a format that coding agents can read in one request.
- **MCP server:** A hosted MCP server at `https://mcp.puter.com/` lets tools like Claude Code, Codex, Cursor and OpenCode manage your files, sites and workers.
```bash
claude mcp add --transport http --scope user puter https://mcp.puter.com/
```

Then authenticate with Puter and ask your agent in plain language, for example "Publish the dist folder as a website." If you are new to this setup, read our explainers on [AI coding agents](https://f9xr.org/dev9b/p/ai-coding-agents-explained/) and [OpenCode MCP servers](https://f9xr.org/dev9b/p/opencode-mcp-servers/).

## Puter.js vs Supabase and Firebase

| Factor | Puter.js | Supabase or Firebase |
|---|---|---|
| Setup | Script tag or npm install | Project creation and configuration |
| Who pays for usage | Each user | You |
| Auth | Puter account sign in | Email, social and more, fully customizable |
| Database | Key-value store | SQL (Supabase) or document store (Firebase) |
| Data isolation | Automatic per user | Manual rules such as row level security |
| Custom business logic | Serverless Workers | Edge functions and cloud functions |
| Best for | AI tools, MVPs, personal apps | Apps needing relational data and full control |

If your product needs complex relational queries, custom user accounts or a classic subscription billing flow, a conventional BaaS is usually the safer base. If you want to ship quickly and avoid usage bills, Puter.js is worth a serious look.

## Practical Tips Before You Ship

1. **Handle errors on purpose.** The SDK shows users an upgrade dialog for out-of-credit and storage errors, but your promise still rejects. Catch `402`, `429` and `413` errors so your UI does not fail silently.
2. **Back off on rate limits.** Free accounts have tighter limits, for example 30 AI requests per 10 seconds. Retry with a delay on `429`.
3. **Watch egress.** The docs call out egress, bytes sent to the client, as the cost developers underestimate. Keep responses lean.
4. **Do not store big blobs in KV.** Values are capped at about 399 KB. Use `puter.fs` for large data.
5. **Store large numbers as strings.** KV clamps numbers beyond the safe integer range.
6. **Plan your shared data early.** Decide which data is per user and which must live in a worker.
7. **Pin your model choices.** Model names and pricing change. Make the model a config value you can update quickly.
8. **Design for an exit.** Wrap Puter calls in a small data layer so you can swap providers later if you need to.
9. **Test signed-out states.** Make sure your UI explains clearly why sign in is needed.
10. **Read the terms.** Confirm current policy on branding, monetization and acceptable use.

## Key Takeaways

- **Puter.js is a serverless JavaScript SDK** that gives frontend apps auth, storage, a KV database, AI, hosting and workers.
- The **user-pays model** bills each user's usage to their own Puter account, so your infrastructure cost does not grow with users.
- It is **keyless**, which removes the risk of leaking provider API keys from your app.
- It is a strong fit for **AI tools, MVPs and personal apps**, and a weaker fit for apps needing relational data or classic per-seat billing.
- **Shared data across users needs a Serverless Worker**, because each user's storage is isolated.
- You can **deploy with the Puter CLI** to `puter.site` and `puter.work`, or use Puter.js from any website.
- **Handle `402`, `429` and `413` errors** and respect rate limits to keep your UX smooth.
- Treat monetization as a separate design question, and **check the latest Puter docs and terms** before building a business model around it.

## Frequently Asked Questions

### What is Puter.js?

Puter.js is an open-source, serverless JavaScript SDK from Puter that adds authentication, cloud storage, a key-value database, AI models, hosting and serverless workers to web apps. It runs in the browser, Node.js and Puter workers, and needs no backend servers or API keys.

### What is the user-pays model in Puter.js?

In the user-pays model, each app user covers their own storage, database and AI usage through their own Puter account, not the developer. Every account gets a free monthly allowance, and heavy users can top up directly with Puter, so the developer's infrastructure cost stays at $0.

### Is Puter.js free to use?

Puter.js is free for developers to build with, because usage is billed to each user's Puter account. Users get a free monthly allowance, and paid plans or purchased credit cover heavier use. Developers still pay for their own usage when they use their own app.

### Do I need API keys to use AI models with Puter.js?

No. Puter.js is keyless, so you can call models from providers such as OpenAI, Anthropic and Google through `puter.ai.chat()` without creating or storing provider API keys.

### How do I install Puter.js?

Add `<script src="https://js.puter.com/v2/"></script>` to your page, or run `npm install @heyputer/puter.js` and import it. Serve your page from a real origin such as `http://localhost`, because opening a local file directly is not supported.

### Can I build a SaaS app with Puter.js?

Yes, especially AI-powered tools and MVPs. You can use `puter.auth` for sign in, `puter.kv` and `puter.fs` for data, `puter.ai` for models and workers for shared backend logic. For paid subscriptions, plan an additional billing layer and check Puter's current terms.

### How do I share data between users in Puter.js?

Each user's storage is private to their account, so shared data needs a Serverless Worker. A worker can act on the owner's resources, which gives all users a single shared backend for things like leaderboards or global settings.

### How do I deploy a Puter.js app?

Install the Puter CLI with `npm install -g @heyputer/cli`, log in with `puter login`, then run `puter site deploy ./dist my-app` to publish a static site to `my-app.puter.site`. Use `puter worker deploy ./api.js my-api` for backend workers.

### How is Puter.js different from Supabase or Firebase?

Supabase and Firebase require project setup and bill the developer for usage. Puter.js needs no setup beyond one library and bills each user for their own usage. The trade-off is a simpler key-value data model and a dependency on Puter accounts.

### Is Puter.js open source?

The core Puter platform is open source under the AGPL-3.0 license and is developed publicly on GitHub. Review the license carefully if you plan to modify and host the platform yourself.

## Conclusion

Puter.js is a useful answer to a specific problem: you want to ship an AI-powered app without becoming a cloud billing department. The user-pays model and keyless design remove two of the biggest costs and risks for a small team. It will not fit every product, especially one that needs relational data, full control over accounts or classic per-seat subscriptions.

If you want to try it, start with the QuickNotes AI example, deploy it to a `puter.site` subdomain, and watch how the user-pays flow behaves with real people. Read the [Contributor Guide](https://f9xr.org/dev9b/contribute/) and [Editorial Policy](https://f9xr.org/dev9b/editorial-policy/) if you want to share your own build with the Dev9b community.

## Sources

- Puter.js official documentation and User-Pays Model page
- Puter developer portal, pricing and tutorials
- Puter blog comparison with Supabase
- Puter.js listing on EveryDev.ai
- Puter on GitHub (HeyPuter/puter)

*Note: Puter.js features, limits, model names and pricing change often. Verify details in the official docs before you build.*

*Disclosure: This article was drafted with AI assistance and reviewed and edited by the F9XR Team. Product details, limits and pricing change frequently. Verify current facts on the official Puter site before you build on it.*
