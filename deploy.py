#!/usr/bin/env python3

import os
import sys
import subprocess

def run_cmd(cmd, shell=False):
    print(f"▶️  Running: {cmd if shell else ' '.join(cmd)}")
    subprocess.run(cmd, check=True, shell=shell)

def deploy_app(app):
    output_dir = f"output/{app}"
    helm_dir = os.path.join(output_dir, "helm")

    # 1. Helm jika ada values.yaml
    values_file = os.path.join(helm_dir, "values.yaml")
    if os.path.exists(values_file):
        run_cmd([
            "helm", "upgrade", "--install", app,
            "traefik/traefik",  # Ganti sesuai chart
            "-f", values_file,
            "--namespace", "kube-system",
            "--create-namespace"
        ])
    elif os.path.isdir(output_dir):
        run_cmd(["kubectl", "apply", "-f", output_dir])

    # 2. Jalankan perintah tambahan jika ada
    extra_cmd_path = f"sources/{app}/post-deploy.sh"
    if os.path.isfile(extra_cmd_path):
        print(f"📎 Running post-deploy commands for {app}")
        run_cmd(f"bash {extra_cmd_path}", shell=True)

def main(apps):
    for app in apps:
        print(f"🚀 Deploying {app}")
        deploy_app(app)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy.py app1 [app2 ...]")
        sys.exit(1)
    main(sys.argv[1:])
