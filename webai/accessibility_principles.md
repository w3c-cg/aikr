# W3C Code Quality Principles for AI-Generated Code

## An Explainer for Developers and Evaluators

Authors: Paola Di Maio (W3C AIKR CG Chair) 
ESL Ronin Institute / W3C AI Knowledge Representation CG
Reference: [w3c/webai#23](https://github.com/w3c/webai/issues/23)

---

## Why This Matters

AI code assistants now write a significant proportion of production code. Studies estimate that AI assistants produce close to half of all new developer code. Yet research consistently shows that AI-generated code introduces quality and security risks that are not caught by functional testing alone.

The W3C community has identified a gap: there is no systematic way to ensure that AI-generated web code respects the foundational principles that make the web work for everyone. Issue #23 in the W3C Web & AI repository calls for tools and prompts that guide LLMs toward generating code that follows W3C guidelines for accessibility, internationalization, privacy, and security.

This document explains the four principles and why each one matters for AI-generated code specifically.

---

## The Four Principles

### 1. Accessibility (A11Y)

**What it means:** Web content must be usable by people with disabilities, including those who use screen readers, keyboard-only navigation, voice control, and other assistive technologies.

**The standard:** The Web Content Accessibility Guidelines (WCAG) 2.2, maintained by the W3C Web Accessibility Initiative (WAI), define testable success criteria at three conformance levels (A, AA, AAA). Level AA is the widely accepted baseline for compliance.

**Why AI-generated code fails here:**

LLMs are trained on vast quantities of existing web code, and the web is overwhelmingly inaccessible. The WebAIM Million report consistently finds that over 95% of home pages have detectable WCAG failures. When an LLM learns from this corpus, it reproduces the same patterns: images without alt text, div-soup layouts instead of semantic HTML, click handlers without keyboard equivalents, forms without associated labels, and missing language declarations.

The problem is structural. An LLM optimising for "code that looks like the training data" will produce inaccessible code, because most of the training data is inaccessible. The model has no incentive to add an alt attribute unless the prompt explicitly demands it, because most of the code it learned from does not have one.

**What good code looks like:**

- Semantic HTML landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`, `<article>`, `<section>` instead of generic `<div>` elements
- Every `<img>` has a descriptive `alt` attribute (or `alt=""` for decorative images)
- Every form input has an associated `<label>` element or `aria-label`
- Interactive elements are keyboard-accessible (using `<button>`, `<a>`, or adding `tabindex="0"` with keyboard event handlers)
- The `<html>` element declares `lang="en"` (or appropriate language code)
- Page has a descriptive `<title>`
- No positive `tabindex` values (which disrupt natural tab order)
- Media elements with `autoplay` also have `controls` and `muted`

**Key WCAG success criteria tested:**

| Criterion | Requirement |
|-----------|-------------|
| 1.1.1 Non-text Content | Alt text on images |
| 1.3.1 Info and Relationships | Semantic HTML structure |
| 2.1.1 Keyboard | All functionality keyboard-accessible |
| 2.4.2 Page Titled | Descriptive page title |
| 2.4.4 Link Purpose | Links have meaningful text |
| 3.1.1 Language of Page | Lang attribute on html element |
| 4.1.2 Name, Role, Value | ARIA labels on interactive elements |

---

### 2. Internationalization (I18N)

**What it means:** Web content must be designed so that it can be adapted for users from any culture, region, or language -- without requiring engineering changes to the codebase.

**The standard:** The W3C Internationalization Activity maintains best practices for specification developers and web authors. The core principle is that internationalisation is a design requirement, not a translation afterthought.

**Why AI-generated code fails here:**

LLMs predominantly generate code with English-only assumptions baked in. They hardcode UI strings directly into HTML, use fixed pixel widths that break when text is translated (German runs approximately 30% longer than English, while Chinese can be more compact), format dates manually instead of using locale-aware APIs, omit charset declarations, and never consider right-to-left script support.

This is not merely an inconvenience. A web application that cannot declare its language cannot be correctly pronounced by a screen reader. A form that cannot accept non-ASCII characters excludes billions of users. A layout that breaks with translated text is not production-ready.

**What good code looks like:**

- `<meta charset="UTF-8">` as the first element in `<head>`
- `<html lang="en" dir="ltr">` (with appropriate BCP 47 language tag and direction)
- `dir="auto"` on user-generated content containers
- UI text externalised using `data-i18n` attributes or resource bundles rather than hardcoded strings
- `Intl.DateTimeFormat()` and `Intl.NumberFormat()` for locale-aware formatting
- Relative units (`rem`, `em`, `%`, `ch`) instead of fixed pixel widths for text containers
- CSS logical properties (`margin-inline-start` instead of `margin-left`) for RTL support

**Key I18N requirements tested:**

| Requirement | Why It Matters |
|-------------|----------------|
| UTF-8 charset | Correct rendering of all world scripts |
| Language declaration | Screen reader pronunciation, search indexing, hyphenation |
| Text direction | Arabic, Hebrew, Urdu, and other RTL scripts |
| Externalised strings | Enables translation without code changes |
| Flexible layouts | Accommodates text expansion in translation |
| Intl API usage | Locale-correct dates, numbers, currencies |

---

### 3. Privacy

**What it means:** Web applications must respect user privacy by minimising data collection, requiring informed consent for tracking, transmitting data securely, and avoiding covert identification techniques.

**The standard:** The W3C Privacy Interest Group (PING) maintains privacy principles for web standards. The W3C Technical Architecture Group (TAG) has published findings on unsanctioned tracking. These align with regulatory frameworks including GDPR and the ePrivacy Directive.

**Why AI-generated code fails here:**

LLMs reproduce common patterns from the training data, and common patterns include dropping Google Analytics or Facebook tracking pixels into pages without any consent mechanism, storing personally identifiable information in localStorage (which is accessible to any script on the page), submitting forms over HTTP instead of HTTPS, and accessing geolocation or camera APIs without explaining why.

More subtly, AI-generated code can include browser fingerprinting techniques -- reading canvas data, enumerating plugins, collecting screen dimensions -- that enable user tracking without cookies. The LLM does not understand that these are privacy-invasive; it simply learned them as "things web code does."

**What good code looks like:**

- No third-party tracking scripts loaded without an explicit consent mechanism
- No PII (names, emails, phone numbers) stored in localStorage or sessionStorage
- All form actions use HTTPS
- Geolocation, camera, and microphone APIs accessed only after user consent with clear purpose explanation
- No canvas fingerprinting or navigator property enumeration
- Password fields with appropriate `autocomplete` attributes
- Data minimisation: collect only what is needed for the stated purpose

**Key privacy requirements tested:**

| Requirement | Risk If Violated |
|-------------|------------------|
| No unconsented trackers | GDPR/ePrivacy violation, user surveillance |
| No PII in client storage | Data exposure via XSS |
| HTTPS form submission | Credential interception |
| No fingerprinting | Covert tracking without user knowledge |
| Geolocation consent | Location surveillance |
| Secure credential handling | Credential theft |

---

### 4. Security

**What it means:** Web code must not introduce vulnerabilities that allow attackers to inject malicious scripts, steal user data, or compromise the integrity of the application.

**The standard:** The OWASP Top 10 provides the industry-standard taxonomy of web application security risks. The W3C contributes directly through specifications including Content Security Policy (CSP), Subresource Integrity (SRI), and the Mixed Content specification.

**Why AI-generated code fails here:**

Security is arguably where AI-generated code is most dangerous, because the vulnerabilities are invisible to non-expert review. An LLM will cheerfully generate code that uses `eval()` to parse user input, sets `innerHTML` from unsanitised data, loads external scripts without integrity checks, includes inline event handlers that prevent CSP deployment, opens links with `target="_blank"` without `rel="noopener"`, and embeds API keys directly in client-side code.

Each of these is a well-known, well-documented vulnerability. Yet LLMs reproduce them routinely because the training data is full of tutorials, Stack Overflow answers, and open-source projects that use these patterns. The patterns work functionally, so the LLM has no reason to avoid them unless specifically instructed.

**What good code looks like:**

- No `eval()`, `new Function()`, or `document.write()`
- `textContent` instead of `innerHTML` for text insertion; `DOMPurify.sanitize()` when HTML is necessary
- External scripts with `integrity="sha384-..."` and `crossorigin="anonymous"` (Subresource Integrity)
- No inline event handlers (`onclick`, `onload`, etc.) -- use `addEventListener()` instead
- Links with `target="_blank"` include `rel="noopener noreferrer"`
- No hardcoded secrets, API keys, or credentials in client-side code
- No mixed HTTP/HTTPS content
- All user input sanitised before DOM insertion

**Key security requirements tested:**

| Requirement | Attack Vector Prevented |
|-------------|------------------------|
| No eval/innerHTML/document.write | Cross-site scripting (XSS) |
| Subresource Integrity | CDN compromise, supply chain attacks |
| No inline event handlers | Enables Content Security Policy |
| No hardcoded secrets | Credential theft via source inspection |
| No mixed content | Man-in-the-middle attacks |
| noopener on _blank links | Reverse tabnabbing |

---

## The Tools

Two companion tools have been developed to test code against these principles:

### Code Safety Checker

Live app: [https://starborn.github.io/codesafetycheckr2026/](https://starborn.github.io/codesafetycheckr2026/)

Checks Python, JavaScript, and Shell code for security vulnerabilities (40+ rules). Runs entirely in the browser. Covers dangerous function calls, hardcoded secrets, injection vulnerabilities, network exfiltration patterns, and file system risks.

### W3C Code Quality Checker

Colab notebook: [https://colab.research.google.com/drive/1bFsY-gZx03qxtIB2TlY5lwsSNkrWMUV9](https://colab.research.google.com/drive/1bFsY-gZx03qxtIB2TlY5lwsSNkrWMUV9?usp=sharing)

Checks HTML/CSS/JS against all four W3C principles (30+ rules). Provides per-principle scoring, detailed findings with WCAG references, and reusable prompt templates for guiding LLMs toward compliant output.

Both tools use static analysis only -- no code is executed. Both are open source under CC-BY-4.0.

---

## How to Use This

**If you are evaluating AI-generated code:** Paste it into either tool and check the scores. The per-principle breakdown tells you exactly where the code falls short and what to fix.

**If you are prompting an LLM to write code:** Use the prompt templates in the Colab notebook (Part 5). These bake in all four principles as explicit requirements, so the LLM cannot silently omit them.

**If you are developing AI code assistants:** The rule sets in both tools can serve as evaluation benchmarks. Run your assistant's output through them and track compliance over time.

**If you are contributing to W3C standards work:** These tools provide concrete evidence of where AI-generated code systematically fails to meet existing web standards, supporting the case for explicit guidance to AI tool developers.

---

## References

- W3C Web Content Accessibility Guidelines (WCAG) 2.2: https://www.w3.org/TR/WCAG22/
- W3C Internationalization Best Practices: https://w3c.github.io/bp-i18n-specdev/
- W3C Privacy Principles: https://www.w3.org/TR/privacy-principles/
- W3C Content Security Policy Level 3: https://www.w3.org/TR/CSP3/
- W3C Subresource Integrity: https://www.w3.org/TR/SRI/
- W3C Accessibility of Machine Learning and Generative AI: https://w3c.github.io/ai-accessibility/
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- w3c/webai Issue #23: https://github.com/w3c/webai/issues/23

---

## Citation

Di Maio, P. & Claude (2026). W3C Code Quality Principles for AI-Generated Code: An Explainer. W3C AIKR CG / Epistemic Systems Lab, Ronin Institute.

License: CC-BY-4.0
