import zipfile
import os
from pathlib import Path
import click

class PackageManager:
    def validate_project_structure(self, source_path):
        required_dirs = ['iflow', 'resources']
        for dir in required_dirs:
            if not (Path(source_path) / dir).exists():
                raise ValueError(f"❌ Missing required directory: {dir}")

    def package_project(self, source_path, output_file):
        try:
            self.validate_project_structure(source_path)
            with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(source_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_path)
                        zipf.write(file_path, arcname)
            click.echo(f"📦 Package created: {output_file}")
            return True
        except Exception as e:
            click.echo(f"❌ Packaging failed: {str(e)}")
            return False