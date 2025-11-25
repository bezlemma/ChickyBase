import glob
import yaml
import os

def extract_sources():
    genes_dir = "content/genes"
    sources = set()
    
    files = glob.glob(os.path.join(genes_dir, "*.md"))
    print(f"Found {len(files)} gene files.")
    
    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # Extract YAML frontmatter
                if content.startswith('---'):
                    parts = content.split('---')
                    if len(parts) >= 3:
                        frontmatter = parts[1]
                        try:
                            data = yaml.safe_load(frontmatter)
                            if 'images' in data and data['images']:
                                for img in data['images']:
                                    if 'source' in img and img['source']:
                                        src = img['source'].strip()
                                        if src.upper() != 'GEISHA' and src.lower() != 'null':
                                            sources.add(src)
                        except yaml.YAMLError as e:
                            print(f"Error parsing YAML in {file_path}: {e}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    sorted_sources = sorted(list(sources))
    
    print(f"Found {len(sorted_sources)} unique sources.")
    
    with open("sources_list.txt", "w") as f:
        for source in sorted_sources:
            f.write(f"- {source}\n")
            print(f"- {source}")

if __name__ == "__main__":
    extract_sources()
