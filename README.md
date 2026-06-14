<h1 align="center">🧬 Project Helix</h1>

<p align="center">A research template for the agentic age.</p>

<p align="center">
  <a href="LICENSE"><img alt="Open Source" src="https://img.shields.io/badge/Open%20Source-%E2%9D%A4-2ea44f" /></a>
  <a href="https://www.python.org/"><img alt="Python supported" src="https://img.shields.io/badge/Supported-Python-3776AB?logo=python&logoColor=white" /></a>
  <a href="https://www.r-project.org/"><img alt="R supported soon" src="https://img.shields.io/badge/Supported%20soon-R-276DC3?logo=r&logoColor=white" /></a>
  <a href="LICENSE"><img alt="License MIT" src="https://img.shields.io/badge/License-MIT-2ea44f" /></a>
  <a href="https://github.com/nicograssetto/Project-Helix/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/nicograssetto/Project-Helix" /></a>
  <a href="https://github.com/nicograssetto/Project-Helix/codespaces"><img alt="Open in Codespaces" src="https://img.shields.io/badge/Open%20in-Codespaces-fb8c00?logo=github" /></a>
</p>

Project Helix shows how researchers can boost productivity in the agentic age by combining Azure ML compute with agents, skills, and MCP-based workflows that support day-to-day research. It is tool-agnostic by design: you can use GitHub Copilot, Claude Code, Cursor, OpenCode, or other coding assistants. The project serves two audiences: Research IT teams who deploy and manage the infrastructure, and researchers who use it to run and accelerate their work.

Fields that can benefit from this repo include `Physics`, `Machine Learning`, `Data Science`, `Statistics`, `Bioinformatics`, `Artificial Intelligence`, `Economics`, and `Econometrics`, but the project is not limited to these domains.

## 🚀 Get started

### For researchers

1. Open [notebooks/getting-started.ipynb](notebooks/getting-started.ipynb) to validate your environment.
2. Install Python dependencies from [dependencies/requirements.txt](dependencies/requirements.txt).
3. Use [src/train.py](src/train.py) for local iteration, then scale experiments with [jobs/train_job.py](jobs/train_job.py) and [jobs/sweep_job.py](jobs/sweep_job.py).

### For IT administrators

1. Review and customize infrastructure in [infra/main.bicep](infra/main.bicep) and [infra/modules/resources.bicep](infra/modules/resources.bicep).
2. Set deployment values in [infra/main.parameters.json](infra/main.parameters.json).
3. Use [azure.yaml](azure.yaml) as the project deployment entry point and validate access, compute, and workspace settings before handing over to research teams.

## 📦 What's in this repository

| Surface | What it is |
| --- | --- |
| `infra/` | Bicep infrastructure-as-code (`main.bicep`) to provision the Azure resources used by the project. |
| `data/` | Data assets and dataset files used for experiments and training workflows. |
| `dependencies/` | Environment dependency definitions (for example `requirements.txt`) for reproducible setup. |
| `docs/` | Project documentation, notes, and architecture or workflow write-ups. |
| `jobs/` | Azure ML job entry points (for example sweep and training jobs). |
| `notebooks/` | Interactive notebooks for exploration, prototyping, and walkthroughs. |
| `src/` | Core source code for training and supporting project logic. |

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, pull request, and review guidelines.

## Security

If you discover a security vulnerability, please report it privately via GitHub Security Advisories for this repository.

- Do not open public issues for security vulnerabilities.
- Include reproduction steps, impact, and any suggested remediation.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.