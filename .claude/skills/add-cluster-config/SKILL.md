---
name: add-cluster-config
description: Add or change a Tanzu namespace, supervisor server or cluster name in config.yaml for the Tanzu login GUI. Use when the user wants another namespace or cluster selectable.
---

# Add a cluster configuration

Background: `docs/architecture.md` (`config.yaml` format).

## Steps

1. Edit `config.yaml`:
   - New namespace: new top-level key with `server` and a `cluster_names`
     list.
   - New cluster: append to `cluster_names` of the namespace.
2. Values are addresses and names only. No usernames, passwords or tokens.
   Ask the user before committing real internal addresses to the repository.
3. Validate the YAML:
   `python3 -c "import yaml; print(yaml.safe_load(open('config.yaml')))"`
   (needs PyYAML; if missing, say so).
4. If the structure changes (new key per namespace), update
   `load_cluster_config()` users in `start.py` and the format block in
   `docs/architecture.md`.
5. Then the `document-change` skill.
