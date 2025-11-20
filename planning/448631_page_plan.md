# Planning Document: GEISHA Gene Page (ID 448631)

## Overview
The GEISHA gene detail page (e.g., https://geisha.arizona.edu/geisha/search.jsp?gene=448631) presents a rich set of information for a given chicken gene.  The page layout includes navigation, a header with the gene name, a **Gene Information** table, expression images, and an expression data table.  Our goal is to replicate this content in the static ChickyBase site.

## Page Elements & Observations (Updated via Browser Inspection)
1.  **Tabs Layout**: The page is divided into two main tabs:
    *   **Gene Summary Tab**: Contains core metadata.
        *   *Gene Section*: Official Symbol, Official Full Name, CGNC ID, Gene Type, Genomic Map.
        *   *Sequence Information*: Genomic, RNA, Polypeptide links.
        *   *Orthology*: Human, Mouse, Xenopus, Zebrafish (Entrez/Ensembl IDs).
        *   *Gene Ontology*: Molecular Function, Biological Process, Cellular Component.
        *   *Links*: Entrez Gene, Ensembl Gene, KEGG.
    *   **Expression Tab**: Contains the in-situ hybridization data.
        *   *Header*: GEISHA Id, Data Source, Primer Info.
        *   *Data Organization*: Grouped by **Stage Ranges** (e.g., "Stages 4-6", "Stages 7-12").
        *   *Rows*: Within each stage group, rows contain:
            *   **Image**: Thumbnail (clickable to open modal).
            *   **Location**: Anatomical location links.
            *   **Comments**: Text notes.

2.  **Top Navigation Bar** – links to Home, Contact, Anatomical Location, Stage, Gene Name, GEISHA ID, etc.
3.  **Gene Header** – displays the gene symbol and full description (e.g., `ABCC5 ATP binding cassette subfamily C member 5`).

## Data Required to Reproduce the Page
| Category | Fields to Capture | Source in Scraper |
|----------|------------------|-------------------|
| **Core Gene** | `gene_id`, `gene_name`, `description` | Parsed from gene list and page title |
| **Metadata (Summary Tab)** | `official_symbol`, `official_full_name`, `cgnc_id`, `gene_type`, `orthology` (human/mouse/etc IDs), `gene_ontology` (MF, BP, CC) | **NEW**: Need to parse the specific "Gene Summary" table structure. |
| **Expression Data (Expression Tab)** | `stage_group` (e.g. "4-6"), `image_url` (thumb & full), `location`, `comments`, `geisha_id` | **NEW**: Need to parse the stage-grouped tables in the "Expression" tab section. |
| **Images** | `image_id`, `url` (full‑res), `thumbnail_url`, `local_path` (optional) | Image loop in `parse_gene_page` – builds URLs from `photos/` and `photos/thumbs/` |

## JSON Schema (Refined)
```json
{
  "gene_id": "448631",
  "gene_name": "ABCC5",
  "description": "ATP binding cassette subfamily C member 5",
  "metadata": {
      "official_symbol": "ABCC5",
      "official_full_name": "ATP binding cassette subfamily C member 5",
      "cgnc_id": "...",
      "orthology": {
          "human_entrez": "...",
          "mouse_entrez": "..."
      },
      "gene_ontology": {
          "molecular_function": ["..."],
          "biological_process": ["..."]
      }
  },
  "expression_data": [
      {
          "stage_range": "4-6",
          "entries": [
              {
                  "image_id": "ABCC5_1",
                  "thumbnail_url": "...",
                  "full_image_url": "...",
                  "locations": ["Heart", "Limb"],
                  "comments": "..."
              }
          ]
      }
  ]
}
```

## Implementation Notes
- **Scraper Enhancements**: 
    - **Metadata**: The "Gene Summary" table needs to be parsed more robustly. Look for the "Gene Summary" tab content specifically.
    - **Expression Data**: The scraper needs to handle the stage-grouped tables. It should iterate through these groups and extract the image-location pairs.
- **Image Handling**: Keep the `--skip-images` flag. Ensure images are correctly associated with their stage/location in the JSON structure if possible (currently they are just a flat list).
- **Generator Adjustments**: 
    - **Sidebar**: Display the rich metadata from the "Gene Summary" section.
    - **Main Content**: Replicate the "Stage Group" layout. Show images grouped by stage, with their location labels.


## Next Steps
1. Verify the current scraper extracts the **Gene Information** table for gene 448631 (inspect the JSON output).
2. If missing fields, adjust `parse_gene_metadata` accordingly.
3. Update `_extract_entry_data` to reliably capture `stage` and `location`.
4. Modify `generate_qmd.py` sidebar block to display the new metadata fields (as per the implementation plan).
5. Regenerate the site and compare visually with the original GEISHA page.
"
