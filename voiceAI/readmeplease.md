# Voice Interaction Standards Framework — Document Set

**W3C AI KR Community Group — Discussion Draft**
**Author:** Paola Di Maio
**Date:** January 2026

---

## Overview

This document set contains two companion versions of the **Configurable Voice Interaction Standards Framework**, a proposal to standardize controls for voice-driven web interfaces. Both documents are formatted using [W3C ReSpec](https://respec.org/) and render as proper W3C Community Group Draft specifications when opened in a modern browser (Chrome or Firefox recommended).

The two versions serve different purposes at different stages of the standardization discussion.

---

## The Two Documents

### `voice-ai-standards-withoutnewtypes.html`
**Purpose: Initial discussion and API design review**

This version presents the six proposed API components as **design sketches only**. All novel types (interfaces, enums, callbacks) are shown as pseudocode inside forward-declaration blocks marked with:

> ⚠ TYPE NOT YET DEFINED — Proposed for future standardization

This version is intended for early-stage conversations where the focus is on:

- Whether the proposed API surface makes sense
- Whether the six components address real gaps
- How the proposals relate to existing standards (Web Speech API, Media Session, etc.)
- Whether the W3C community sees value in pursuing formal standardization

It deliberately avoids committing to specific WebIDL signatures, keeping the discussion at the level of capability and intent rather than type-level specifics.

---

### `voice-ai-standards-withnewtypes.html`
**Purpose: Formal proposal with complete type definitions**

This version includes **full WebIDL definitions** for all 11 proposed new types. Each novel type is visually marked with:

> ⬢ NEW TYPE PROPOSED FOR STANDARDIZATION

It also includes a **§ Proposed New Types** inventory section — a single table listing every new type, its kind (interface/enum/callback), where it is defined in the document, its purpose, and the nearest existing W3C standard it relates to.

This version is intended for:

- Technical review of the proposed interfaces
- Evaluating whether types should extend existing specs or form a standalone specification
- Identifying conflicts or overlaps with current W3C/WHATWG work
- Serving as the basis for a polyfill implementation

---

## How They Stack Together

```
┌─────────────────────────────────────────────────┐
│                                                 │
│   withoutnewtypes.html                          │
│   ─────────────────────                         │
│   "Here's what we think voice apps need"        │
│                                                 │
│   • 6 API components as design concepts         │
│   • Pseudocode forward declarations             │
│   • Focus: Do we agree on the problem space?    │
│   • Audience: Broad community, first review     │
│                                                 │
│              │                                   │
│              │  Once there is agreement on       │
│              │  the API design direction...      │
│              ▼                                   │
│                                                 │
│   withnewtypes.html                             │
│   ─────────────────                             │
│   "Here's exactly what we propose to add"       │
│                                                 │
│   • 11 new types in full WebIDL                 │
│   • New Types inventory table                   │
│   • Focus: Are these the right interfaces?      │
│   • Audience: Spec reviewers, implementers      │
│                                                 │
└─────────────────────────────────────────────────┘
```

The intended workflow is:

1. **Share `withoutnewtypes.html` first** — use it to open discussion with the WebDX CG, AI KR CG, and other interested parties about whether the problem space and API shape are right.

2. **Share `withnewtypes.html` second** — once there is directional agreement, use the full-types version for technical review, WebIDL scrutiny, and implementation planning.

3. **Both documents cross-reference each other** in their abstracts, so reviewers can navigate between them.

---

## Proposed New Types (Summary)

| Type | Kind | API Component |
|------|------|---------------|
| `VoicePlaybackController` | Interface | Temporal Control |
| `VoiceInteractionState` | Enum | Interaction State Machine |
| `VoiceInteractionStateMachine` | Interface | Interaction State Machine |
| `VoiceContext` | Interface | Context Management |
| `VoiceTask` | Interface | Task Queue |
| `VoiceTaskResult` | Interface | Task Queue |
| `VoiceTaskQueue` | Interface | Task Queue |
| `VoiceTaskStatus` | Enum | Task Queue |
| `VoiceTaskCallback` | Callback | Task Queue |
| `VoiceHistoryEntry` | Interface | Recovery Protocol |
| `VoiceSessionRecovery` | Interface | Recovery Protocol |

None of these types exist in any current W3C or WHATWG specification.

---

## How to View

Open either `.html` file in **Chrome or Firefox**. The ReSpec processor loads automatically from `https://www.w3.org/Tools/respec/respec-w3c` and renders the W3C-styled specification with table of contents, numbered sections, and formatted references.

ReSpec may show a brief loading bar at the top — this is normal. Once processing completes, the document is fully navigable.

---

## Context

These notes originated from a Voice AI white paper by Paola Di Maio (W3C AI KR CG) and were shared with Patric and Francois of the W3C WebDX CG via email on 29 January 2026 to explore relevance to the WebDX Community Group.

Source document: [Google Doc](https://docs.google.com/document/d/1gbEBIR3YDw1lu5mu6FbKkUBaMH282QNbgDdsf2jWokM/edit)

---

## Feedback

Discussion and feedback are welcome. The open question at the heart of this proposal is:

> Should these types be proposed as extensions to existing specifications (e.g., Web Speech API, Media Session API) or as a standalone new specification?
