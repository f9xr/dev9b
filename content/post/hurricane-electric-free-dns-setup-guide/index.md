---
title: "Hurricane Electric Free DNS: Setup Guide for Devs"
description: "Learn what Hurricane Electric Free DNS (dns.he.net) is and how to set it up. Free dual-stack DNS, DDNS, reverse zones. Step-by-step for developers."
slug: hurricane-electric-free-dns-setup-guide
date: 2026-11-16
image: cover.jpg
author: F9XR Team
keywords: hurricane electric free dns, dns.he.net, free dns, dynamic dns, hurricane electric nameservers, ddns, reverse dns, ipv6 dns, free authoritative dns, he.net
categories:
    - Tutorials
tags:
    - dns
    - self-hosting
    - developer-tools
    - indie-hackers
draft: false
math: false
faq:
    - question: "What is Hurricane Electric Free DNS?"
      answer: "Hurricane Electric Free DNS is a no-cost authoritative DNS hosting service at dns.he.net. It lets you manage forward and reverse zones, supports dual-stack IPv4 and IPv6, dynamic DNS, and many record types, all hosted on Hurricane Electric's global network."
    - question: "Is Hurricane Electric DNS really free?"
      answer: "Yes. There is no paid tier inside the Free DNS product and no credit card required. The service has remained free for years."
    - question: "How do I change nameservers to Hurricane Electric?"
      answer: "At your domain registrar, replace the existing nameservers with ns1.he.net, ns2.he.net, ns3.he.net, ns4.he.net, and ns5.he.net. Then wait for propagation."
    - question: "Does dns.he.net support Dynamic DNS?"
      answer: "Yes. Enable the option on an A, AAAA, or TXT record, generate a DDNS key, and update the record with a curl request to dyn.dns.he.net. Both IPv4 and IPv6 are supported."
    - question: "Does Hurricane Electric Free DNS support DNSSEC?"
      answer: "No. dns.he.net does not offer DNSSEC signing for hosted zones. If you require signed zones or DS records, you will need a different provider."
    - question: "Can I use HE DNS for reverse DNS?"
      answer: "Yes. Reverse zone support, including several formats for IPv4 and IPv6, is one of the stronger features of the service and is fully free."
---

Most developers eventually hit the same wall. You need reliable DNS for a side project, a home lab, or a personal domain, but you do not want to pay Cloudflare, Route 53, or DNSimple every month just to point a few records. Hurricane Electric Free DNS, available at dns.he.net, has quietly filled that gap for years.

It is a no-cost authoritative DNS hosting service run by one of the largest IPv6 backbone operators in the world. You get forward zones, reverse zones, dynamic DNS for both IPv4 and IPv6, slave zone support, and a surprisingly wide list of record types. No credit card, no paid tier inside the product, and the nameservers sit on a real global network.

This guide walks through exactly what the service offers, how to get a domain running on it, how to enable dynamic DNS, and the practical limits you should know before you depend on it for production traffic.

<!--more-->

## What Hurricane Electric Free DNS Actually Is

Hurricane Electric, usually just called HE, is a major internet backbone and colocation provider based in Fremont, California. Their free DNS portal at [dns.he.net](https://dns.he.net) lets you host the authoritative DNS for domains you control.

![The Hurricane Electric Free DNS portal homepage showing the login form and the list of supported features such as dual-stack support, slave mode and reverse zones](dns-he-net-portal-homepage.png "dns.he.net Free DNS management portal")

*The dns.he.net portal in November 2026. The feature list on the front page is still the clearest summary of what the service does.*

Key capabilities:

- Forward DNS zones (normal hostname to IP mapping)
- Reverse DNS zones (IP to hostname, useful for mail servers and IPv6)
- Dual-stack support: queries work over both IPv4 and native IPv6
- Dynamic DNS for A, AAAA, and even TXT records
- Slave (secondary) zone support so HE can act as a backup nameserver
- Multiple domains under one free account
- Geographically diverse name servers
- Delegation sanity checks that flag common misconfigurations

Supported record types include A, AAAA, ALIAS, CNAME, CAA, MX, NS, TXT, SRV, SSHFP, SPF, RP, NAPTR, HINFO, LOC, and PTR. The interface enforces a minimum TTL of 300 seconds, which is five minutes.

One notable gap: HE's free DNS does not offer DNSSEC signing. If signed zones are a hard requirement for your project, plan for a different provider.

## Why Developers Still Choose dns.he.net in 2026

Plenty of free DNS options exist. Cloudflare is the default for many. What keeps people coming back to HE?

- It is genuinely free, with no paid upsell path inside the DNS product.
- Native IPv6 and reverse DNS are first-class, which is still rare among free offerings.
- Dynamic DNS works for both IPv4 and IPv6 and is simple to script with curl.
- It pairs naturally with HE's free Tunnelbroker IPv6 tunnels.
- The service has been stable for a long time. The interface looks dated, but the servers do not.

For home labs, personal sites, mail servers that need proper reverse DNS, or as a secondary nameserver behind another primary, it remains one of the better zero-cost choices. If you are weighing providers, our [Anycast DNS explainer](/p/anycast-dns-what-is-it-setup-guide/) covers the routing model behind the bigger commercial networks, and the [free subdomains for developers roundup](/p/free-subdomains-for-developers-list/) lists the naming services that pair well with your own zone.

![Promotional overview of Hurricane Electric Free DNS showing the dns.he.net laptop, global network and the three selling points: reliable DNS, fast global service and easy setup](hurricane-electric-free-dns-overview.webp "Hurricane Electric Free DNS overview")

## How to Set Up Hurricane Electric Free DNS

The process is straightforward. Allow 10 to 20 minutes plus DNS propagation time.

### Step 1: Create an Account

1. Go to [https://dns.he.net](https://dns.he.net) and click Register.
2. Fill in the required fields: username, password, email, name, address, and phone.
3. Confirm the account via the email HE sends.
4. Log in. You should land on the Free DNS management page.

Existing HE Tunnelbroker or colocation customers can often use the same credentials, or request a password from support.

### Step 2: Add Your Domain

1. On the main DNS page, look for the zone functions or the add-a-new-domain option.
2. Enter the domain name, for example `example.com`, and submit.
3. The domain appears in your list. Click the edit icon next to it to manage records.

You can add multiple domains to the same account, and each one is managed independently.

### Step 3: Create Basic Records

Inside the zone editor:

- Click **New A** for IPv4. Leave the name field empty, or use `@`, for the apex, enter your server IP, set the TTL to 300 or 1800, and submit.
- Create another A record with the name `www` pointing to the same IP if needed.
- Add AAAA records the same way for IPv6 addresses.
- Use **New CNAME**, **New MX**, **New TXT**, and the rest for your other needs.

For dynamic DNS later, check the **Enable entry for dynamic dns** box when creating the A or AAAA record.

### Step 4: Point Your Domain's Nameservers

This is the step that actually moves resolution to HE.

Log into your domain registrar, whether that is Namecheap, Porkbun, Cloudflare Registrar, or another, and replace the current nameservers with:

```
ns1.he.net
ns2.he.net
ns3.he.net
ns4.he.net
ns5.he.net
```

Save the change. Propagation usually takes anywhere from a few minutes to several hours. You can watch it with `dig`, `nslookup`, or an online DNS checker. If your registrar is Cloudflare, the workflow is similar to the one in our [Cloudflare to GitHub Pages domain guide](/p/github-pages-custom-domain-cloudflare/), except here you are handing authoritative DNS to HE rather than keeping it inside Cloudflare.

### Step 5: Verify Everything Works

After propagation:

```bash
dig example.com @ns1.he.net
dig www.example.com A
dig example.com AAAA
```

Confirm the answers match what you configured. HE also performs basic delegation and syntax checks, and the panel often flags a broken setup before you have to debug it from the outside.

## Setting Up Dynamic DNS (DDNS)

Many developers use HE specifically for dynamic DNS on home connections or VPS instances with changing IPs.

1. When creating or editing an A or AAAA record, enable the dynamic DNS option.
2. In the record list, click the key icon in the DDNS column.
3. Save the generated password or key. It is independent of your account login password.

Update the record with a simple curl command. The username is the record name, and the password is the DDNS key:

```bash
# Autodetect IPv4
curl -4 "https://dyn.example.com:YOUR_DDNS_KEY@dyn.dns.he.net/nic/update?hostname=dyn.example.com"

# Autodetect IPv6
curl -6 "https://dyn.example.com:YOUR_DDNS_KEY@dyn.dns.he.net/nic/update?hostname=dyn.example.com"

# Explicit IP
curl "https://dyn.dns.he.net/nic/update?hostname=dyn.example.com&password=YOUR_DDNS_KEY&myip=203.0.113.10"
```

You can put these in a cron job, a systemd timer, or a router script. The same endpoint supports dynamic TXT records, which is useful for Let's Encrypt DNS-01 challenges: create the TXT record first, enable DDNS on it, then let your ACME client write the challenge value. The [Let's Encrypt challenge types documentation](https://letsencrypt.org/docs/challenge-types/) explains why that path matters when your server is not reachable on port 80.

If you prefer a dedicated dynamic DNS provider rather than running a zone at HE, our [noip.at DynDNS guide](/p/noipat-dyndns-what-is-it-setup-guide/) covers a lighter option for a single hostname.

```mermaid
flowchart LR
    A[Register at dns.he.net] --> B[Add your domain]
    B --> C[Create A / AAAA records]
    C --> D[Change nameservers at registrar]
    D --> E[Wait for propagation]
    E --> F[Optional: enable DDNS]
    F --> G[Script updates with curl]
```

## Practical Tips and Limitations

- TTL starts at 300 seconds. Lower values help during testing; raise them once things are stable.
- There is no documented public API for bulk record management. Community tools and scripts exist that drive the web interface or the DDNS endpoint, but treat them carefully.
- DNSSEC is missing. Plan accordingly if you need signed zones or DS records at your registrar.
- The web UI is functional but old-school. Bookmark your domain list.
- Reverse DNS is a real strength. If you have a /48 or smaller IPv6 allocation, HE makes reverse zones relatively painless.
- Use it as secondary DNS: add the zone as a slave and let it pull from your primary with AXFR.

For most personal projects and many small production sites, these trade-offs are acceptable. The one that matters most in practice is DNSSEC: if a customer or compliance rule requires it, HE cannot be your primary provider.

## Where HE DNS Fits in a Real Stack

We use free DNS in the least interesting way possible: as the authoritative zone for demo apps and internal tools, with the actual site hosted elsewhere. That split is the useful part. Keep DNS and hosting separate, and moving a site later becomes a nameserver or record change instead of a migration project.

Two combinations work well:

- **Static site on a free host, DNS at HE.** Point the apex and `www` at your host, and keep the zone in HE. Our walkthrough for [hosting static sites on Codeberg Pages](/p/how-to-host-static-websites-codeberg-pages/) uses exactly this shape.
- **Registrar plus HE for mail and reverse DNS.** Keep the website where it is and move only the MX and PTR records that need HE's reverse zone support.

If you are setting up a blog rather than an app, the [Blogger custom domain via Cloudflare guide](/p/blogger-custom-domain-cloudflare-setup/) shows the same record work from a different provider's angle. The record types do not change; only the panel does. And if you are launching an AI side project, a free [is-an.ai subdomain for your AI SaaS](/p/free-is-an-ai-subdomain-for-ai-saas-cli-guide/) can sit in front of a HE-hosted zone while you validate the idea.

## Key Takeaways

- Hurricane Electric Free DNS at dns.he.net is a completely free authoritative DNS service with strong IPv6 and reverse DNS support.
- Setup is: register, add the domain, create records, then change nameservers at the registrar to ns1 through ns5.he.net.
- Dynamic DNS works through a simple authenticated HTTP request and covers A, AAAA, and TXT records.
- There is no DNSSEC. That is the main reason some teams still choose a paid alternative.
- It suits home labs, personal domains, secondary DNS, and anyone already using HE Tunnelbroker.
- Multiple domains and normal record volumes fit under one free account.

## Frequently Asked Questions

### What is Hurricane Electric Free DNS?

Hurricane Electric Free DNS is a no-cost authoritative DNS hosting service at dns.he.net. It lets you manage forward and reverse zones, supports dual-stack IPv4 and IPv6, dynamic DNS, and many record types, all hosted on Hurricane Electric's global network.

### Is Hurricane Electric DNS really free?

Yes. There is no paid tier inside the Free DNS product and no credit card required. The service has remained free for years.

### How do I change nameservers to Hurricane Electric?

At your domain registrar, replace the existing nameservers with ns1.he.net, ns2.he.net, ns3.he.net, ns4.he.net, and ns5.he.net. Then wait for propagation.

### Does dns.he.net support Dynamic DNS?

Yes. Enable the option on an A, AAAA, or TXT record, generate a DDNS key, and update the record with a curl request to dyn.dns.he.net. Both IPv4 and IPv6 are supported.

### Does Hurricane Electric Free DNS support DNSSEC?

No. dns.he.net does not offer DNSSEC signing for hosted zones. If you require signed zones or DS records, you will need a different provider.

### Can I use HE DNS for reverse DNS?

Yes. Reverse zone support, including several formats for IPv4 and IPv6, is one of the stronger features of the service and is fully free.

## Conclusion

Hurricane Electric Free DNS will not replace a full-featured commercial platform if you need DNSSEC, advanced traffic steering, or polished APIs. For a large number of developer projects, however, it remains one of the most capable free options available. Set it up once, point your nameservers, and you can stop thinking about monthly DNS bills.

If you run into something this guide does not cover, the [HE DNS documentation](https://dns.he.net/docs.html) and the [Hurricane Electric main site](https://he.net) are the places to check first. To share your own setup notes, read our [contributor guide](/contribute/). The [editorial policy](/editorial-policy/) explains how we check product details and links before publishing. This article was drafted with AI assistance and reviewed by the F9XR Team against the dns.he.net portal and HE's public documentation.
