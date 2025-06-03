# Kubernetes Deployment Tool

A simple tool to render and deploy Kubernetes manifests using templates.

## Requirements

- Python 3.6+
- Kubernetes cluster
- kubectl configured
- Helm 3
- Required Python packages:
  - PyYAML
  - Jinja2

## Setup

1. Clone this repository
2. Create your `env.yaml` file based on `example.env.yaml`
3. Install dependencies:
   ```
   pip install pyyaml jinja2
   ```

## Usage

### 1. Configure your environment

Edit `env.yaml` with your specific configuration values.

### 2. Render templates

```bash
python render.py app1 [app2 ...]
```

This will process Jinja2 templates in the specified app directories and output rendered manifests to the `output/` directory.

### 3. Deploy applications

```bash
python deploy.py app1 [app2 ...]
```

This will apply the rendered manifests to your Kubernetes cluster.

## Available Applications

- metallb: Layer 2 load balancer
- cert-manager: Certificate management
- nginx-ingress: Nginx ingress controller
- traefik-ingress: Traefik ingress controller
- local-path-storage: Local path provisioner

## Example

```bash
# Render and deploy metallb and traefik
python render.py metallb traefik-ingress
python deploy.py metallb traefik-ingress
```