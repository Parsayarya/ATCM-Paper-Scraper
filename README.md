# ATCM Paper Scraper

## Overview

This program scrapes and processes documents from Antarctic Treaty Consultative Meetings (ATCMs). It performs several functions:

1. Transforms meeting information into structured data
2. Creates download links for documents
3. Analyzes document numbering to identify gaps
4. Filters documents by language availability
5. Checks link accessibility
6. Downloads available documents

## Project Structure

```
.
├── main.py                 # Main script that orchestrates the entire workflow
├── src/                    # Source code directory
│   ├── LinkCreator.py      # Functions for transforming data and creating download links
│   ├── GapChecker.py       # Functions for analyzing document numbering gaps
│   ├── MissingPapers.py    # Functions for analyzing and filtering inaccessible/non-English docs
│   └── Scrape.py           # Functions for downloading documents
├── Data/                   # Data directory
│   ├── Input/              # Input data
│   │   └── listofpapers.xlsx  # Original dataset of ATCM papers
│   └── Output/             # Processed data files
│       ├── listofpapers-WithLinks.csv
│       ├── listofpapers-WithLinks-AllEnglish.csv
│       └── listofpapers-WithLinks-AllEnglish-Existing.csv
├── papers/                 # Directory where downloaded papers are stored
└── document_number_gaps.csv  # Output file with gap analysis results
```

## Installation

1. Clone the repository
2. Install the required dependencies:

```bash
pip install pandas numpy matplotlib seaborn requests tqdm roman
```

## Usage

Run the main script to execute the entire workflow:

```bash
python main.py
```

The script will:
1. Read the initial list of papers(which can be downloaded from the ATCM website)
2. Combine metadata columns
3. Transform meeting information
4. Create download links
5. Check for document numbering gaps
6. Filter for English documents
7. Check link accessibility
8. Download accessible documents

## Module Descriptions

### LinkCreator.py

Contains functions for:
- `transform_meeting_column()`: Extracts Year, Meeting Number, and CEP Number from the Meeting field
- `create_download_links()`: Generates download URLs based on document metadata
- `combine_submitted_by_columns()`: Consolidates multiple "Submitted By" columns into one
- `combine_AgItems_columns()`: Consolidates multiple "Ag. Items" columns into one

### GapChecker.py

Contains functions for:
- `analyze_document_numbering()`: Identifies gaps in document numbering sequences
- `create_gap_visualizations()`: Generates visualizations of document numbering gaps

### MissingPapers.py

Contains functions for:
- `analyze_and_filter_data()`: Analyzes non-English papers and filters for English documents
- `check_links_and_filter()`: Checks link accessibility and visualizes inaccessible documents

### Scrape.py

Contains functions for:
- `download_papers()`: Downloads papers with accessible links

## Visualizations

The program generates several visualizations:

1. **In-Accessible Papers Based on the Links**: Shows the number of inaccessible documents by year and type
2. **Non-English Papers by Year and Type**: Shows the distribution of non-English documents
3. **Document Numbering Gap Percentage**: Heatmap showing the percentage of missing document numbers

## Known Issues

The analysis identified several issues with the ATCM document collection:

1. **Inaccessible Links**: Some documents have links that are no longer accessible, particularly older documents from years like 1983, 1998, and 2003-2004.
2. **Non-English Documents**: A significant number of documents are not available in English, with a notable spike in 1985 for WP documents and increasing numbers of non-English BP documents in recent years.
3. **Document Numbering Gaps**: Several years show gaps in document numbering sequences, particularly for IP documents in 1981 and 1989 (>80% gap percentage).

## Alternative Document Source

For documents that cannot be accessed through the primary links, an alternative source is available:

[UTAS RASC Antarctic Treaty Documents](https://prod.utasrasc.cloud.edu.au/index.php/antarctic-treaty-consultative-meeting-atcm-documents-2/informationobject/inventory?sort=levelUp)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
