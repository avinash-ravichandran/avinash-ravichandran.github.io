
# coding: utf-8

def detect_publication_type(venue, paper_url=''):
    """Detect publication type based on venue string and URL."""
    venue_lower = venue.lower()
    url_lower = paper_url.lower() if paper_url else ''
    
    # Patents - check both venue and URL
    if ('patent' in venue_lower or 'patents.google.com' in venue_lower or 
        'patents.google.com' in url_lower):
        return 'patent'
    
    # Preprints
    if 'arxiv' in venue_lower or 'preprint' in venue_lower:
        return 'preprint'
    
    # Known conferences (check first to avoid misclassification)
    conference_names = [
        'cvpr', 'iccv', 'eccv', 'neurips', 'nips', 'icml', 'iclr',
        'aaai', 'ijcai', 'siggraph', 'bmvc', 'wacv', 'accv',
        'conference', 'proceedings', 'workshop', 'symposium'
    ]
    
    # Specific conference venue patterns
    conference_patterns = [
        'proceedings of the ieee/cvf',
        'advances in neural information processing systems',
        'international conference',
        'workshop',
        'symposium'
    ]
    
    # Special cases: Springer-published conferences (ECCV, ICCV, etc.)
    # Check URL patterns for Springer conferences
    springer_conference_urls = [
        'link.springer.com/chapter',
        'eccv',
        'iccv', 
        'accv'
    ]
    
    if ('springer' in venue_lower and 
        any(pattern in url_lower for pattern in springer_conference_urls)):
        return 'conference'
    
    # Check specific conference patterns first
    if any(pattern in venue_lower for pattern in conference_patterns):
        return 'conference'
    
    # Check conference names
    if any(conf in venue_lower for conf in conference_names):
        return 'conference'
    
    # Journals (after checking conferences)
    journal_keywords = [
        'transactions', 'journal', 'ieee transactions', 'acm', 'springer', 'elsevier',
        'pami', 'tpami', 'corr'
    ]
    if any(keyword in venue_lower for keyword in journal_keywords):
        return 'journal'
    
    # Special cases
    if 'advances in neural information processing systems' in venue_lower:
        return 'conference'  # NeurIPS
    
    # Default to conference if uncertain
    return 'conference'

def extract_conference_from_springer_url(paper_url):
    """Extract proper conference name from Springer URL using ISBN patterns."""
    if not paper_url or 'link.springer.com/chapter' not in paper_url:
        return None
    
    # ISBN to conference mapping for computer vision conferences
    isbn_to_conference = {
        # ECCV 2024
        '978-3-031-73464-8': 'ECCV 2024',
        '978-3-031-73013-4': 'ECCV 2024', 
        '978-3-031-72983-1': 'ECCV 2024',
        
        # ECCV 2022
        '978-3-031-20059-5': 'ECCV 2022',
        '978-3-031-20044-1': 'ECCV 2022',
        '978-3-031-20062-5': 'ECCV 2022',
        '978-3-031-20086-1': 'ECCV 2022',
        
        # ECCV 2020
        '978-3-030-58571-6': 'ECCV 2020',
        '978-3-030-58610-2': 'ECCV 2020',
        '978-3-030-58555-6': 'ECCV 2020',
        '978-3-030-58548-8': 'ECCV 2020',
        
        # ECCV 2018
        '978-3-030-01249-6': 'ECCV 2018',
        '978-3-030-01234-2': 'ECCV 2018',
        '978-3-030-01216-8': 'ECCV 2018',
        
        # ICCV 2019
        '978-3-030-33709-3': 'ICCV 2019',
        '978-3-030-33720-8': 'ICCV 2019',
        
        # ACCV 2020
        '978-3-030-69532-3': 'ACCV 2020',
        '978-3-030-69525-5': 'ACCV 2020',
        
        # Add more mappings as needed
    }
    
    # Extract ISBN from URL (format: 978-x-xxx-xxxxx-x)
    import re
    isbn_match = re.search(r'978-\d-\d{3}-\d{5}-\d', paper_url)
    if isbn_match:
        isbn = isbn_match.group()
        return isbn_to_conference.get(isbn)
    
    return None

# # Publications markdown generator for academicpages
# 
# Takes a TSV of publications with metadata and converts them for use with [academicpages.github.io](academicpages.github.io). This is an interactive Jupyter notebook, with the core python code in publications.py. Run either from the `markdown_generator` folder after replacing `publications.tsv` with one that fits your format.
# 
# TODO: Make this work with BibTex and other databases of citations, rather than Stuart's non-standard TSV format and citation style.
# 

# ## Data format
# 
# The TSV needs to have the following columns: pub_date, title, venue, excerpt, citation, site_url, and paper_url, with a header at the top. 
# 
# - `excerpt` and `paper_url` can be blank, but the others must have values. 
# - `pub_date` must be formatted as YYYY-MM-DD.
# - `url_slug` will be the descriptive part of the .md file and the permalink URL for the page about the paper. The .md file will be `YYYY-MM-DD-[url_slug].md` and the permalink will be `https://[yourdomain]/publications/YYYY-MM-DD-[url_slug]`


# ## Import pandas
# 
# We are using the very handy pandas library for dataframes.

# In[2]:

import pandas as pd


# ## Import TSV
# 
# Pandas makes this easy with the read_csv function. We are using a TSV, so we specify the separator as a tab, or `\t`.
# 
# I found it important to put this data in a tab-separated values format, because there are a lot of commas in this kind of data and comma-separated values can get messed up. However, you can modify the import statement, as pandas also has read_excel(), read_json(), and others.

# In[3]:

publications = pd.read_csv("publications.tsv", sep="\t", header=0)
publications


# ## Escape special characters
# 
# YAML is very picky about how it takes a valid string, so we are replacing single and double quotes (and ampersands) with their HTML encoded equivilents. This makes them look not so readable in raw format, but they are parsed and rendered nicely.

# In[4]:

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;"
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)


# ## Creating the markdown files
# 
# This is where the heavy lifting is done. This loops through all the rows in the TSV dataframe, then starts to concatentate a big string (```md```) that contains the markdown for each type. It does the YAML metadata first, then does the description for the individual page. If you don't want something to appear (like the "Recommended citation")

# In[5]:

import os
for row, item in publications.iterrows():
    
    md_filename = str(item.pub_date) + "-" + item.url_slug + ".md"
    html_filename = str(item.pub_date) + "-" + item.url_slug
    year = item.pub_date[:4]
    
    ## YAML variables
    
    md = "---\ntitle: \""   + item.title + '"\n'
    
    md += """collection: publications"""
    
    md += """\npermalink: /publication/""" + html_filename
    
    if len(str(item.excerpt)) > 5:
        md += "\nexcerpt: '" + html_escape(item.excerpt) + "'"
    
    md += "\ndate: " + str(item.pub_date) 
    
    # Fix Springer venue names with proper conference names
    venue = str(item.venue)
    paper_url = str(item.paper_url) if hasattr(item, 'paper_url') and str(item.paper_url) != 'nan' else ''
    if ('springer' in venue.lower() and paper_url and 
        'link.springer.com/chapter' in paper_url):
        conference_name = extract_conference_from_springer_url(paper_url)
        if conference_name:
            venue = conference_name
    
    md += "\nvenue: '" + html_escape(venue) + "'"
    
    if len(str(item.paper_url)) > 5:
        md += "\npaperurl: '" + item.paper_url + "'"
    
    md += "\ncitation: '" + html_escape(item.citation) + "'"
    
    # Add citation count if available
    if hasattr(item, 'citations') and str(item.citations) != 'nan' and str(item.citations) != '':
        md += "\ncitations: " + str(int(float(item.citations)))
    
    # Add publication type - detect it dynamically using corrected venue
    pub_type = detect_publication_type(venue, paper_url)
    md += "\npub_type: '" + pub_type + "'"
    
    md += "\n---"
    
    ## Markdown description for individual page
    
    if len(str(item.paper_url)) > 5:
        md += "\n\n<a href='" + item.paper_url + "'>Download paper here</a>\n" 
    
    # Add citation count display
    if hasattr(item, 'citations') and str(item.citations) != 'nan' and str(item.citations) != '':
        citations = int(float(item.citations))
        if citations > 0:
            md += f"\n**Citations: {citations}**\n"
        
    md += "\nRecommended citation: " + item.citation
    
    md_filename = os.path.basename(md_filename)
       
    with open("../_publications/" + md_filename, 'w') as f:
        f.write(md)


