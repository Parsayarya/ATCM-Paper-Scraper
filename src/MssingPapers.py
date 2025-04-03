import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from tqdm import tqdm
import time

def check_links_and_filter(input_file, output_file):
    """
    Check if each link in the dataframe is accessible,
    visualize existing documents by year and type,
    and save filtered results.
    
    Parameters:
    input_file (str): Path to the input CSV file
    output_file (str): Path to save the filtered CSV file
    """
    # Read the data
    df = pd.read_csv(input_file)
    
    # Add a column to track if links are accessible
    df['Exists'] = 'Unknown'
    # Filter for specific years
    # df = df[df['Year'].isin([2000, 2002, 2021])]
    
    # Function to check if a link is accessible
    def check_link(url):
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                return 'Yes'
            else:
                return 'No'
        except:
            return 'No'
    
    # Check each link with a progress bar
    print("Checking document links (this may take some time)...")
    for i, row in tqdm(df.iterrows(), total=len(df)):
        if pd.notna(row['Download_Link']):
            df.at[i, 'Exists'] = check_link(row['Download_Link'])
            # Add a small delay to avoid overwhelming the server
            # time.sleep(0.1)
    
    # Count existing documents by year and type
    # Drop duplicates based on Title column, keeping the one with 'Yes' in Exists column
    df = df.sort_values('Exists', ascending=False).drop_duplicates(subset=['Title'], keep='first')
    df = df.sort_values('Year', ascending=False)
    df.to_csv("Data/Output/listofpapers-WithLinks-AllEnglish-Existing-Column.csv")
    exists_df = df[df['Exists'] == 'No']
    yearly_counts = exists_df.groupby(['Year', 'Type']).size().reset_index(name='Count')
    
    # Create the plot
    plt.figure(figsize=(14, 8))
    
    # Use seaborn for better-looking plots
    sns.barplot(x='Year', y='Count', hue='Type', data=yearly_counts)
    
    # Customize the plot
    plt.title('In-Accessible Papers Based on the Links', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of In-Accessible Documents', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Document Type')
    
    # Enhance the layout
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('In-Accessible_papers_by_year.png', dpi=300)
    
    # Filter the dataframe to keep only rows with accessible links
    accessible_df = df[df['Exists'] == 'Yes']
    
    # Save the filtered data to a new CSV file
    accessible_df.to_csv(output_file, index=False)
    
    # Print summary statistics
    total_papers = len(df)
    accessible_papers = len(accessible_df)
    inaccessible_papers = total_papers - accessible_papers
    
    print(f"Total number of papers: {total_papers}")
    print(f"Papers with accessible links: {accessible_papers} ({accessible_papers/total_papers:.1%})")
    print(f"Papers with inaccessible links: {inaccessible_papers} ({inaccessible_papers/total_papers:.1%})")




def analyze_and_filter_data(input_file, output_file):
    """
    Read processed data, create a visualization of non-English papers,
    filter out rows without English documents, and save the result.
    
    Parameters:
    input_file (str): Path to the input CSV file
    output_file (str): Path to save the filtered CSV file
    """
    # Read the processed data
    df = pd.read_csv(input_file)
    
    # Identify rows where 'E' column is missing (non-English papers)
    df['Has_English'] = df['E'].notna()
    non_english_df = df[~df['Has_English']]
    
    # Count non-English papers by year and type
    yearly_counts = non_english_df.groupby(['Year', 'Type']).size().reset_index(name='Count')
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Use seaborn for better-looking plots
    sns.barplot(x='Year', y='Count', hue='Type', data=yearly_counts)
    
    # Customize the plot
    plt.title('Non-English Papers by Year and Type', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Papers', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Document Type')
    
    # Enhance the layout
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('non_english_papers_by_year.png', dpi=300)    
    # Filter the dataframe to keep only rows with 'E' column values
    english_df = df[df['E'].notna()]
    
    # Save the filtered data to a new CSV file
    english_df.to_csv(output_file, index=False)
    
    # Print summary statistics
    total_papers = len(df)
    english_papers = len(english_df)
    non_english_papers = total_papers - english_papers
    
    print(f"Total number of papers: {total_papers}")
    print(f"Papers with English versions: {english_papers} ({english_papers/total_papers:.1%})")
    print(f"Papers without English versions: {non_english_papers} ({non_english_papers/total_papers:.1%})")



