import csv
import os

# --- SHARED HTML COMPONENTS ---
HTML_HEAD = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="stylesheet.css">
  <title>PICoL Lab</title>
</head>
<body>
"""

NAVBAR = """
<div id="navbar" style="font-size: 25px; display: flex; justify-content: space-between;"> <span> <b>
  <a href="index.html"> PICoL Lab </a> • 
  <a href="people.html"> People </a> • 
  <a href="publications.html"> Publications</a> </span> <span> 🧠&nbsp;📡&nbsp;🧮 </span> </b>
</div>
<hr>
"""

HTML_FOOTER = """
</body>
</html>
"""

def generate_index_page():
    print("Generating index.html...")
    
    body_content = """

    <div style="display: flex; flex-wrap: wrap; gap: 30px;">
      
      <div style="flex: 2; min-width: 400px;">
        <div style="text-align: center; padding:5px; margin-bottom: 20px;">
          <img src="./assets/images/lab_photo.png" style="width: 100%; border-radius: 5px;" alt="PICoL Lab Photo"> <br>
          <div style="font-size: 14px; color: gray; margin-top: 5px;"> PICoL members, Spring, 2025 </div>
        </div>

        <section style="margin-bottom: 10px;">
          Welcome to the 🧠 <b>P</b>sycholinguistics, 📡 <b>I</b>nformation, and 🧮 <b>C</b>omputation <b>L</b>ab (PICoL pronounced "pickle" 🥒) at Georgetown University 
        </section>

        <p style="margin-top: 0;">Our goal in PICoL is to understand the computational mechanisms that facilitate language learning and language processing in the human mind, and to use this knowledge to build intelligent and safe language technologies. To do so, we deploy a multidisciplinary toolkit including deep learning, statistical modeling, formal linguistic theories, and experimental psycholinguistics. PICoL was launched in fall 2024 and is housed in the <a href="https://linguistics.georgetown.edu/"> Department of Linguistics </a> at Georgetown. It is directed by Prof. <a href="https://wilcoxeg.github.io/"> Ethan Gotlieb Wilcox</a>.</p>

      <div style="margin-top: 5px;">
          <div class="update-bullet" style="background-color: white; margin-bottom: 5px;">
            &#128204; <b>Prospective Students:</b> PICoL will be recruiting PhD students in Fall 2026 for admission in 2027. Please see this <a href="https://wilcoxeg.github.io/prospective-students.html"> <u> prospective students page </u> </a> on Ethan's personal website for more information.
          </div>
        </div>
      </div>

      <div style="flex: 1; min-width: 250px;">
        <h3 style="color: #0d592b; margin-top: 0; margin-bottom: 0; position: sticky; top: 0; background: white; padding-bottom: 0px; z-index: 10;">Lab News & Updates</h3>
        <div class="updates-box">
    """

    announcements_path = 'assets/data/annoucements.csv'
    if os.path.exists(announcements_path):
        with open(announcements_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                if count >= 10:  # Increased count since the box is now scrollable!
                    break
                
                embed_html = row.get('html', '').strip()
                post_date = row.get('post date', '').strip()
                
                old_date = row.get('Activity Date', '').strip()
                desc = row.get('Description', '').strip()
                link = row.get('Link to Media (e.g., paper)', '').strip()
                
                body_content += '<div class="update-bullet" style="padding: 5px 0; border-bottom: 1px solid #ddd;">'
                
                # Wrap the embed to apply the zoom and max-width fixes
                if embed_html:
                    body_content += f'<div class="embed-wrapper">{embed_html}</div>'
                elif desc:
                    display_date = post_date if post_date else old_date
                    text = f"<b>{display_date}</b>: {desc}"
                    if link:
                        text = f'<a href="{link}">{text}</a>'
                    body_content += f'&#128073; {text}'
                    
                body_content += '</div>\n'
                count += 1
    else:
        body_content += '<p><i>No recent updates.</i></p>\n'
        
    body_content += '        </div>\n      </div>\n    </div>\n<br><hr>\n'

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(HTML_HEAD + NAVBAR + body_content + HTML_FOOTER)

def get_academic_rank(role):
    r = role.lower()
    if 'director' in r or 'professor' in r: return 1
    if 'postdoc' in r: return 2
    if 'phd' in r or 'ph.d' in r: return 3
    if 'master' in r: return 4
    if 'undergrad' in r: return 5
    return 6

def generate_people_page():
    print("Generating people.html...")
    
    current_members = []
    former_members = []
    
    people_path = 'assets/data/people.csv'
    if os.path.exists(people_path):
        with open(people_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('Status', '').strip().lower() == 'former':
                    former_members.append(row)
                else:
                    current_members.append(row)
                    
    current_members.sort(key=lambda x: get_academic_rank(x.get('Role', '')))
    former_members.sort(key=lambda x: get_academic_rank(x.get('Role', '')))

    def build_people_html(members_list):
        html = ""
        for row in members_list:
            name = row.get('Name', '')
            role = row.get('Role', '')
            website = row.get('Personal Website', '')
            image = row.get('Image URL', '').strip()
            desc = row.get('Description', '')

            img_src = f"./assets/images/lab_members/{image}" if image else "./assets/images/lab_members/placeholder.png"
            name_display = f'<a href="{website}">{name}</a>' if website else name
            
            html += f"""
            <div class="person-card">
              <img src="{img_src}" alt="{name}" class="person-img">
              <div class="person-info">
                <h3>{name_display}</h3>
                <p><b>{role}</b></p>
                <p>{desc}</p>
              </div>
            </div>
            """
        return html

    body_content = "<h2>Current Members</h2>\n<div class='people-container'>\n"
    body_content += build_people_html(current_members)
    body_content += "</div>\n<hr>\n<h2>Former Members</h2>\n<div class='people-container'>\n"
    body_content += build_people_html(former_members)
    body_content += "</div>\n"

    with open('people.html', 'w', encoding='utf-8') as f:
        f.write(HTML_HEAD + NAVBAR + body_content + HTML_FOOTER)

def convert_latex_bold(author_text):
    return author_text.replace(r'\textbf{', '<b>').replace(r'}', '</b>')

def generate_publications_page():
    print("Generating publications.html...")
    pubtype_dict = {
        'Journal' : '<span class="tag journal">Journal Article</span>',
        'Proceedings' : '<span class="tag proceedings">Proceedings Article</span>',
        'Manuscript' : '<span class="tag preprint">Manuscript</span>',
        'Chapter' : '<span class="tag chapter">Book Chapter</span>',
        'Preprint' : '<span class="tag preprint">Manuscript</span>',
    }
    
    body_content = "<h2>Publications</h2>\n"
    pubs_path = 'assets/data/publications/publications.csv'
    
    if os.path.exists(pubs_path):
        with open(pubs_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            year_counter = ""
            
            for row in reader:
                authors = convert_latex_bold(row.get('Authors', '')).replace("{", "").replace("}", "")
                url = row.get('URL', '')
                title = row.get('Title', '').replace("{", "").replace("}", "")
                publication = row.get('Publication', '').replace("{", "").replace("}", "")
                date = row.get('Year', '')
                pub_type_raw = row.get('Type', '')
                pubtype = pubtype_dict.get(pub_type_raw, '<span class="tag preprint">Publication</span>')

                if date != year_counter:
                    body_content += f"<div style='width:100%; background-color: #f0f0f0; padding: 3px; margin-bottom: 0px;'> <b> {date} </b> </div>\n"
                    year_counter = date
                
                body_content += f"""
                <div class="update-bullet" style="margin-bottom: 15px;"> 
                    {pubtype} <a href="{url}" style="font-size: 18px;"><b>{title}</b></a> <br> 
                    {authors} <br> 
                    <i>{publication}</i>, {date} 
                </div>\n"""
    
    with open('publications.html', 'w', encoding='utf-8') as f:
        f.write(HTML_HEAD + NAVBAR + body_content + HTML_FOOTER)

if __name__ == "__main__":
    generate_index_page()
    generate_people_page()
    generate_publications_page()
    print("Website updated successfully!")