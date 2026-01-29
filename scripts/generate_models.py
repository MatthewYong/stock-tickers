from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    print(f"project_root = {project_root}")

    schema_path = project_root / "src" / "stock_ticker_api" / "models" / "schemas" / "stock_schema.json"
    output_path = project_root / "src" / "stock_ticker_api" / "models" / "stock_model.py"

    if not schema_path.exists():
        print(f"Schema not found: {schema_path}", file=sys.stderr)
        return 1

    cmd = [
        sys.executable, "-m", "datamodel_code_generator",
        "--input", str(schema_path),
        "--input-file-type", "jsonschema",
        "--output", str(output_path),
        "--output-model-type", "pydantic_v2.BaseModel",
    ]

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
