import pandas as pd
import re
from roman import fromRoman

def transform_meeting_column(df):
    """
    Transform the Meeting column into separate Year, Meeting, and CEP columns.
    
    Parameters:
    df (pandas.DataFrame): DataFrame with a 'Meeting' column
    
    Returns:
    pandas.DataFrame: DataFrame with added 'Year', 'Meeting', and 'CEP' columns
    """
    # Create a copy of the dataframe to avoid modifying the original
    result_df = df.copy()
    
    # Initialize new columns
    result_df['Year'] = None
    result_df['Meeting_Number'] = None
    result_df['CEP_Number'] = None
    
    # Define patterns to extract information
    year_pattern = r'\((\d{4})\)'
    atcm_pattern = r'ATCM\s+([IVXL0-9]+)'
    cep_pattern = r'CEP\s+([IVXL0-9]+)'
    
    # Process each row
    for idx, row in result_df.iterrows():
        meeting_str = row['Meeting']
        
        # Extract year
        year_match = re.search(year_pattern, meeting_str)
        if year_match:
            result_df.at[idx, 'Year'] = int(year_match.group(1))
        
        # Extract meeting number
        meeting_match = re.search(atcm_pattern, meeting_str)
        if meeting_match:
            meeting_num = meeting_match.group(1)
            # Convert Roman numerals to integers if necessary
            if meeting_num.isdigit():
                result_df.at[idx, 'Meeting_Number'] = int(meeting_num)
            else:
                try:
                    result_df.at[idx, 'Meeting_Number'] = fromRoman(meeting_num)
                except:
                    # Handle invalid Roman numerals
                    result_df.at[idx, 'Meeting_Number'] = meeting_num
        
        # Extract CEP number
        cep_match = re.search(cep_pattern, meeting_str)
        if cep_match:
            cep_num = cep_match.group(1)
            # Convert Roman numerals to integers if necessary
            if cep_num.isdigit():
                result_df.at[idx, 'CEP_Number'] = int(cep_num)
            else:
                try:
                    result_df.at[idx, 'CEP_Number'] = fromRoman(cep_num)
                except:
                    # Handle invalid Roman numerals
                    result_df.at[idx, 'CEP_Number'] = cep_num
    
    return result_df

def create_download_links(df):
    """
    Create download links based on Meeting, No., and Year columns.
    Also extract the document type.
    For 2002 and 2021, create two versions of each document with both file extensions.
    
    Parameters:
    df (pandas.DataFrame): DataFrame with 'Meeting', 'No.', and 'Year' columns
    
    Returns:
    pandas.DataFrame: DataFrame with added 'Download_Link' and 'Type' columns,
                     duplicated rows for transition years with different extensions
    """
    # Create a copy of the dataframe to avoid modifying the original
    result_df = df.copy()
    
    # Initialize new columns
    result_df['Download_Link'] = None
    result_df['Type'] = None
    result_df['Extension'] = None  # Add a column to track the file extension used
    
    # Create a list to store rows for duplicate file extensions
    additional_rows = []
    
    # Process each row
    for idx, row in result_df.iterrows():
        doc_number = row['No.'].strip() if pd.notna(row['No.']) else ""
        year = row['Year']
        meeting_number = row['Meeting_Number']
        
        # Extract document type and number
        type_match = re.match(r'([A-Z]+)(\d+)(?:\s+rev\.\s+(\d+))?', doc_number)
        if type_match:
            doc_type = type_match.group(1).lower()  # wp, ip, bp, sp
            doc_num = type_match.group(2).zfill(3)  # pad with leading zeros
            revision = type_match.group(3)
            
            # Save the document type
            result_df.at[idx, 'Type'] = type_match.group(1)  # WP, IP, BP, SP
            
            # Determine file extension based on year
            if year < 2002:
                file_ext = 'pdf'
            elif year == 2002:
                # For 2002, we'll use .pdf for the original row
                file_ext = 'pdf'
                # And create a duplicate row with .doc
                new_row = row.copy()
            elif year < 2021:
                file_ext = 'doc'
            elif year == 2021:
                # For 2021, we'll use .doc for the original row
                file_ext = 'doc'
                # And create a duplicate row with .docx
                new_row = row.copy()
            else:
                file_ext = 'docx'
            
            # Construct the download link
            base_url = f"https://documents.ats.aq/ATCM{meeting_number}/{doc_type}/"
            file_name = f"ATCM{meeting_number}_{doc_type}{doc_num}"
            
            # Add revision if present
            if revision:
                file_name += f"_rev{revision}"
            
            # Complete the URL
            download_link = f"{base_url}{file_name}_e.{file_ext}"
            
            # Save the download link and extension
            result_df.at[idx, 'Download_Link'] = download_link
            result_df.at[idx, 'Extension'] = file_ext
            
            # If this is a 2002 document, create a duplicate with .doc extension
            if year == 2002:
                new_row = row.copy()
                doc_link = f"{base_url}{file_name}_e.doc"
                new_row['Download_Link'] = doc_link
                new_row['Extension'] = 'doc'
                additional_rows.append(new_row)
            
            # If this is a 2021 document, create a duplicate with .docx extension
            elif year == 2021:
                new_row = row.copy()
                docx_link = f"{base_url}{file_name}_e.docx"
                new_row['Download_Link'] = docx_link
                new_row['Extension'] = 'docx'
                additional_rows.append(new_row)
    
    # Append the additional rows for documents with alternate extensions
    if additional_rows:
        additional_df = pd.DataFrame(additional_rows)
        result_df = pd.concat([result_df, additional_df], ignore_index=True)
    
    return result_df

def combine_submitted_by_columns(df):
    # Get all columns that start with "Submitted By"
    submitted_by_cols = [col for col in df.columns if col.startswith("Submitted By")]
    
    # Create a new column that combines all "Submitted By" columns
    df['Submitted By'] = df[submitted_by_cols].apply(
        lambda row: ', '.join([str(val) for val in row if pd.notna(val)]), 
        axis=1
    )
    
    return df


def combine_AgItems_columns(df):
    # Get all columns that start with "Submitted By"
    submitted_by_cols = [col for col in df.columns if col.startswith("Ag. Items")]
    
    # Create a new column that combines all "Submitted By" columns
    df['Ag. Items'] = df[submitted_by_cols].apply(
        lambda row: ', '.join([str(val) for val in row if pd.notna(val)]), 
        axis=1
    )
    
    return df
