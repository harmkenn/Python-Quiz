"""
Consolidated Italian Language Dataset
Combines data from '1000 Words.csv' and 'italian_set.py'
Total entries: 1737 (1169 from CSV + 568 unique from italian_set.py)

This module provides three ways to access the data:
1. english_to_italian: Dict for English -> Italiano lookup
2. italian_to_english: Dict for Italiano -> English lookup
3. full_data: List of dicts with complete metadata (English, Italiano, Part of Speech, Source)
"""

import pandas as pd
from pathlib import Path

# Lazy-load from consolidated CSV
_csv_loaded = False
_df = None
_english_to_italian = {}
_italian_to_english = {}
_full_data = []


def _load_data():
    """Load data from consolidated CSV on first access."""
    global _csv_loaded, _df, _english_to_italian, _italian_to_english, _full_data
    
    if _csv_loaded:
        return
    
    csv_path = Path(__file__).parent / "Consolidated_Italian_Dataset.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")
    
    _df = pd.read_csv(csv_path)
    
    # Build English -> Italiano mapping
    for _, row in _df.iterrows():
        eng = str(row['English']).strip()
        ita = str(row['Italiano']).strip()
        if eng and eng not in _english_to_italian:
            _english_to_italian[eng] = ita
    
    # Build Italiano -> English mapping
    for _, row in _df.iterrows():
        ita = str(row['Italiano']).strip()
        eng = str(row['English']).strip()
        if ita and ita not in _italian_to_english:
            _italian_to_english[ita] = eng
    
    # Build full data list
    for _, row in _df.iterrows():
        _full_data.append({
            'english': str(row['English']).strip(),
            'italiano': str(row['Italiano']).strip(),
            'part_of_speech': str(row['Part']).strip(),
            'source': str(row['Source']).strip()
        })
    
    _csv_loaded = True


def get_english_to_italian():
    """Get English -> Italiano dictionary. Lazy-loads on first call."""
    _load_data()
    return _english_to_italian.copy()


def get_italian_to_english():
    """Get Italiano -> English dictionary. Lazy-loads on first call."""
    _load_data()
    return _italian_to_english.copy()


def get_full_data():
    """Get full dataset as list of dicts with metadata. Lazy-loads on first call."""
    _load_data()
    return _full_data.copy()


def translate_english(english_word):
    """Translate a single English word to Italian. Returns None if not found."""
    _load_data()
    return _english_to_italian.get(english_word.strip().lower())


def translate_italian(italian_word):
    """Translate a single Italian word to English. Returns None if not found."""
    _load_data()
    return _italian_to_english.get(italian_word.strip())


def get_by_part_of_speech(part):
    """Get all entries for a given part of speech (e.g., 'Noun', 'Verb')."""
    _load_data()
    return [entry for entry in _full_data if entry['part_of_speech'].lower() == part.lower()]


def search_english(query):
    """Search for entries containing query string in English (case-insensitive)."""
    _load_data()
    query_lower = query.lower()
    return [entry for entry in _full_data if query_lower in entry['english'].lower()]


def search_italian(query):
    """Search for entries containing query string in Italian."""
    _load_data()
    return [entry for entry in _full_data if query in entry['italiano']]


def get_statistics():
    """Return dataset statistics."""
    _load_data()
    parts = {}
    sources = {}
    for entry in _full_data:
        part = entry['part_of_speech']
        source = entry['source']
        parts[part] = parts.get(part, 0) + 1
        sources[source] = sources.get(source, 0) + 1
    
    return {
        'total_entries': len(_full_data),
        'unique_english': len(_english_to_italian),
        'unique_italian': len(_italian_to_english),
        'parts_of_speech': parts,
        'sources': sources
    }


# Eager-load for backward compatibility (optional, lazy-load only if needed)
# Uncomment to always load on import:
# _load_data()
# english_to_italian = _english_to_italian
# italian_to_english = _italian_to_english
# full_data = _full_data

__all__ = [
    'get_english_to_italian',
    'get_italian_to_english',
    'get_full_data',
    'translate_english',
    'translate_italian',
    'get_by_part_of_speech',
    'search_english',
    'search_italian',
    'get_statistics',
]
