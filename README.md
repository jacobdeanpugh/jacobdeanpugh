<img src="assets/banner.svg" width="100%" alt="Jacob Pugh, infrastructure and automation: a label-maker label with my name stuck on a server in a rack" />

<p align="center">
  <a href="https://www.linkedin.com/in/jacobdeanpugh/">LinkedIn</a>
  &nbsp;·&nbsp;
  <a href="mailto:jacob.pugh.riverside@gmail.com">Email</a>
</p>

I'm a CS student at California Baptist University. Most of what I build is infrastructure: clusters, CI/CD pipelines and the automation that ties a project together.

**Right now**

- **ember**, my capstone: I built the team's k3s cluster and I'm working on the ingestion side
- **Homelab**: rebuilding it so every layer, from the VMs up, is defined in code
- **Parallax**: measuring where real-time object detectors fail, with a 10B vision-language model as the reference

## Featured

<table>
<tr>
<td width="50%" valign="top">

### [UniCore](https://github.com/ghbrando/unicore)

A peer-to-peer compute marketplace. Rent out idle CPU and RAM, or spin up a Linux VM from the browser with no cloud account. Provider machines are never exposed: their containers dial out to a GCP relay over FRP, so consumers get a browser SSH shell with zero open ports.

**What I built** (top contributor)

- Persistent volumes, GCS sync and container snapshots
- Caddy wildcard-subdomain reverse proxy for VM services
- Provider dashboard backend, provider selection, emergency stop

`.NET 10` `Blazor` `Docker` `GCP` `Firestore` `FRP` `Caddy`

</td>
<td width="50%" valign="top">

### [ember](https://github.com/cbu-capstone-design-27/ember)

Graph-based context for AI coding agents. It replaces static `AGENTS.md` files with a typed knowledge graph of a project's decisions, conventions, people and tickets, kept current from GitHub, Jira and Slack and served to coding tools over MCP.

**What I built** (infrastructure)

- The team's k3s cluster: nodes set up with Ansible, workloads deployed by Flux
- Tailscale Funnel and NGINX to receive GitHub webhooks
- CI that builds service images and publishes them to GHCR
- On-cluster Postgres, the ingestion architecture and the intake listener

`k3s` `Flux` `Ansible` `Tailscale` `GitHub Actions` `Postgres` `MCP`

</td>
</tr>
</table>

## Homelab

<img src="assets/homelab.svg" width="100%" alt="Homelab pipeline: git, then GitHub Actions, OpenTofu, Ansible, k3s and Flux" />

A single Proxmox node, defined end to end in code. OpenTofu builds the VMs, Ansible configures them, k3s runs the workloads and Flux keeps the cluster in sync with git. Nothing faces the internet: the machines are reachable only over a private Tailscale tailnet, and secrets are committed encrypted with SOPS and age. The repo is private while I build it out.

## Projects

| Project | What it does |
| :-- | :-- |
| [**Graph‑fil‑A**](https://github.com/ghbrando/Graph-fil-A) | Speech in, interactive knowledge graph out. Five Cloud Run services fan out over Eventarc and Pub/Sub, Gemini extracts entities, and a Cytoscape mind map updates live. I deployed the API Gateway and built the multi-turn chat service (top contributor).<br>`GCP` `Terraform` `Gemini` `React` |
| **Parallax**<br><sub>private</sub> | Finds where real-time object detectors fail: scores stock YOLO and RT-DETR against a 10B reasoning model on street-level imagery, then clusters the disagreements into named failure modes. Runs on a DGX Spark.<br>`Python` `YOLO` `RT-DETR` `HDBSCAN` |
| [**PughCV**](https://github.com/jacobdeanpugh/PughCV) | Tailors a résumé to a job description: an LLM returns a structured résumé and a containerized LaTeX toolchain renders the PDF.<br>`Next.js` `TypeScript` `LaTeX` `Docker` |
| [**NoteHunt**](https://github.com/jacobdeanpugh/NoteHunt) | Watches note folders and keeps a Lucene full-text index in sync in real time, with file state tracked in embedded H2.<br>`Java` `Lucene` `H2` |

## Contributions

| Where | What I shipped |
| :-- | :-- |
| **CBU CAiMLL**<br><sub>private</sub> | Azure Data Factory pipelines and Python Azure Functions that crawl, download and clean source data, with unit tests. Salesforce work in Apex and Lightning Web Components. |
| **Dalcion**<br><sub>private</sub> | RAG pipeline plus document and code endpoints for an AI assistant that helps architects build within their company's codes, and a fix to the Revit add-on. |
| [**Save-Water-CBU**](https://github.com/Save-Water-CBU) | Information security coursework: an [AES CLI](https://github.com/Save-Water-CBU/AES-Encryption) with PBKDF2 key derivation (Java 21) and a [simulated USB installer attack](https://github.com/Save-Water-CBU/USB-Crack-Attack) for classroom use (Python). |
| **ClassMates**<br><sub>private</sub> | A study-group app: groups, invites, friends, flashcards and account pages. |
| **Restaurant app template**<br><sub>private</sub> | Flutter: shopping cart, maps and theming for a reusable restaurant app. |

## Stack

<img src="assets/stack.svg" width="100%" alt="Stack, as label-maker labels on a rack panel. Infra: Proxmox, Rocky Linux, Debian, Arch, OpenTofu, Terraform, Ansible, k3s, Kubernetes, Flux, Docker, Tailscale, NGINX, Caddy, GitHub Actions. Cloud and data: GCP, Azure, Firebase, Postgres, Neo4j, Salesforce. Code: Python, C# and .NET, TypeScript, Java, Bash, Next.js, React, Flutter." />
