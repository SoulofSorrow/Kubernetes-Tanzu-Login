# Architecture

## Files

| Path | Content |
| --- | --- |
| `start.py` | The application (PyQt5 GUI) |
| `config.yaml` | Namespaces with server and cluster names (sample values) |
| `install.txt` | Dependency hints (`brew reinstall pyqt@5`, pip install) |
| `start.exe` | Committed Windows GUI executable (PE32+); build process not defined in the repository |
| `Makefile` | Repo scaffolding only (`.editorconfig`, `.gitignore`, `.dockerignore`, pre-commit hook checking the git identity, `set-git-local`, `clean`); no build or test target |
| `README.md` | German user documentation |

## Code map (`start.py`)

| Name | Responsibility |
| --- | --- |
| `PasswordDialog` | `QDialog` with username and masked password fields |
| `TanzuLoginUI` | Main window: buttons `1) Login`, `2) Kubeconfig löschen`, output `QTextEdit` |
| `TanzuLoginUI.login()` | Login flow (below) |
| `TanzuLoginUI.delete_kubeconfig()` | Confirmation dialog, then `rm -rf ~/.kube` |
| `TanzuLoginUI.display_message()` | Appends to the output widget and prints to stdout |
| `load_cluster_config()` | `yaml.safe_load` of `config.yaml` next to `start.py` |
| `select_tns_name()`, `select_cluster_name()` | `QInputDialog.getItem` selection; cancel raises `ValueError` |
| `generate_login_command()` | Builds the `kubectl-vsphere login` command string |

## Login flow

1. Load `config.yaml`; missing file shows an error and stops.
2. Select a namespace (top-level key of `config.yaml`).
3. Read `server` of that namespace; missing key shows an error.
4. `PasswordDialog`: username and password. The password is set as
   `os.environ['KUBECTL_VSPHERE_PASSWORD']`.
5. Select a cluster from `cluster_names`.
6. Run `kubectl-vsphere login --server <server> --vsphere-username
   <username>@<domain> --insecure-skip-tls-verify
   --tanzu-kubernetes-cluster-namespace <namespace>
   --tanzu-kubernetes-cluster-name <cluster>` with `subprocess.run(...,
   shell=True, check=True)`. `<domain>` is a literal placeholder in the code.
7. Success: delete `KUBECTL_VSPHERE_PASSWORD` from the environment and quit
   the application. Failure: show stderr.

## `config.yaml` format

```yaml
<namespace>:
  server: <address of the vSphere supervisor>
  cluster_names:
    - <cluster>
```

## External requirements

- `kubectl-vsphere` in `PATH` (the README names `kubectl`).
- PyQt5, PyYAML.
