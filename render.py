import os
import sys
import yaml
from jinja2 import Environment, FileSystemLoader

def load_env_vars(path='env.yaml'):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def render_jinja_dir(source_dir, output_dir, context):
    env = Environment(loader=FileSystemLoader(source_dir), keep_trailing_newline=True)
    for root, _, files in os.walk(source_dir):
        rel_dir = os.path.relpath(root, source_dir)
        for file in files:
            if not file.endswith(".j2"):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.join(rel_dir, file[:-3])  # remove .j2
            output_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            template = env.get_template(os.path.relpath(full_path, source_dir))
            rendered = template.render(context)
            with open(output_path, 'w') as f:
                f.write(rendered)
            print(f"Rendered: {output_path}")

def main(apps):
    env_vars = load_env_vars()
    for app in apps:
        app_vars = env_vars.get(app, {})
        merged_vars = {**env_vars.get("global", {}), **app_vars}
        render_jinja_dir(f"sources/{app}", f"output/{app}", merged_vars)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python render.py app1 [app2 ...]")
        sys.exit(1)
    main(sys.argv[1:])
