# bailian-docs-llm-wiki

bailian-docs-llm-wiki is a skill for quickly looking up documentation.

## Directory Structure

| Directory | Content | Description |
| --- | --- | --- |
| `models/` | Model marketplace structured data | Fetched from Bailian console gateway; includes context window, QPM, pricing, sample code |
| `wiki/` | LLM-synthesized Wiki | Topic / concept / comparison pages, organized by functional domain |
| `raw/` | Raw documentation | Markdown originals crawled from help.aliyun.com |
| `llms.txt` | Full-text index | Complete directory tree for quick file lookup |

## Trust Priority

`models/` > `raw/` > `wiki/`

- **models/** — pulled directly from console gateway, most up-to-date
- **raw/** — crawled from the official help site
- **wiki/** — LLM-synthesized, may lag behind

## Usage

See [SKILL.md](./SKILL.md) for the full lookup workflow, quick-reference mapping, and usage constraints.
