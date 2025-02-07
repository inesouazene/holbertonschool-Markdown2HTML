#!/usr/bin/python3
"""
Markdown to HTML converter script
"""

import sys
import os


def convert_markdown_heading_to_html(lines):
    """
    Convert Markdown heading syntax to HTML.

    Args:
        lines (list): List of lines from the Markdown file.

    Returns:
        list: List of converted lines with HTML headings.
    """
    converted_lines = []
    for line in lines:
        for i in range(6, 0, -1):
            # Exactly i hashes followed by a space
            if line.startswith("#" * i + " "):
                line = f"<h{i}>{line[i+1:].strip()}</h{i}>\n"
                break
        converted_lines.append(line)
    return converted_lines


def convert_markdown_ul_list_to_html(lines):
    """
    Convert Markdown unordered list syntax to HTML.

    Args:
        lines (list): List of lines from the Markdown file.

    Returns:
        list: List of converted lines with HTML unordered list.
    """
    in_list = False
    html_lines = []

    for line in lines:
        if line.startswith("- "):  # If the line starts with '- '
            line_content = line[2:].strip()  # Extract text after the dash
            if not in_list:
                # Open a <ul> tag for the list
                html_lines.append("<ul>\n")
                in_list = True
            # Convert each item to <li>
            html_lines.append(f"   <li>{line_content}</li>\n")
        else:
            if in_list:
                # Close the <ul> tag at the end of the list
                html_lines.append("</ul>\n")
                in_list = False
            # Add the line without modification
            html_lines.append(line)

    if in_list:
        html_lines.append("</ul>\n")

    return html_lines


def convert_markdown_ol_list_to_html(lines):
    """
    Convert Markdown ordered list syntax to HTML.

    Args:
        lines (list): List of lines from the Markdown file.

    Returns:
        list: List of converted lines with HTML ordered list.
    """
    in_list = False
    html_lines = []

    for line in lines:
        if line.startswith("* "):
            line_content = line[2:].strip()
            if not in_list:
                html_lines.append("<ol>\n")
                in_list = True
            html_lines.append(f"   <li>{line_content}</li>\n")
        else:
            if in_list:
                html_lines.append("</ol>\n")
                in_list = False
            html_lines.append(line)

    if in_list:
        html_lines.append("</ol>\n")

    return html_lines


def convert_markdown_paragraph_to_html(lines):
    """
    Convert Markdown paragraphs to HTML.

    Args:
        lines (list): List of lines from the Markdown file.

    Returns:
        list: List of converted lines with HTML paragraphs.
    """
    html_lines = []
    in_paragraph = False

    for line in lines:
        stripped_line = line.strip()

        # If the line is not empty and not a list or heading
        if stripped_line and not stripped_line.startswith(("#", "-", "*")):
            if not in_paragraph:
                # Start a new paragraph
                html_lines.append("<p>\n")
                in_paragraph = True
            # Add the line to the paragraph
            html_lines.append(f"    {stripped_line}<br/>\n")
        else:
            if in_paragraph:
                # Close the current paragraph / # Remove the last <br/>
                html_lines[-1] = html_lines[-1].replace("<br/>\n", "\n")
                html_lines.append("</p>\n")
                in_paragraph = False
            # Add the line as is
            html_lines.append(line)

    # Close the last paragraph if still open
    if in_paragraph:
        # Remove the last <br/>
        html_lines[-1] = html_lines[-1].replace("<br/>\n", "\n")
        html_lines.append("</p>\n")

    return html_lines


def main():
    """
    Main function that verifies arguments, file existence
    and converts Markdown to HTML.
    """
    # Check if the number of arguments is sufficient
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        exit(1)

    # Get the file names from the arguments
    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        exit(1)

    # Read the content of the Markdown file
    with open(markdown_file, "r") as md:
        lines = md.readlines()

    # Convert Markdown headings to HTML
    converted_lines = convert_markdown_heading_to_html(lines)

    # Convert Markdown unordered lists to HTML
    converted_lines = convert_markdown_ul_list_to_html(converted_lines)

    # Convert Markdown ordered lists to HTML
    converted_lines = convert_markdown_ol_list_to_html(converted_lines)

    # Convert Markdown paragraphs to HTML
    converted_lines = convert_markdown_paragraph_to_html(converted_lines)

    # Write the converted lines to the HTML file
    with open(html_file, "w") as html:
        html.writelines(converted_lines)

    exit(0)


if __name__ == "__main__":
    main()
