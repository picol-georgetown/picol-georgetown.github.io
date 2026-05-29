import csv
from datetime import datetime

# Function to replace LaTeX bold markup with HTML <b> tags
def convert_latex_bold(author_text):
    return author_text.replace(r'\textbf{', '<b>').replace(r'}', '</b>')

# Pubtype Dictionary
pubtype_dict = {
    'Journal' : '<span class="tag journal">Journal Article</span>',
    'Proceedings' : '<span class="tag proceedings">Proceedings Article</span>',
    'Manuscript' : '<span class="tag preprint">Manuscript</span>',
    'Chapter' : '<span class="tag chapter">Book Chapter</span>',
    'Preprint' : '<span class="tag preprint">Manuscript</span>',

}

# Function to process the TSV file and generate HTML output
def process_publications(input_file, output_file):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            year_counter = ""

            for row in reader:
                authors = convert_latex_bold(row['Authors']).replace("{", "").replace("}", "")
                url = row['URL']
                title = row['Title'].replace("{", "").replace("}", "")
                publication = row['Publication'].replace("{", "").replace("}", "")
                date = row['Year']
                pubtype = pubtype_dict[row['Type']]

                if date != year_counter:
                    outfile.write(f"<div style='width:100%; background-color: #F0FFF0;'> <b> {date} </b> </div>")
                    year_counter = date
                
                # Create the HTML string
                html_output = f'<div class="update-bullet"> {pubtype} {authors} <a href="{url}"> {title}</a> <i> {publication} </i> {date} </div>\n\n'
                
                # Write the HTML to the output file
                outfile.write(html_output)

# Set input and output file names
input_file = 'publications.csv'
output_file = 'publications_list.html'

# Process the file and generate the HTML
process_publications(input_file, output_file)

print("HTML file generated successfully.")