from Bio import Entrez
import datetime

# Function to generate a plain text report
def generate_text_report(results):
    text_content = ""

    for result in results:
        text_content += f"Title: {result['Title']}\n"
        text_content += f"Authors: {', '.join(result['AuthorList'])}\n"
        text_content += f"Publication Date: {result['PubDate']}\n"

        if 'Abstract' in result:
            # Encode abstract to handle Unicode characters
            abstract = result['Abstract'].encode('utf-8').decode('utf-8', 'ignore')
            text_content += f"Abstract: {abstract}\n"
        else:
            text_content += "Abstract: Abstract not available\n"

    return text_content

# Input keywords or phrases from the user as a comma-separated string
user_input = input("Enter keywords or phrases (comma-separated): ")
keywords = user_input.split(',')

# Set up the query
query = " AND ".join(keywords) + "[Title]"

# Calculate the date range for the last 10 years
current_year = datetime.datetime.now().year
ten_years_ago = current_year - 10
date_range = f"{ten_years_ago}/01/01:{current_year}/12/31[Date - Publication]"

# Perform the PubMed search
Entrez.email = "your_email@example.com"  # Provide your email address
handle = Entrez.esearch(db="pubmed", term=query, retmax=10, mindate=ten_years_ago, maxdate=current_year)
result = Entrez.read(handle)
handle.close()

# Extract and store information for each paper
paper_results = []
if 'IdList' in result:
    for pmid in result['IdList']:
        summary = Entrez.esummary(db="pubmed", id=pmid)
        summary_result = Entrez.read(summary)[0]

        title = summary_result['Title']
        authors = summary_result['AuthorList']
        pub_date = summary_result['PubDate']

        paper_results.append({
            'Title': title,
            'AuthorList': authors,
            'PubDate': pub_date,
        })

    # Generate plain text report
    text_report = generate_text_report(paper_results)

    # Save the plain text report to a TXT file
    with open("literature_review_results.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write(text_report)

    print("Results saved to literature_review_results.txt")
else:
    print("No papers found.")
