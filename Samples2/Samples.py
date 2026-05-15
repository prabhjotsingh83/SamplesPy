import json
import os

# Mapping for source to base URL
source_mapping = {
    "UTB": "https://www.youtube.com/",
    "XVID": "https://xvideos.com/"
}


def load_template(template_name):
    """Load HTML template from file"""
    template_path = os.path.join('templates', template_name)
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: Template {template_path} not found!")
        return ""

def load_data_from_json(filename):
    """Load data from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filename}")
        return []

def get_full_url(item):
    """Construct full URL by combining source mapping with link"""
    base_url = source_mapping.get(item["source"], "")
    return base_url + item["link"]

def sort_by_rank_and_tags(data_list):
    """Sort list by rank (ascending) and then by first tag (alphabetically)"""
    return sorted(data_list, key=lambda x: (x["source"], x["rank"], x["tags"][0] if x["tags"] else ""))


def generate_table_rows(sorted_data):
    """Generate HTML table rows from sorted data"""
    rows_html = ""

    for item in sorted_data:
        full_url = get_full_url(item)

        # Create tags HTML
        tags_html = ""
        for tag in item['tags']:
            tags_html += f'<span class="tag">{tag}</span>'

        # Add table row
        rows_html += f"""                <tr>
                    <td class="key">{item['key']}</td>
                    <td class="key">{item['source']}</td>
                    <td class="rank">{item['rank']}</td>
                    <td class="tags">{tags_html}</td>
                    <td class="link">
                        <a href="{full_url}" target="_blank" rel="noopener noreferrer">
                            {full_url}
                        </a>
                    </td>
                </tr>
"""

    return rows_html


def create_html_file(sorted_data):
    """Create an HTML file with a table containing rank, tags, and links"""
    # Load templates
    header_html = load_template('header.html')
    footer_html = load_template('footer.html')

    if not header_html or not footer_html:
        print("Error: Could not load HTML templates!")
        return

    # Generate table rows
    table_rows = generate_table_rows(sorted_data)

    # Combine all parts
    html_content = header_html + table_rows + footer_html

    # Write to file
    with open('samples2.html', 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML file 'samples2.html' has been created successfully!")
    print(f'File location: file://{os.getcwd()}/samples2.html')

if __name__ == "__main__":
    # Load data from JSON file
    data = load_data_from_json('data/data.json')

    if data:
        # Sort the data
        sorted_data = sort_by_rank_and_tags(data)

        # Create HTML file
        create_html_file(sorted_data)
    else:
        print("No data loaded. Please check your data.json file.")