"""
report_generator.py

Takes the GPT-generated portfolio explanation and saves it to a Markdown (.md) file
under the `reports/` directory. Filenames are based on the persona.

Key function:
- save_markdown_report(persona_name, content): Saves portfolio report as Markdown.
"""

import os

def save_markdown_report(persona_name: str, content: str, output_dir: str = "reports"):
    """
    Saves the GPT-generated portfolio explanation to a markdown file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{persona_name.lower().replace(' ', '_')}_report.md"
    path = os.path.join(output_dir, filename)

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Report saved to {path}")
    except Exception as e:
        print(f"Error writing report to {path}: {e}")