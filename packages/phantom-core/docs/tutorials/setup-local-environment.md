# Setup Local Development Environment

This project uses **VS Code Dev Containers** for a consistent development environment.

## Prerequisites

1. **Git:** [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. **Docker:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) (or Docker Engine + Docker Compose). Ensure it's running.
3. **VS Code:** Install [Visual Studio Code](https://code.visualstudio.com/).
4. **VS Code Extension:** Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) (`ms-vscode-remote.remote-containers`).

## Setup Steps (Recommended: VS Code UI)

1. **Clone:**

    ```bash
    git clone https://github.com/Phantomklange/phantom.git
    cd phantom
    ```

2. **Open Folder:** Open the cloned `phantom` folder in VS Code.
3. **Reopen in Container:** When prompted by VS Code (bottom-right notification), click **"Reopen in Container"**.
4. **Wait:** The container will build and initialize (running `npm install` & `./scripts/setup-dev.sh`). This can take several minutes on the first run. Monitor the integrated terminal for progress.

**Setup is complete** when the `setup-dev.sh` script finishes successfully in the terminal.

## Alternative Setup (Terminal CLI)

1. **Install Dev Containers CLI** (one time):

    ```bash
    npm install -g @devcontainers/cli
    ```

2. **Clone & CD:**

    ```bash
    git clone https://github.com/Phantomklange/phantom.git
    cd phantom
    ```

3. **Build & Start:**

    ```bash
    devcontainer up --workspace-folder .
    ```

4. **Run Commands** (examples):

    ```bash
    # Run docs dev server
    devcontainer exec --workspace-folder . npm run dev

    # Open a shell inside the container
    devcontainer exec --workspace-folder . bash
    ```

5. **Stop Container:**

    ```bash
    devcontainer down --workspace-folder .
    ```

## Rebuilding the Container

If dependencies or the container definition change, rebuild:

* **VS Code:** Command Palette (Ctrl+Shift+P) -> `Dev Containers: Rebuild Container`.
* **CLI:** `devcontainer down --workspace-folder . && devcontainer up --workspace-folder .`

## Troubleshooting

* Ensure Docker Desktop is running.
* Check logs in VS Code's "Dev Containers" output tab or via `docker logs <container_name>`.
* If files seem missing in VS Code Explorer after startup, refresh the Explorer or check via the integrated terminal (`ls dist`).
