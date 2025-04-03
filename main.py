from src.LinkCreator import *
from src.GapChecker import *
from src.MssingPapers import *
from src.Scrape import *

df = pd.read_excel('Data/Input/listofpapers.xlsx')
df = combine_submitted_by_columns(df)
submitted_by_cols = [col for col in df.columns if col.startswith("Submitted By.")]
df = combine_AgItems_columns(df)
AgItems_Cols = [col for col in df.columns if col.startswith("Ag. Items.")]
df = df.drop(columns=submitted_by_cols)
df = df.drop(columns=AgItems_Cols)
df = df.drop(columns=['S','F','R'])
df = transform_meeting_column(df)
df = create_download_links(df)

df.to_csv('Data/Output/listofpapers-WithLinks.csv', index=False)
input_file = "Data/Output/listofpapers-WithLinks.csv"
output_file = "document_number_gaps.csv"
gap_analysis = analyze_document_numbering(input_file, output_file)
analyze_and_filter_data("Data/Output/listofpapers-WithLinks.csv", "Data/Output/listofpapers-WithLinks-AllEnglish.csv")
check_links_and_filter("Data/Output/listofpapers-WithLinks-AllEnglish.csv", "Data/Output/listofpapers-WithLinks-AllEnglish-Existing.csv")

input_file = "Data/Output/listofpapers-WithLinks-AllEnglish-Existing.csv"
download_papers(input_file, "papers")
