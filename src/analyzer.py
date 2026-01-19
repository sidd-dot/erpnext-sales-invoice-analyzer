import ast
import json
import os
import sys
from pathlib import Path

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

entities = []
relationships = []
business_rules = []
data_access = []

class Analyzer(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.current_class = None
        self.current_function = None

    # ---------- ENTITIES ----------
    def visit_ClassDef(self, node):
        entities.append({
            "type": "class",
            "name": node.name,
            "file": self.filename
        })

        # Inheritance
        for base in node.bases:
            if isinstance(base, ast.Name):
                relationships.append({
                    "type": "inherits",
                    "from": node.name,
                    "to": base.id
                })

        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = None

    def visit_FunctionDef(self, node):
        entities.append({
            "type": "function",
            "name": node.name,
            "class": self.current_class,
            "file": self.filename
        })

        # Business rule hint: validate_*
        if node.name.startswith("validate"):
            business_rules.append({
                "type": "validation_function",
                "name": node.name,
                "file": self.filename
            })

        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = None

    # ---------- RELATIONSHIPS ----------
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        elif isinstance(node.func, ast.Name):
            func_name = node.func.id
        else:
            func_name = "unknown"

        relationships.append({
            "type": "calls",
            "from": self.current_function,
            "to": func_name,
            "file": self.filename
        })

        # Data access detection
        if isinstance(node.func, ast.Attribute):
            full = ast.unparse(node.func)
            if full.startswith("frappe.db") or full.startswith("frappe.get"):
                data_access.append({
                    "function": self.current_function,
                    "call": full,
                    "file": self.filename
                })

        self.generic_visit(node)

    # ---------- BUSINESS RULES ----------
    def visit_If(self, node):
        business_rules.append({
            "type": "conditional",
            "condition": ast.unparse(node.test),
            "function": self.current_function,
            "file": self.filename
        })
        self.generic_visit(node)

    def visit_Raise(self, node):
        business_rules.append({
            "type": "exception",
            "function": self.current_function,
            "file": self.filename
        })
        self.generic_visit(node)


def analyze_path(path):
    for py_file in Path(path).rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
            Analyzer(str(py_file)).visit(tree)
        except Exception as e:
            print(f"⚠️ Skipped {py_file}: {e}")


def write_outputs():
    json.dump(entities, open(OUTPUT_DIR / "entities.json", "w"), indent=2)
    json.dump(relationships, open(OUTPUT_DIR / "relationships.json", "w"), indent=2)
    json.dump(business_rules, open(OUTPUT_DIR / "business_rules.json", "w"), indent=2)
    json.dump(data_access, open(OUTPUT_DIR / "data_access.json", "w"), indent=2)

    # Mermaid
    with open(OUTPUT_DIR / "relationships.mermaid", "w") as f:
        f.write("graph TD\n")
        for r in relationships:
            if r["type"] in ("calls", "inherits"):
                f.write(f'  {r["from"]} --> {r["to"]}\n')

    with open(OUTPUT_DIR / "summary.md", "w") as f:
        f.write("# Analysis Summary\n\n")
        f.write(f"- Classes & functions discovered: {len(entities)}\n")
        f.write(f"- Relationships detected: {len(relationships)}\n")
        f.write(f"- Business rules flagged: {len(business_rules)}\n")
        f.write(f"- Data access points: {len(data_access)}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/analyzer.py <path>")
        sys.exit(1)

    analyze_path(sys.argv[1])
    write_outputs()
    print("✅ Analysis complete. Outputs written to /output")
