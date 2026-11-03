# The Discoverability Gap in the Decentralized and AI-Mediated Web

**A Technical Primer on DID Search, Web Indexing and Information Retrieval**

**Technical Note | November 2026**

**Status:** Independent research discussion draft. Not a W3C Recommendation or an endorsed W3C Community Group report.

## Central Research Question

**Can an open web remain genuinely open if resources are technically accessible but cannot be reliably discovered by independent search mechanisms?**

### Supporting Research Questions

1. How does the discoverability of DID-associated resources compare with resources published through conventional HTTP(S) infrastructure?
2. What technical and architectural limitations prevent universal keyword search across decentralized networks?
3. To what extent are conventional search engines becoming less effective at retrieving relevant, authoritative and independently published information?
4. How do AI-generated search summaries affect source visibility, provenance and access to original publications?
5. What open standards are needed to support interoperable discovery, indexing and retrieval across centralized and decentralized architectures?
6. How can knowledge representation and semantic metadata improve resource discovery for human users and autonomous AI agents?

> The open web has historically enabled the possibility of access, but it has never guaranteed discoverability. As information becomes increasingly distributed across decentralized architectures and mediated by AI search interfaces, this distinction becomes more consequential.

## Executive Summary

Decentralized Identifiers (DIDs) offer important advantages for digital identity, cryptographic verification and reduced dependence on centralized identity providers. However, they do not, by themselves, provide a mechanism for discovering information through ordinary keyword searches.

A resource may be accessible through a DID, a distributed storage network or a content identifier without being discoverable by users who do not already know its address.

**The central conclusion is that publishers who want their content to remain discoverable through general-purpose search engines should continue publishing it at stable HTTPS URLs on conventional domain-based servers.**

Decentralized identifiers and storage technologies can complement this infrastructure but should not currently be regarded as substitutes for it.

At the same time, concerns about the usefulness of contemporary Google Search raise a separate issue. Research documents problems involving search-engine optimization spam, commercially motivated content pollution and changes in how users encounter sources through AI-generated summaries.

These two problems—limited discovery in decentralized systems and challenges to effective information retrieval on the conventional web—suggest a common need for open, interoperable standards for content discovery, indexing, provenance and search-quality assessment.

## 1. Understanding the Problem

**The ability to access a resource is not the same as the ability to find it.**

Four operations must be distinguished:

| Operation | Purpose |
|---|---|
| Identification | Assign a unique identifier to a resource or subject |
| Resolution | Determine the information or services associated with a known identifier |
| Discovery | Find previously unknown resources relevant to a topic |
| Retrieval | Obtain the identified information |

Traditional web search combines these operations through URLs, hyperlinks, web crawlers, indexing systems and search interfaces.

DIDs primarily support identification and resolution. They do not automatically provide topic-based discovery or full-text indexing.

This distinction is important when evaluating decentralized web architectures and their implications for independent scholarship, information access and agentic AI.

## 2. How Search Works on the Conventional Web

The traditional web relies on several complementary technologies:

- DNS associates domain names with network services.
- HTTP and HTTPS enable clients to request and retrieve resources.
- URLs provide addresses for resources.
- HTML hyperlinks create discoverable connections between pages.
- Search engines crawl publicly accessible resources and build searchable indexes.

A simplified search process is:

1. An author publishes a resource at an HTTP(S) URL.
2. A crawler discovers the URL through hyperlinks, sitemaps or other signals.
3. The crawler retrieves and parses the content.
4. The search provider incorporates eligible information into an index.
5. A user enters a keyword or natural-language query.
6. The search provider ranks and returns matching resources.

Google distinguishes crawling, indexing and serving results as separate stages.

A publisher does not need to register every document individually with every search provider. Nevertheless, publication does not guarantee indexing or visibility. Search engines determine which pages they crawl, index and rank.

Reference: [Google Search Central — How Search Works](https://developers.google.com/search/docs/fundamentals/how-search-works).

## 3. How Search Works With Decentralized Identifiers

The W3C DID Core specification defines Decentralized Identifiers as identifiers that can be resolved, according to their DID methods, into DID documents.

An example DID is:

```text
did:example:123456789abcdefghi
```

A DID identifies a subject, which may be a person, organization, concept or information resource.

A DID resolver may obtain a DID document containing verification methods, verification relationships and optional service endpoints.

A simplified resolution sequence is:

1. A client supplies a known DID.
2. The appropriate DID-method resolution procedure is invoked.
3. Resolution returns a DID document or an error.
4. The client examines the available verification methods or service information.
5. Where applicable, the client contacts an associated service.

Crucially, **DID resolution is not equivalent to general-purpose information search**.

A DID document does not necessarily contain:

- A searchable publication title
- Descriptive keywords
- Full-text content
- An IPFS content identifier
- A publicly accessible publication URL

Service endpoints are optional, and a DID document is not necessarily a content manifest.

A DID and an IPFS CID are different types of identifiers. A DID identifies a subject according to a DID method, whereas a CID identifies content through a content-addressing scheme.

The W3C specification does not establish a universal keyword-search service across all DIDs.

### The fundamental discovery problem

Suppose someone wants to find:

*Research papers discussing interoperability between autonomous AI agents.*

They do not know the identifiers of relevant authors or publications.

A DID resolver cannot, by itself, answer that query.

A separate discovery infrastructure is needed to collect resource descriptions, retrieve or receive content, construct indexes and return relevant matches.

Reference: [W3C Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/).

## 4. Keyword Search in Decentralized Systems

### 4.1 Distributed content discovery

IPFS uses content identifiers and routing mechanisms to locate providers of requested data.

Its distributed hash table helps locate peers offering data associated with a known CID.

However, this is not equivalent to a general-purpose keyword index.

Knowing a CID and finding the peers that hold it is fundamentally different from asking which previously unknown resources discuss a particular subject.

A keyword search engine must separately collect, retrieve or receive, and index relevant information.

References:

- [IPFS — How IPFS Works](https://docs.ipfs.tech/concepts/how-ipfs-works/)
- [IPFS — Distributed Hash Tables](https://docs.ipfs.tech/concepts/dht/)

### 4.2 Specialized decentralized search engines

Specialized indexers, registries and peer-to-peer search frameworks attempt to make distributed resources searchable.

Their effectiveness depends on factors such as:

- Network and collection coverage
- Participation by resource providers
- Availability of usable metadata
- Discovery of newly published resources
- Persistence of stored content
- Compatibility between indexing systems

Successful decentralized keyword search therefore depends on the coverage and capabilities of the particular indexer.

### 4.3 Blockchain event indexing

Some blockchain ecosystems expose events or transactions that indexing services can collect.

An application could publish an event associating an identifier with descriptive metadata.

An indexer could then construct a searchable database from those announcements.

However, indexing events does not automatically index the full text of external documents. That requires additional retrieval or processing.

### 4.4 Publisher registration and push-based discovery

An alternative to conventional crawling is for publishers to announce resources to one or more indexing services.

Such mechanisms could support decentralized or federated discovery, provided that independent indexers can understand the announcements.

Potential requirements include:

- Interoperable publication announcements
- Common metadata vocabularies
- Update and withdrawal mechanisms
- Provenance information
- Spam prevention
- Privacy protection

These are possible architectural components, not an established universal DID-search standard.

## 5. Bridging Decentralized Content and Conventional Search

One practical approach is to expose decentralized resources through HTTP gateways.

For example, content stored in IPFS may become accessible through an HTTPS URL.

A conventional search engine can potentially crawl that URL if the resource is accessible, linked and eligible for indexing.

However, an HTTP gateway does not guarantee discoverability.

Multiple gateways may also expose the same resource at different URLs, creating duplicate representations.

Search engines already use canonicalization mechanisms to identify preferred URLs among duplicate or similar pages.

For publishers, a dependable arrangement is to maintain a canonical HTTPS publication page and reference any corresponding decentralized identifiers or storage locations from that page.

This arrangement supports conventional keyword discovery while preserving opportunities for decentralized verification or distribution.

Reference: [Google Search Central — Canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization).

## 6. Why Google Search Appears to Be Becoming Less Useful

Complaints about deteriorating search quality require careful evaluation.

It has not been established that Google has universally lost its ability to retrieve useful information. Search usefulness varies by query type, language, subject, ranking criteria and user expectations.

Nevertheless, several documented developments help explain why some users find contemporary search less effective.

### 6.1 Search-engine optimization and commercially motivated content

Bevendorff and colleagues investigated SEO spam in search engines in a longitudinal study published at ECIR 2024.

The research examined product-review searches across Google, Bing and DuckDuckGo.

It identified substantial problems involving affiliate-oriented content and search-engine optimization.

These findings support concern that commercially optimized pages can displace informative resources in certain search categories.

They do not establish equivalent deterioration across every category of web search.

Reference: [Bevendorff et al. — Is Google Getting Worse?](https://gwern.net/doc/technology/google/2024-bevendorff.pdf).

### 6.2 AI-generated and scaled content

Generative AI has reduced the cost of producing large quantities of text.

This enables legitimate publishing but also creates opportunities to mass-produce low-value pages designed primarily to attract search traffic.

Google's spam policies expressly recognize scaled content abuse, including automated production that provides little original value.

Challenges for search systems include distinguishing:

- Original research from derivative summaries
- Expert analysis from plausible but unsupported text
- Independently produced information from replicated content
- Useful aggregation from material optimized primarily for rankings

Not all AI-generated content is spam. The relevant concern is the purpose and value of publication.

Reference: [Google Search Central — Spam Policies](https://developers.google.com/search/docs/essentials/spam-policies).

### 6.3 The transition from finding sources to generating answers

Traditional search generally presents links to sources.

AI-enhanced search increasingly supplies synthesized answers directly within search interfaces.

This may help users answer factual questions quickly, but it changes how they encounter and evaluate original publications.

A Pew Research Center study based on March 2025 browsing activity from 900 US adults reported:

| Search-result condition | Visits resulting in clicks on conventional search-result links |
|---|---:|
| Without an AI summary | 15% |
| With an AI summary | 8% |

Only 1% of visits involving an AI summary resulted in a click on a link inside that summary.

These findings are observational. They do not demonstrate that AI summaries caused the entire difference, nor do they establish lower answer accuracy.

They do indicate a change in the relationship between search providers, publishers and readers.

Users may obtain answers without visiting original sources, potentially reducing opportunities to examine context, authorship, supporting evidence and competing interpretations.

Reference: [Pew Research Center — Google Users Are Less Likely to Click on Links When an AI Summary Appears](https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/).

### 6.4 Discoverability of independent and specialist publications

Independent researchers and specialist publishers may struggle for visibility when competing with large platforms and commercial content providers.

A resource's relevance and its visibility in search rankings are not equivalent.

For independent scholarship, this is important because valuable work may reside on individual domains, small institutional websites or specialized repositories.

It would be premature to conclude that Google systematically suppresses independent scholarship without controlled evidence.

Nevertheless, the concern warrants reproducible measurement.

## 7. What Publishers Should Do

For authors, researchers and organizations whose priority is public discoverability, several practices remain advisable.

| Publishing practice | Discovery benefit |
|---|---|
| Publish at a stable HTTPS URL | Makes resources accessible to conventional crawlers |
| Maintain a publisher-controlled domain | Provides a recognizable and persistent publication location |
| Supply descriptive titles and metadata | Helps indexers interpret resources |
| Publish accessible HTML and linked documents | Enables retrieval and parsing |
| Maintain XML sitemaps | Helps crawlers discover URLs |
| Use meaningful internal and external hyperlinks | Supports navigation and discovery |
| Maintain canonical URLs and redirects | Reduces ambiguity between copies |
| Include persistent identifiers where appropriate | Supports reference and verification |
| Mirror content in decentralized storage if useful | Adds preservation or distribution options |
| Monitor crawl eligibility and broken links | Helps identify visibility failures |

**Publishers who want their work to be found should continue publishing through conventional HTTP(S) domain infrastructure.**

A DID may provide an additional identity or verification layer. An IPFS CID may support content integrity through content addressing.

Neither eliminates the practical value of conventional web publication.

## 8. Implications for Web Standards

The limitations of decentralized discovery and contemporary commercial search suggest several areas for standardization and research.

### 8.1 Discovery interoperability

Develop mechanisms enabling independent indexers to discover resources across different hosting architectures.

### 8.2 Machine-readable descriptive metadata

Encourage consistent descriptions of subjects, authorship, content types, dates, versions, access rights and relationships.

### 8.3 Provenance and authenticity

Support verifiable claims about publishers and resources.

Cryptographic verification should not be confused with factual accuracy: proving control of an identifier does not establish that every associated assertion is true.

### 8.4 Open indexing interfaces

Explore interfaces through which independent indexing services can discover or query public resource descriptions.

### 8.5 Search transparency

Develop reproducible methods for measuring relevance, indexing coverage, source diversity, commercial influence and provenance visibility.

### 8.6 Preservation of the open web

Avoid architectures that make the discovery of public information dependent on a single commercial search service or proprietary AI interface.

These topics are relevant to W3C work on identifiers, linked data, knowledge representation and interoperability.

They are also increasingly important for AI agents that must discover, retrieve and evaluate resources autonomously.

The W3C Web of Things Discovery Recommendation provides a relevant domain-specific example of searchable directories and structured resource metadata.

Reference: [W3C Web of Things Discovery](https://www.w3.org/TR/wot-discovery/).

## 9. Proposed Empirical Research Agenda

### Working research title

**The Discoverability Gap in the Decentralized and AI-Mediated Web**

A follow-up empirical study could investigate discoverability across:

1. Conventional HTTP(S) publications
2. HTTP(S) publications linked to DID-identified resources
3. Decentralized-only publication systems
4. Conventional search engines
5. Specialized decentralized search services
6. AI-mediated search interfaces

### Proposed Discoverability and Retrievability Framework

| Dimension | Possible measurement |
|---|---|
| Keyword findability | Percentage of predefined topical queries retrieving a resource within the top-ranked results |
| Indexing coverage | Percentage of eligible resources represented in a search index |
| Retrievability | Successful retrieval rate when an exact identifier is supplied |
| Discovery latency | Time between publication and first successful topical discovery |
| Provenance visibility | Availability of checkable publisher and source information |
| Source diversity | Distribution of independent publishers and domains |
| Ranking independence | Variation in resource visibility across search providers |
| Persistence | Continued availability and retrieval success over time |
| Semantic discoverability | Ability to retrieve relevant information despite vocabulary differences |
| AI-mediated source visibility | Frequency with which original sources are cited or made accessible in generated answers |

The study should distinguish known-identifier retrieval from unknown-identifier discovery.

A reproducible protocol should define query samples, relevance criteria, indexing conditions, observation dates and independent assessments.

The objective would be to measure discoverability without assuming that absence from one search engine implies universal invisibility.

## 10. Conclusion

Decentralized Identifiers support identification and resolution, including mechanisms for cryptographic verification and discovery of associated services.

However, **DIDs do not inherently provide a universal mechanism for finding unknown resources through natural-language or keyword searches**.

DID resolution should not be confused with information retrieval.

A decentralized resource can exist, remain accessible and be cryptographically verifiable while being practically invisible to users who do not know its identifier.

Until broadly interoperable decentralized discovery and indexing mechanisms are established, publishers who want their content to be found should continue publishing through HTTP(S) on conventional domain-based web servers.

Decentralized technologies should be treated as complementary layers for identity, verification, storage or distribution—not as replacements for the established discoverability infrastructure of the conventional web.

At the same time, maintaining conventional publication infrastructure does not guarantee effective discovery.

SEO spam, scaled low-value content and AI-mediated search interfaces raise legitimate questions about search quality, source visibility and the independence of information access.

These concerns require empirical investigation rather than assumptions of universal deterioration.

**The long-term objective should be to preserve the web as an open, independently searchable and verifiable information space.**

Achieving that objective requires interoperable discovery mechanisms, transparent indexing practices, meaningful provenance information, semantic descriptions and continued support for publisher-controlled web addresses.

## References

1. W3C. (2022). [Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/). W3C Recommendation, 19 July 2022.
2. IPFS Documentation. [How IPFS Works](https://docs.ipfs.tech/concepts/how-ipfs-works/).
3. IPFS Documentation. [Distributed Hash Tables](https://docs.ipfs.tech/concepts/dht/).
4. Google Search Central. [How Google Search Works](https://developers.google.com/search/docs/fundamentals/how-search-works).
5. Google Search Central. [Canonicalization](https://developers.google.com/search/docs/crawling-indexing/canonicalization).
6. Google Search Central. [Spam Policies for Google Web Search](https://developers.google.com/search/docs/essentials/spam-policies).
7. Bevendorff, J., Wiegmann, M., Potthast, M., and Stein, B. (2024). [Is Google Getting Worse? A Longitudinal Investigation of SEO Spam in Search Engines](https://gwern.net/doc/technology/google/2024-bevendorff.pdf). Advances in Information Retrieval, ECIR 2024.
8. Chapekis, A., and Lieb, A. (2025). [Google Users Are Less Likely to Click on Links When an AI Summary Appears in the Results](https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/). Pew Research Center, 22 July 2025.
9. W3C. (2023). [Web of Things (WoT) Discovery](https://www.w3.org/TR/wot-discovery/). W3C Recommendation, 5 December 2023.

---

*Independent research discussion draft, November 2026. The analysis distinguishes established technical specifications and empirical findings from proposed standards requirements and future research questions.*
