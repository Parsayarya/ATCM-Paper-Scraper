import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_document_numbering(input_file, output_file=None):
    """
    Analyzes the document numbering system to identify gaps per year and document type.
    
    Parameters:
    input_file (str): Path to the CSV file with document data
    output_file (str, optional): Path to save the gap analysis results
    """
    # Read the dataset
    df = pd.read_csv(input_file)
    
    # Extract document numbers from the No. column
    def extract_number(doc_id):
        if pd.isna(doc_id):
            return np.nan
        
        # Extract the numeric part after the document type (WP, IP, etc.)
        import re
        match = re.search(r'([A-Z]+)(\d+)', doc_id)
        if match:
            return int(match.group(2))  # Return as integer
        return np.nan
    
    # Add a column with just the numeric part
    df['Doc_Number'] = df['No.'].apply(extract_number)
    
    # Create a list to store gap information
    gap_results = []
    
    # If we have duplicate rows for different file extensions, keep only one instance
    if 'Extension' in df.columns:
        # Create a unique identifier for each document
        df['Doc_ID'] = df.apply(lambda row: f"{row['Year']}_{row['Type']}_{row['Doc_Number']}", axis=1)
        df_unique = df.drop_duplicates(subset=['Doc_ID'])
    else:
        df_unique = df
        
    # Group by Year and Type
    for (year, doc_type), group in df_unique.groupby(['Year', 'Type']):
        if pd.isna(year) or pd.isna(doc_type):
            continue
            
        # Get all document numbers for this year and type
        doc_numbers = sorted(group['Doc_Number'].dropna().astype(int).unique())
        
        if len(doc_numbers) <= 1:
            continue
            
        # Find the expected range and identify gaps
        expected_range = set(range(min(doc_numbers), max(doc_numbers) + 1))
        actual_set = set(doc_numbers)
        missing_numbers = sorted(expected_range - actual_set)
        
        # Calculate gap percentage
        gap_percentage = len(missing_numbers) / len(expected_range) * 100 if expected_range else 0
        
        # Store the results
        gap_results.append({
            'Year': year,
            'Type': doc_type,
            'Min_Number': min(doc_numbers),
            'Max_Number': max(doc_numbers),
            'Expected_Count': len(expected_range),
            'Actual_Count': len(actual_set),
            'Missing_Count': len(missing_numbers),
            'Gap_Percentage': gap_percentage,
            'Missing_Numbers': missing_numbers
        })
    
    # Convert results to DataFrame
    gap_df = pd.DataFrame(gap_results)
    
    # Print summary information
    if not gap_df.empty:
        print(f"Analysis complete. Found potential gaps in {len(gap_df)} year-type combinations.")
        
        # Print the top 10 combinations with the highest gap percentage
        if len(gap_df) > 0:
            print("\nTop combinations with the highest percentage of missing numbers:")
            top_gaps = gap_df.sort_values('Gap_Percentage', ascending=False).head(10)
            for _, row in top_gaps.iterrows():
                print(f"Year {row['Year']}, Type {row['Type']}: {row['Missing_Count']} missing out of {row['Expected_Count']} expected ({row['Gap_Percentage']:.1f}%)")
                if len(row['Missing_Numbers']) <= 10:
                    print(f"   Missing numbers: {row['Missing_Numbers']}")
                else:
                    print(f"   First 10 missing numbers: {row['Missing_Numbers'][:10]}...")
        
        # Save to file if requested
        if output_file:
            # Create a version without the full missing numbers list for CSV export
            export_df = gap_df.copy()
            export_df['Missing_Numbers'] = export_df['Missing_Numbers'].apply(lambda x: str(x)[:100] + '...' if len(str(x)) > 100 else x)
            export_df.to_csv(output_file, index=False)
            print(f"\nDetailed results saved to {output_file}")
    else:
        print("No document numbering gaps found in the dataset.")
    
    # Create visualizations
    create_gap_visualizations(gap_df, df_unique)
    
    return gap_df

def create_gap_visualizations(gap_df, full_df):
    """
    Creates visualizations of the document numbering gaps.
    
    Parameters:
    gap_df (DataFrame): DataFrame with gap analysis results
    full_df (DataFrame): Full DataFrame with document data
    """
    if gap_df.empty:
        return
    
    # 1. Heatmap of gap percentages by year and type
    plt.figure(figsize=(14, 8))
    # Prepare data for heatmap
    heatmap_data = gap_df.pivot_table(
        index='Year', 
        columns='Type', 
        values='Gap_Percentage',
        aggfunc='mean'
    ).fillna(0)
    
    # Create heatmap
    sns.heatmap(heatmap_data, annot=True, cmap='YlOrRd', fmt='.1f',
               linewidths=.5, cbar_kws={'label': 'Gap Percentage (%)'})
    plt.title('Document Numbering Gap Percentage by Year and Type', fontsize=16)
    plt.tight_layout()
    plt.savefig('document_gap_heatmap.png', dpi=300)
    
    # 2. Bar chart of number of documents by year and type
    plt.figure(figsize=(14, 8))
    # Count documents by year and type
    doc_counts = full_df.groupby(['Year', 'Type']).size().reset_index(name='Count')
    
    # Create grouped bar chart
    sns.barplot(x='Year', y='Count', hue='Type', data=doc_counts)
    plt.title('Number of Documents by Year and Type', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Document Type')
    plt.tight_layout()
    plt.savefig('document_count_by_type.png', dpi=300)
    
    # 3. Line plot showing gap percentage trend over time
    plt.figure(figsize=(14, 6))
    # Aggregate gap percentage by year
    yearly_gaps = gap_df.groupby(['Year', 'Type'])['Gap_Percentage'].mean().reset_index()
    
    # Create line plot
    sns.lineplot(x='Year', y='Gap_Percentage', hue='Type', marker='o', data=yearly_gaps)
    plt.title('Document Numbering Gap Percentage Trend by Year', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Gap Percentage (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('gap_percentage_trend.png', dpi=300)
    
    print("\nVisualizations saved as:")
    print("- document_gap_heatmap.png")
    print("- document_count_by_type.png")
    print("- gap_percentage_trend.png")
