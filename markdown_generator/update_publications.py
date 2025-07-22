#!/usr/bin/env python3
"""
Google Scholar Publication Updater

This script scrapes publication data from a Google Scholar profile and updates
the publications.tsv file used by the Jekyll site's markdown generator.
"""

import csv
import time
from datetime import datetime
from scholarly import scholarly
import pandas as pd
import os
import re
import json

# Configuration
GOOGLE_SCHOLAR_ID = "28p_eLYAAAAJ"  # Your Google Scholar profile ID
TSV_FILE = "publications.tsv"
BACKUP_FILE = f"publications_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tsv"
VENUE_OVERRIDES_FILE = "venue_overrides.json"

def load_venue_overrides():
    """Load venue overrides from JSON file."""
    if os.path.exists(VENUE_OVERRIDES_FILE):
        try:
            with open(VENUE_OVERRIDES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load venue overrides: {e}")
    return {}

def apply_venue_overrides(title, venue, pub_type, paper_url, citations, overrides):
    """Apply venue overrides if available for this publication."""
    venue_overrides = overrides.get('venue_overrides', {})
    
    # Check for exact title match
    if title in venue_overrides:
        override = venue_overrides[title]
        print(f"Applying venue override for: {title[:50]}...")
        
        # Apply overrides
        if 'venue' in override:
            venue = override['venue']
        if 'pub_type' in override:
            pub_type = override['pub_type']
        if 'paper_url' in override:
            paper_url = override['paper_url']
        if 'citations' in override:
            citations = override['citations']
    
    # Apply global patterns
    global_patterns = overrides.get('global_patterns', {})
    
    # Conference alias mapping
    conference_aliases = global_patterns.get('conference_aliases', {})
    if venue in conference_aliases:
        venue = conference_aliases[venue]
        print(f"Applied conference alias: {venue}")
    
    # Patent venue cleanup
    patent_settings = overrides.get('patent_venue_override', {})
    if (pub_type == 'patent' and 
        patent_settings.get('remove_unknown_venue', False) and 
        venue == 'Unknown Venue'):
        venue = ''
    
    return venue, pub_type, paper_url, citations

def backup_existing_tsv():
    """Create a backup of the existing TSV file."""
    if os.path.exists(TSV_FILE):
        print(f"Creating backup: {BACKUP_FILE}")
        with open(TSV_FILE, 'r') as src, open(BACKUP_FILE, 'w') as dst:
            dst.write(src.read())

def format_date(year):
    """Convert year to YYYY-MM-DD format for Jekyll."""
    if year:
        return f"{year}-01-01"
    return "2023-01-01"  # Default date if year is missing

def create_url_slug(title):
    """Create a URL-friendly slug from the paper title."""
    # Remove special characters and replace spaces with hyphens
    slug = ''.join(c for c in title.lower() if c.isalnum() or c.isspace())
    slug = '-'.join(slug.split())
    return slug[:50]  # Limit length

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

def is_supplementary_material(title, paper_url=''):
    """Check if this is supplementary material that should be excluded."""
    title_lower = title.lower() if title else ''
    url_lower = paper_url.lower() if paper_url else ''
    
    # Check title for supplementary keywords
    supplementary_keywords = [
        'supplementary material',
        'supplemental material', 
        'supplement',
        'supplementary',
        'supplemental',
        'supp material'
    ]
    
    if any(keyword in title_lower for keyword in supplementary_keywords):
        return True
    
    # Check URL for supplementary file patterns
    supplementary_url_patterns = [
        '-supp.pdf',
        '_supplemental.pdf',
        'supplementary.pdf',
        'supplement.pdf'
    ]
    
    if any(pattern in url_lower for pattern in supplementary_url_patterns):
        return True
    
    return False

def extract_enhanced_info(pub):
    """Extract enhanced publication information from available fields."""
    try:
        bib = pub.get('bib', {})
        paper_url = pub.get('pub_url', '')
        
        # Initialize fields with available data
        fields = {}
        for key, value in bib.items():
            fields[key.lower()] = value
            
        # Add additional fields
        fields['url'] = paper_url
        fields['citations'] = pub.get('num_citations', 0)
        
        # Enhanced venue detection using multiple sources
        venue_sources = [
            bib.get('venue', ''),
            bib.get('journal', ''),
            bib.get('booktitle', ''),
            bib.get('publisher', ''),
            bib.get('conference', ''),
        ]
        
        # Try to extract venue from citation string if others fail
        if not any(venue_sources) and 'citation' in pub and pub['citation']:
            citation = pub['citation']
            venue_patterns = [
                r'(?:In )?(?:Proceedings of )?(CVPR|ICCV|ECCV|BMVC|WACV|ACCV)(?:\s+\d{4})?',
                r'(IEEE Transactions on [^,\.]+)',
                r'(Advances in Neural Information Processing Systems)',
                r'(arXiv preprint arXiv:[0-9\.]+)',
                r'In ([^,\.]+),?\s+\d{4}'
            ]
            for pattern in venue_patterns:
                match = re.search(pattern, citation, re.IGNORECASE)
                if match:
                    venue_sources.append(match.group(1).strip())
                    break
        
        # Choose the best venue
        venue = next((v for v in venue_sources if v), 'Unknown Venue')
        fields['venue'] = venue
        
        # Infer entry type from venue and URL patterns
        entry_type = infer_entry_type_from_venue(venue, paper_url, bib)
        
        return entry_type, fields, None
        
    except Exception as e:
        print(f"Warning: Could not extract enhanced info: {e}")
        return None, None, None

def infer_entry_type_from_venue(venue, paper_url='', bib={}):
    """Infer BibTeX entry type from venue and other indicators."""
    venue_lower = venue.lower()
    url_lower = paper_url.lower() if paper_url else ''
    
    # Check for preprints first
    if ('arxiv' in venue_lower or 'preprint' in venue_lower or
        'arxiv.org' in url_lower):
        return 'misc'  # arXiv preprints are typically @misc
    
    # Check for patents
    if ('patent' in venue_lower or 'patents.google.com' in url_lower):
        return 'patent'
    
    # Check for conference proceedings
    conference_indicators = [
        'proceedings', 'conference', 'workshop', 'symposium',
        # Major CV/AI conferences
        'cvpr', 'iccv', 'eccv', 'neurips', 'nips', 'icml', 'iclr',
        'aaai', 'ijcai', 'siggraph', 'bmvc', 'wacv', 'accv',
        # Additional AI/ML conferences  
        'kdd', 'www', 'chi', 'uist', 'icra', 'iros', 'rss',
        'aistats', 'colt', 'uai', 'pkdd', 'icdm', 'sdm',
        # Graphics and vision
        'tog', '3dv', 'iccvw', 'cvprw', 'eccvw',
        # Medical imaging
        'miccai', 'ipmi', 'isbi', 'spie',
        # Robotics
        'icra', 'iros', 'rss', 'humanoids',
        # NLP
        'acl', 'emnlp', 'naacl', 'coling', 'eacl',
        # Theory
        'focs', 'stoc', 'soda', 'icalp'
    ]
    
    if any(indicator in venue_lower for indicator in conference_indicators):
        return 'inproceedings'
    
    # Check for journals
    journal_indicators = [
        'transactions', 'journal', 'ieee', 'acm', 'pami', 'tpami'
    ]
    
    if any(indicator in venue_lower for indicator in journal_indicators):
        return 'article'
    
    # Special case: Springer published conferences
    if ('springer' in venue_lower and 
        any(pattern in url_lower for pattern in ['link.springer.com/chapter', 'eccv', 'iccv', 'accv'])):
        return 'inproceedings'
    
    # Default to inproceedings for computer science publications
    return 'inproceedings'

def categorize_from_bibtex(entry_type, bibtex_fields, paper_url=''):
    """Categorize publication based on BibTeX entry type and fields."""
    if not entry_type:
        return 'conference'  # Default fallback
    
    # Direct mapping from BibTeX entry types
    if entry_type in ['inproceedings', 'conference']:
        return 'conference'
    elif entry_type in ['article']:
        # Check if it's a journal article or preprint
        journal = bibtex_fields.get('journal', '').lower()
        if 'arxiv' in journal or 'preprint' in journal:
            return 'preprint'
        return 'journal'
    elif entry_type in ['misc', 'unpublished']:
        # Check for preprints in misc category
        note = bibtex_fields.get('note', '').lower()
        title = bibtex_fields.get('title', '').lower()
        if 'arxiv' in note or 'preprint' in note or 'arxiv' in title:
            return 'preprint'
        # Check for patents
        if 'patent' in note or 'patent' in title:
            return 'patent'
        return 'preprint'  # Default for misc
    elif entry_type in ['patent']:
        return 'patent'
    elif entry_type in ['book', 'incollection', 'inbook']:
        return 'book'
    elif entry_type in ['phdthesis', 'mastersthesis']:
        return 'thesis'
    elif entry_type in ['techreport']:
        return 'report'
    
    # Fallback to heuristic checking if needed
    return 'conference'

def extract_venue_from_bibtex(entry_type, bibtex_fields, paper_url=''):
    """Extract venue information from BibTeX fields."""
    venue = ''
    
    if entry_type in ['inproceedings', 'conference']:
        # For conferences, prefer booktitle
        venue = bibtex_fields.get('booktitle', '')
        if not venue:
            venue = bibtex_fields.get('organization', '')
        if not venue:
            venue = bibtex_fields.get('publisher', '')
    elif entry_type in ['article']:
        # For articles, prefer journal
        venue = bibtex_fields.get('journal', '')
        if not venue:
            venue = bibtex_fields.get('publisher', '')
    elif entry_type in ['misc', 'unpublished']:
        # For misc, try multiple fields
        venue = bibtex_fields.get('note', '')
        if not venue:
            venue = bibtex_fields.get('publisher', '')
        if not venue:
            venue = bibtex_fields.get('journal', '')
    else:
        # Try all possible venue fields
        for field in ['booktitle', 'journal', 'publisher', 'organization', 'school', 'institution']:
            if bibtex_fields.get(field):
                venue = bibtex_fields.get(field)
                break
    
    # Clean up venue string
    if venue:
        # Remove extra whitespace and clean up
        venue = re.sub(r'\s+', ' ', venue).strip()
        # Remove common prefixes
        venue = re.sub(r'^(Proceedings of the |Proceedings of |In )', '', venue, flags=re.IGNORECASE)
    
    # Apply Springer conference correction if needed
    if ('springer' in venue.lower() and paper_url and 
        'link.springer.com/chapter' in paper_url):
        conference_name = extract_conference_from_springer_url(paper_url)
        if conference_name:
            venue = conference_name
    
    return venue if venue else 'Unknown Venue'

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

def format_citation(pub, venue_override=None):
    """Create a formatted citation string, optionally using BibTeX-derived venue."""
    bib = pub.get('bib', {})
    paper_url = pub.get('pub_url', '')
    
    # Extract authors more carefully
    authors = bib.get('author', '')
    if not authors or authors == 'Unknown Author':
        # Try alternative author field
        authors = pub.get('author', 'Avinash Ravichandran')
    
    title = bib.get('title', 'Unknown Title')
    
    # Use provided venue override if available, otherwise extract venue
    if venue_override:
        venue = venue_override
    else:
        # Extract venue more carefully
        venue = bib.get('venue', '')
        if not venue:
            venue = bib.get('journal', '')
        if not venue:
            venue = bib.get('booktitle', '')
        if not venue:
            venue = bib.get('publisher', '')
        if not venue:
            venue = 'Unknown Venue'
        
        # Fix Springer publisher names with proper conference names
        if ('springer' in venue.lower() and paper_url and 
            'link.springer.com/chapter' in paper_url):
            conference_name = extract_conference_from_springer_url(paper_url)
            if conference_name:
                venue = conference_name
    
    year = bib.get('pub_year', bib.get('year', 'Unknown Year'))
    
    # Format authors - if multiple, use "First Author et al."
    if authors and ',' in authors:
        first_author = authors.split(',')[0].strip()
        authors_formatted = f"{first_author} et al."
    else:
        authors_formatted = authors if authors else 'Avinash Ravichandran'
    
    return f'{authors_formatted} ({year}). "{title}" <i>{venue}</i>.'

def extract_paper_url(pub):
    """Extract the best available URL for the paper."""
    # Try to get the canonical URL first, then fall back to pub_url
    if 'pub_url' in pub:
        return pub['pub_url']
    elif 'eprint_url' in pub:
        return pub['eprint_url']
    else:
        return ""

def scrape_google_scholar():
    """Scrape publications from Google Scholar profile."""
    print(f"Fetching publications for Google Scholar ID: {GOOGLE_SCHOLAR_ID}")
    
    # Load venue overrides
    venue_overrides = load_venue_overrides()
    if venue_overrides:
        print(f"Loaded venue overrides from {VENUE_OVERRIDES_FILE}")
    
    try:
        # Search for the author by ID
        author = scholarly.search_author_id(GOOGLE_SCHOLAR_ID)
        print("Found author profile, filling details...")
        author = scholarly.fill(author)
        
        publications = []
        
        print(f"Found {len(author['publications'])} publications")
        
        # Process all publications
        pub_list = author['publications']
        
        for i, pub in enumerate(pub_list):
            print(f"Processing publication {i+1}/{len(pub_list)}: {pub.get('bib', {}).get('title', 'Unknown')[:50]}...")
            
            try:
                # Fill publication details to get complete information
                pub_filled = scholarly.fill(pub)
                time.sleep(1)  # Be respectful to Google Scholar
            except Exception as e:
                print(f"Warning: Could not fetch full details for publication {i+1}, using basic data: {e}")
                pub_filled = pub
            
            # Extract publication data using BibTeX when possible
            bib = pub_filled.get('bib', {})
            paper_url = extract_paper_url(pub_filled)
            title = bib.get('title', 'Unknown Title')
            
            # Skip supplementary material
            if is_supplementary_material(title, paper_url):
                print(f"Skipping supplementary material: {title[:50]}...")
                continue
            
            # Skip malformed entries
            if title.lower() in ['abstract popular', 'abstract', 'popular']:
                print(f"Skipping malformed entry: {title[:50]}...")
                continue
            
            # Try enhanced info extraction first
            entry_type, enhanced_fields, _ = extract_enhanced_info(pub_filled)
            
            if entry_type and enhanced_fields:
                print(f"Using enhanced data for: {title[:50]}... (type: {entry_type})")
                # Use BibTeX-style categorization
                pub_type = categorize_from_bibtex(entry_type, enhanced_fields, paper_url)
                venue = enhanced_fields.get('venue', 'Unknown Venue')
                
                # Apply Springer conference correction if needed
                if ('springer' in venue.lower() and paper_url and 
                    'link.springer.com/chapter' in paper_url):
                    conference_name = extract_conference_from_springer_url(paper_url)
                    if conference_name:
                        venue = conference_name
                
                year = enhanced_fields.get('year', enhanced_fields.get('pub_year', bib.get('pub_year', bib.get('year', ''))))
            else:
                print(f"Fallback to heuristic for: {title[:50]}...")
                # Fallback to original venue extraction logic
                venue = ''
                
                # Try multiple venue fields from bib
                if bib.get('venue'):
                    venue = bib.get('venue')
                elif bib.get('journal'):
                    venue = bib.get('journal')
                elif bib.get('booktitle'):
                    venue = bib.get('booktitle')
                elif bib.get('publisher'):
                    venue = bib.get('publisher')
                elif bib.get('conference'):
                    venue = bib.get('conference')
                elif 'citation' in pub_filled and pub_filled['citation']:
                    # Try to extract venue from citation string
                    citation = pub_filled['citation']
                    venue_patterns = [
                        r'(?:In )?(?:Proceedings of )?([A-Z]{3,8}(?:\s+\d{4})?)',  # CVPR, ICCV, etc
                        r'(IEEE Transactions on [^,\.]+)',
                        r'(Advances in Neural Information Processing Systems)',
                        r'(arXiv preprint arXiv:[0-9\.]+)',
                        r'In ([^,\.]+),?\s+\d{4}'
                    ]
                    for pattern in venue_patterns:
                        match = re.search(pattern, citation, re.IGNORECASE)
                        if match:
                            venue = match.group(1).strip()
                            break
                
                if not venue:
                    venue = 'Unknown Venue'
                
                # Fix Springer publisher names with proper conference names
                if ('springer' in venue.lower() and paper_url and 
                    'link.springer.com/chapter' in paper_url):
                    conference_name = extract_conference_from_springer_url(paper_url)
                    if conference_name:
                        venue = conference_name
                
                year = bib.get('pub_year', bib.get('year', ''))
                # Fallback to heuristic publication type detection
                pub_type = detect_publication_type(venue, paper_url)
            
            # Get citation count
            citations = pub_filled.get('num_citations', 0)
            
            # Apply venue overrides (this ensures manual corrections persist)
            venue, pub_type, paper_url, citations = apply_venue_overrides(
                title, venue, pub_type, paper_url, citations, venue_overrides
            )
            
            pub_data = {
                'pub_date': format_date(year),
                'title': title,
                'venue': venue,
                'excerpt': '',  # Remove abstracts from display
                'citation': format_citation(pub_filled, venue),
                'url_slug': create_url_slug(title),
                'paper_url': paper_url,
                'citations': citations,
                'pub_type': pub_type
            }
            
            publications.append(pub_data)
        
        # Sort by publication date (newest first)
        publications.sort(key=lambda x: x['pub_date'], reverse=True)
        
        return publications
        
    except Exception as e:
        print(f"Error scraping Google Scholar: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_validation_report(publications):
    """Generate a validation report showing potential issues."""
    print("\n" + "="*50)
    print("VALIDATION REPORT")
    print("="*50)
    
    unknown_venues = []
    potential_misclassifications = []
    
    for pub in publications:
        title = pub['title']
        venue = pub['venue']
        pub_type = pub['pub_type']
        
        # Check for unknown venues
        if venue in ['Unknown Venue', '', 'IEEE', 'Springer Berlin Heidelberg']:
            unknown_venues.append({
                'title': title[:60] + ('...' if len(title) > 60 else ''),
                'venue': venue,
                'type': pub_type,
                'url': pub.get('paper_url', '')
            })
        
        # Check for potential misclassifications
        if venue and pub_type:
            # Journal in conference or vice versa
            if ('transactions' in venue.lower() or 'journal' in venue.lower()) and pub_type == 'conference':
                potential_misclassifications.append({
                    'title': title[:60] + ('...' if len(title) > 60 else ''),
                    'issue': f'Journal venue "{venue}" classified as conference',
                    'venue': venue,
                    'type': pub_type
                })
            elif ('proceedings' in venue.lower() or any(conf in venue.lower() 
                  for conf in ['cvpr', 'iccv', 'eccv', 'neurips', 'iclr'])) and pub_type == 'journal':
                potential_misclassifications.append({
                    'title': title[:60] + ('...' if len(title) > 60 else ''),
                    'issue': f'Conference venue "{venue}" classified as journal',
                    'venue': venue,
                    'type': pub_type
                })
    
    # Report unknown venues
    if unknown_venues:
        print(f"\n⚠️  UNKNOWN/GENERIC VENUES ({len(unknown_venues)} found):")
        print("-" * 50)
        for i, pub in enumerate(unknown_venues[:10]):  # Show first 10
            print(f"{i+1:2d}. {pub['title']}")
            print(f"    Venue: '{pub['venue']}' | Type: {pub['type']}")
            if pub['url']:
                print(f"    URL: {pub['url']}")
            print()
        if len(unknown_venues) > 10:
            print(f"    ... and {len(unknown_venues) - 10} more")
    
    # Report potential misclassifications
    if potential_misclassifications:
        print(f"\n🔍 POTENTIAL MISCLASSIFICATIONS ({len(potential_misclassifications)} found):")
        print("-" * 50)
        for i, issue in enumerate(potential_misclassifications):
            print(f"{i+1:2d}. {issue['title']}")
            print(f"    Issue: {issue['issue']}")
            print()
    
    # Summary
    total_issues = len(unknown_venues) + len(potential_misclassifications)
    if total_issues == 0:
        print("\n✅ No validation issues found!")
    else:
        print(f"\n📊 SUMMARY: {total_issues} issues found")
        print(f"   - {len(unknown_venues)} unknown/generic venues")
        print(f"   - {len(potential_misclassifications)} potential misclassifications")
        print("\n💡 Consider adding these to venue_overrides.json for future runs")
    
    print("="*50)

def update_tsv_file(publications):
    """Update the TSV file with new publication data."""
    if not publications:
        print("No publications to update")
        return
    
    # Generate validation report
    generate_validation_report(publications)
    
    # Create DataFrame
    df = pd.DataFrame(publications)
    
    # Ensure all required columns are present
    required_columns = ['pub_date', 'title', 'venue', 'excerpt', 'citation', 'url_slug', 'paper_url', 'citations', 'pub_type']
    for col in required_columns:
        if col not in df.columns:
            df[col] = ''
    
    # Reorder columns to match expected format
    df = df[required_columns]
    
    # Save to TSV
    df.to_csv(TSV_FILE, sep='\t', index=False)
    print(f"Updated {TSV_FILE} with {len(publications)} publications")

def main():
    """Main function to update publications from Google Scholar."""
    print("Google Scholar Publication Updater")
    print("=" * 40)
    
    # Create backup
    backup_existing_tsv()
    
    # Scrape publications
    publications = scrape_google_scholar()
    
    if publications:
        # Update TSV file
        update_tsv_file(publications)
        
        print("\nUpdate completed successfully!")
        print(f"Next steps:")
        print(f"1. Review the updated {TSV_FILE}")
        print(f"2. Run: uv run python publications.py")
        print(f"3. Check the generated files in ../_publications/")
    else:
        print("Failed to update publications")

if __name__ == "__main__":
    main()