<div align="center">

<img src="assets/banner.svg" width="100%" alt="Jacob Pugh: Infrastructure · Automation · Distributed Systems" />

<br />

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=18&duration=2800&pause=1200&color=22D3EE&center=true&vCenter=true&width=620&height=40&lines=Infrastructure+as+code%2C+end+to+end;Proxmox+%E2%86%92+OpenTofu+%E2%86%92+Ansible+%E2%86%92+k3s+%E2%86%92+Flux;Peer-to-peer+compute+%40+UniCore;Knowledge+graphs+for+AI+agents+%40+ember;If+it+isn%27t+in+git%2C+it+doesn%27t+exist" />
  <img alt="Infrastructure as code, end to end" src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=500&size=18&duration=2800&pause=1200&color=0E7490&center=true&vCenter=true&width=620&height=40&lines=Infrastructure+as+code%2C+end+to+end;Proxmox+%E2%86%92+OpenTofu+%E2%86%92+Ansible+%E2%86%92+k3s+%E2%86%92+Flux;Peer-to-peer+compute+%40+UniCore;Knowledge+graphs+for+AI+agents+%40+ember;If+it+isn%27t+in+git%2C+it+doesn%27t+exist" />
</picture>

<br />

<a href="https://www.linkedin.com/in/jacobdeanpugh/"><img src="https://img.shields.io/badge/LinkedIn-13203A?style=for-the-badge&logo=linkedin&logoColor=22D3EE" alt="LinkedIn" /></a>
<a href="mailto:jacob.pugh.riverside@gmail.com"><img src="https://img.shields.io/badge/Email-13203A?style=for-the-badge&logo=gmail&logoColor=22D3EE" alt="Email" /></a>

</div>

<br />

## `$ whoami`

```yaml
apiVersion: v1
kind: Engineer
metadata:
  name: jacob-pugh
  labels:
    school: california-baptist-university
    focus: infrastructure-and-automation
spec:
  currently:
    - ember        # capstone: the k3s cluster, GitOps and ingestion behind an MCP knowledge graph
    - homelab      # Proxmox → OpenTofu → Ansible → k3s → Flux, all of it in git
    - parallax     # where real-time object detectors fail, measured against a 10B VLA
  shipped:
    - unicore      # peer-to-peer compute marketplace, top contributor
  experience:
    - cbu-caimll   # Azure data pipelines, Salesforce (Apex + LWC)
  os: [arch, debian, rocky]   # arch to build, debian + rocky to run
  principles:
    - if it isn't in git, it doesn't exist
    - outbound-only networking, least privilege, encrypted secrets
    - automate it the second time
status:
  phase: Running
```

## `~/featured`

<table>
<tr>
<td width="50%" valign="top">

### [UniCore](https://github.com/ghbrando/unicore)

**Peer-to-peer compute marketplace.** Rent out idle CPU and RAM, or spin up a Linux VM from the browser with no cloud account. Provider machines are never exposed: their containers dial *out* to a GCP relay over FRP, so consumers get a browser SSH shell with zero open ports.

**What I built** · top contributor
- Persistent volumes, GCS sync and container snapshots
- Caddy wildcard-subdomain reverse proxy for VM services
- Provider dashboard backend, provider selection, emergency stop

<img src="https://img.shields.io/badge/.NET_10-13203A?style=flat-square&logo=dotnet&logoColor=22D3EE" alt=".NET 10" />
<img src="https://img.shields.io/badge/Blazor-13203A?style=flat-square&logo=blazor&logoColor=22D3EE" alt="Blazor" />
<img src="https://img.shields.io/badge/Docker-13203A?style=flat-square&logo=docker&logoColor=22D3EE" alt="Docker" />
<img src="https://img.shields.io/badge/Google_Cloud-13203A?style=flat-square&logo=googlecloud&logoColor=22D3EE" alt="Google Cloud" />
<img src="https://img.shields.io/badge/Firestore-13203A?style=flat-square&logo=firebase&logoColor=22D3EE" alt="Firestore" />
<img src="https://img.shields.io/badge/Caddy-13203A?style=flat-square&logo=caddy&logoColor=22D3EE" alt="Caddy" />

</td>
<td width="50%" valign="top">

### [ember](https://github.com/cbu-capstone-design-27/ember)

**Graph-based context for AI coding agents.** Replaces static `AGENTS.md` files with a typed knowledge graph of a project's decisions, conventions, people and tickets, kept current from GitHub, Jira and Slack and served to any coding tool over MCP.

**What I built** · infrastructure
- The team's k3s cluster: nodes set up with Ansible, workloads deployed by Flux
- Tailscale Funnel and NGINX to receive GitHub webhooks
- CI that builds service images and publishes them to GHCR
- On-cluster Postgres, the ingestion architecture and the intake listener

<img src="https://img.shields.io/badge/k3s-13203A?style=flat-square&logo=k3s&logoColor=22D3EE" alt="k3s" />
<img src="https://img.shields.io/badge/Flux-13203A?style=flat-square&logo=flux&logoColor=22D3EE" alt="Flux" />
<img src="https://img.shields.io/badge/Ansible-13203A?style=flat-square&logo=ansible&logoColor=22D3EE" alt="Ansible" />
<img src="https://img.shields.io/badge/Tailscale-13203A?style=flat-square&logo=tailscale&logoColor=22D3EE" alt="Tailscale" />
<img src="https://img.shields.io/badge/GitHub_Actions-13203A?style=flat-square&logo=githubactions&logoColor=22D3EE" alt="GitHub Actions" />
<img src="https://img.shields.io/badge/PostgreSQL-13203A?style=flat-square&logo=postgresql&logoColor=22D3EE" alt="PostgreSQL" />
<img src="https://img.shields.io/badge/MCP-13203A?style=flat-square&logo=modelcontextprotocol&logoColor=22D3EE" alt="MCP" />

</td>
</tr>
</table>

## `~/homelab`

<img src="assets/pipeline.svg" width="100%" alt="Homelab pipeline: Git, GitHub Actions, OpenTofu, Ansible, k3s, Flux" />

A single-node Proxmox lab, defined end to end in code. OpenTofu builds the VMs, Ansible configures them, k3s runs the workloads and Flux keeps the cluster in sync with git. Nothing faces the internet: every machine is reachable only over a private Tailscale tailnet, and every secret is committed encrypted with SOPS + age. <sub>*Private repo, in progress.*</sub>

## `~/projects`

| Project | What it does | Built with |
| :-- | :-- | :-- |
| [**Graph-fil-A**](https://github.com/ghbrando/Graph-fil-A) | Speech in, interactive knowledge graph out. Five Cloud Run services fan out over Eventarc and Pub/Sub, Gemini extracts entities, and a Cytoscape mind map updates live. I deployed the API Gateway and built the multi-turn chat service. *Top contributor.* | GCP · Terraform · Gemini · React |
| **Parallax** 🔒 | Finds where real-time object detectors fail: scores stock YOLO and RT-DETR against a 10B reasoning model on street-level imagery, then clusters the disagreements into named failure modes. Runs on a DGX Spark. | Python · YOLO · RT-DETR · HDBSCAN |
| [**PughCV**](https://github.com/jacobdeanpugh/PughCV) | Tailors a résumé to a job description: an LLM returns a structured résumé and a containerized LaTeX toolchain renders the PDF. | Next.js · TypeScript · LaTeX · Docker |
| [**NoteHunt**](https://github.com/jacobdeanpugh/NoteHunt) | Watches note folders and keeps a Lucene full-text index in sync in real time, with file state tracked in embedded H2. | Java · Lucene · H2 |

## `~/contributions`

| Where | What I shipped |
| :-- | :-- |
| **CBU CAiMLL** 🔒 | Azure Data Factory pipelines and Python Azure Functions that crawl, download and clean source data, with unit tests. Salesforce work in Apex and Lightning Web Components. |
| **Dalcion** 🔒 | RAG pipeline plus document and code endpoints for an AI assistant that helps architects build within their company's codes; a fix to the Revit add-on. |
| [**Save-Water-CBU**](https://github.com/Save-Water-CBU) | Information security coursework: an [AES CLI](https://github.com/Save-Water-CBU/AES-Encryption) with PBKDF2 key derivation (Java 21) and a [simulated USB installer attack](https://github.com/Save-Water-CBU/USB-Crack-Attack) for classroom use (Python). |
| **ClassMates** 🔒 | A study-group app: groups, invites, friends, flashcards and account pages. |
| **Restaurant app template** 🔒 | Flutter: shopping cart, maps and theming for a reusable restaurant app. |

## `~/stack`

**Infrastructure & automation**<br />
<img src="https://skillicons.dev/icons?i=kubernetes,docker,terraform,ansible,githubactions,nginx,linux,debian,arch&theme=dark" alt="Kubernetes, Docker, Terraform, Ansible, GitHub Actions, NGINX, Linux, Debian, Arch" /><br />
<img src="https://img.shields.io/badge/Proxmox-13203A?style=flat-square&logo=proxmox&logoColor=22D3EE" alt="Proxmox" />
<img src="https://img.shields.io/badge/Rocky_Linux-13203A?style=flat-square&logo=rockylinux&logoColor=22D3EE" alt="Rocky Linux" />
<img src="https://img.shields.io/badge/OpenTofu-13203A?style=flat-square&logo=opentofu&logoColor=22D3EE" alt="OpenTofu" />
<img src="https://img.shields.io/badge/k3s-13203A?style=flat-square&logo=k3s&logoColor=22D3EE" alt="k3s" />
<img src="https://img.shields.io/badge/Flux-13203A?style=flat-square&logo=flux&logoColor=22D3EE" alt="Flux" />
<img src="https://img.shields.io/badge/Tailscale-13203A?style=flat-square&logo=tailscale&logoColor=22D3EE" alt="Tailscale" />
<img src="https://img.shields.io/badge/Caddy-13203A?style=flat-square&logo=caddy&logoColor=22D3EE" alt="Caddy" />

**Cloud & data**<br />
<img src="https://skillicons.dev/icons?i=gcp,azure,firebase,postgres&theme=dark" alt="Google Cloud, Azure, Firebase, PostgreSQL" /><br />
<img src="https://img.shields.io/badge/Neo4j-13203A?style=flat-square&logo=neo4j&logoColor=22D3EE" alt="Neo4j" />
<img src="https://img.shields.io/badge/Salesforce-13203A?style=flat-square" alt="Salesforce" />

**Languages & frameworks**<br />
<img src="https://skillicons.dev/icons?i=python,cs,dotnet,ts,java,bash,nextjs,react,flutter&theme=dark" alt="Python, C#, .NET, TypeScript, Java, Bash, Next.js, React, Flutter" />

<br />

<img src="assets/footer.svg" width="100%" alt="homelab session: k3s, flux, tofu, ansible. All systems nominal." />
