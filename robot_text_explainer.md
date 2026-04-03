# Understanding robots.txt -- A Primer for the Age of AI Agents

## What robots.txt Is

Every website can host a small plain-text file at its root called `robots.txt`. If you visit any major website and append `/robots.txt` to the domain -- for example, `https://nytimes.com/robots.txt` -- you will see it. The file has been around since 1994, when it was introduced as the Robots Exclusion Protocol (REP). Its purpose is simple: to tell automated software ("bots", "crawlers", "spiders") which parts of a website they are welcome to access and which parts they should leave alone.

The key word is "should." Compliance with robots.txt has always been voluntary. The file is a statement of preference, not a technical barrier. A well-behaved crawler reads it and respects it. A malicious scraper ignores it entirely. This distinction -- between expressed intent and enforced access control -- is fundamental to understanding both the power and the limitations of robots.txt.


## How It Works

The syntax is minimal. A robots.txt file consists of one or more blocks, each targeting a specific "user-agent" (the name a crawler identifies itself by) and listing paths that are allowed or disallowed.

A basic example:

```
User-agent: Googlebot
Allow: /
Disallow: /private/

User-agent: *
Disallow: /admin/
```

This says: Googlebot can access everything except the `/private/` directory. All other bots are blocked from `/admin/` but allowed everywhere else.

The wildcard `*` matches any crawler that does not have its own specific block. Rules are matched by specificity -- a longer, more specific path takes precedence over a shorter one. The file can also include a `Sitemap:` directive pointing crawlers to a site's XML sitemap for more efficient discovery.

That is essentially the entire protocol. There is no authentication, no encryption, no handshake, no negotiation. It is a flat file read once at the start of a crawl.


## What robots.txt Was Designed For

In the 1990s and 2000s, the web had a relatively manageable number of crawlers, almost all operated by search engines. The social contract was straightforward: search engines index your content so people can find it, and in return, you allow their crawlers access while using robots.txt to keep them out of administrative pages, duplicate content, or areas that would waste their crawl budget.

The protocol worked well under these conditions because the participants were few, identifiable, and had reputational incentives to comply. Google, Bing, Yahoo, and their peers publicly committed to honouring robots.txt directives. Non-compliance would damage their credibility with webmasters who could simply deindex their sites.


## Why robots.txt Is Under Pressure

The AI era has introduced a fundamentally different class of automated web interaction, and robots.txt was not designed for it. Three structural limitations have become acute:

**It controls access but not usage.** robots.txt can say "do not crawl this path." It cannot say "you may read this page but not use it for model training" or "you may retrieve this article for citation but not reproduce it in generated output." The distinction between crawling-for-indexing and crawling-for-training is invisible to the protocol. A site owner who wants to appear in AI-powered search results but does not want their content ingested into training datasets has no way to express that distinction through robots.txt alone.

**It has no semantic layer.** A web page may contain text, images, code, user-generated comments, and embedded media. An owner might want to permit summarisation of their articles while prohibiting extraction of their images. robots.txt treats an entire URL as a single unit -- it is either allowed or disallowed, with no granularity about what an agent does with the content it retrieves.

**It cannot distinguish between agent types.** The protocol identifies crawlers by user-agent string, but the AI ecosystem now includes dozens of bots with overlapping and sometimes opaque purposes. OpenAI alone operates GPTBot (training) and ChatGPT-User (real-time retrieval) under different user-agent strings. Google has Googlebot (search indexing) and Google-Extended (AI training). Anthropic operates ClaudeBot. Meta, Apple, Cohere, Perplexity, and many others each have their own. Site owners must maintain an ever-growing list of user-agent blocks, and new crawlers appear regularly without standardised announcement mechanisms.

As of 2026, industry analysis shows that a large and growing number of websites are adding AI-specific blocks to their robots.txt files, often blocking training crawlers while permitting retrieval crawlers. This is a reasonable strategy, but it requires constant maintenance and offers no guarantees about compliance from less established operators.


## The Emerging Alternatives

The limitations of robots.txt have prompted several parallel efforts to create richer policy mechanisms for the AI era:

**ai.txt** is a proposed domain-specific language for declaring what kinds of AI interactions are permitted on a site. Unlike robots.txt, it can express rules at the level of actions (summarisation, extraction, training, citation) rather than just access. It supports natural-language instructions aimed at compliant AI agents.

**llms.txt** takes a different approach. Originally proposed by Jeremy Howard, it is a Markdown file placed at a site's root that gives AI systems a curated overview of the site's key content -- what the site is, what its most important pages are, and what it would prefer agents to focus on. It is a guidance document rather than a restriction mechanism.

**siteai.json**, proposed by the newly formed A2WF (Agent to Web Framework) community group, is a structured JSON policy file that websites can host to declare permissions, restrictions, and identification requirements for AI agents. By using JSON rather than plain text, it can express richer semantics -- distinguishing between agent types, specifying usage constraints, and potentially integrating with agent identity and capability verification systems.

These proposals are not mutually exclusive. They address different aspects of the same problem: robots.txt handles coarse access control, llms.txt provides content guidance, ai.txt specifies usage permissions, and siteai.json aims to provide a comprehensive, machine-parseable policy framework.


## How This Connects to Knowledge Representation

From a knowledge representation perspective, the evolution from robots.txt to structured policy files like siteai.json represents a familiar trajectory: the move from implicit, informally expressed knowledge to explicit, formally structured, machine-reasonble representations.

robots.txt encodes a site owner's intent in a format that is technically machine-readable but semantically impoverished. It can express "do not access" but not "you may access for purpose X but not purpose Y" or "access is permitted if the agent meets condition Z." The richer proposals -- particularly siteai.json -- begin to look like lightweight ontologies of web-site intent, making previously implicit expectations about agent behaviour explicit, structured, and available for automated reasoning.

This is precisely the problem that knowledge representation in AI has always aimed to solve: bridging the gap between what humans mean and what machines can reliably interpret and act upon.


## What This Means in Practice

For anyone working on web standards, agent interoperability, or AI governance, the practical implications are worth noting:

The robots.txt protocol will not disappear. It remains the baseline, and all major AI companies publicly commit to respecting it. But it is increasingly insufficient as the sole mechanism for web-AI negotiation.

The proliferation of competing proposals (ai.txt, llms.txt, siteai.json, well-known agent.json URIs, and others) creates a coordination challenge. Without convergence or at least interoperability, site owners will face the burden of maintaining multiple policy files, and agent developers will face the burden of parsing multiple formats.

The voluntary compliance model that sustained robots.txt for three decades is under strain. As the economic stakes of AI training and retrieval increase, purely honour-based systems may prove inadequate. Some organisations -- notably Cloudflare -- are already offering enforcement layers that technically block non-compliant crawlers rather than relying on voluntary adherence.

The question of agent identity -- how a website verifies that the entity requesting access is who it claims to be -- remains largely unresolved. robots.txt trusts user-agent strings, which are trivially spoofable. More robust identity and capability verification mechanisms will be needed as AI agents become more autonomous and more consequential in their web interactions.


## Summary

robots.txt is a thirty-year-old protocol that does one thing simply and well: it tells crawlers which URLs they may visit. For the search-engine era, that was enough. For the AI-agent era, it is a necessary but insufficient foundation. The emerging proposals -- ai.txt, llms.txt, siteai.json, and others -- represent the field's attempt to build richer, more expressive, more verifiable mechanisms for negotiating the relationship between websites and the AI systems that interact with them. Understanding robots.txt is the starting point for understanding where that negotiation is heading.


---

*Epistemic Systems Lab, Ronin Institute for Independent Scholarship*
