"""
Team Name Canonicalization for F1 Data Pipeline

Handles F1 team name variations across different data sources and years.
Maps all variations to canonical team identifiers for consistent analysis.

Key Features:
- Handles team rebranding (AlphaTauri → RB, Alfa Romeo → Sauber)
- Maps sponsor name changes to core team identity
- Tracks institutional continuity for causal inference (SCM donor pool)
- Provides safe fallback for unknown teams
- Logs unknown team names for manual review

Example:
    >>> from src.team_name_mapping import canonicalize_team, normalize_team_column
    >>> canonicalize_team('Visa Cash App RB')
    'RB'
    >>> df = normalize_team_column(df, col='team')

Author: Tomasz Solis
Date: November 2025
Updated: November 2025 (added historical teams for SCM analysis)
"""

import pandas as pd
import logging
from typing import Union

logger = logging.getLogger(__name__)


# =============================================================================
# TEAM NAME MAPPING
# =============================================================================

TEAM_NAME_MAP = {
    # Sauber lineage (Sauber → Alfa Romeo → Kick Sauber → Audi)
    # Institutional continuity: YES (same team, different sponsors)
    'Sauber': 'SAUBER',
    'Alfa Romeo': 'SAUBER',
    'Kick Sauber': 'SAUBER',
    'Stake F1 Team Kick Sauber': 'SAUBER',
    'Kick Sauber F1 Team': 'SAUBER',
    
    # AlphaTauri lineage (Toro Rosso → AlphaTauri → RB → Racing Bulls)
    # Institutional continuity: YES (Red Bull's B-team throughout)
    'Toro Rosso': 'RB',
    'AlphaTauri': 'RB',
    'Scuderia AlphaTauri': 'RB',
    'Visa Cash App RB': 'RB',
    'VCARB': 'RB',
    'Racing Bulls': 'RB',
    'RB F1 Team': 'RB',
    'RB': 'RB',

    # Red Bull Racing (stable identity)
    # Institutional continuity: YES
    'Red Bull Racing': 'RED BULL',
    'Oracle Red Bull Racing': 'RED BULL',
    'Red Bull': 'RED BULL',

    # Mercedes (stable identity)
    # Institutional continuity: YES
    'Mercedes': 'MERCEDES',
    'Mercedes-AMG Petronas F1 Team': 'MERCEDES',

    # Ferrari (stable identity)
    # Institutional continuity: YES
    'Ferrari': 'FERRARI',
    'Scuderia Ferrari': 'FERRARI',

    # Aston Martin lineage (Force India → Racing Point → Aston Martin)
    # Institutional continuity: PARTIAL (major ownership change 2018, 2020)
    # Note: Force India went into administration 2018, became Racing Point
    # Then Lawrence Stroll investment 2020 → Aston Martin
    'Force India': 'ASTON MARTIN',
    'Racing Point': 'ASTON MARTIN',
    'SportPesa Racing Point': 'ASTON MARTIN',
    'BWT Racing Point': 'ASTON MARTIN',
    'Aston Martin': 'ASTON MARTIN',
    'Aston Martin Aramco': 'ASTON MARTIN',

    # Alpine lineage (Renault → Alpine)
    # Institutional continuity: YES (same team, rebrand only)
    'Lotus F1': 'ALPINE',
    'Renault': 'ALPINE',
    'Renault F1': 'ALPINE',
    'Renault F1 Team': 'ALPINE',
    'Alpine': 'ALPINE',
    'Alpine F1 Team': 'ALPINE',
    'BWT Alpine F1 Team': 'ALPINE',

    # McLaren (stable identity)
    # Institutional continuity: YES
    'McLaren': 'MCLAREN',
    'McLaren F1 Team': 'MCLAREN',

    # Haas (stable identity, entered 2016)
    # Institutional continuity: YES
    'Haas': 'HAAS',
    'Haas F1 Team': 'HAAS',
    'MoneyGram Haas F1 Team': 'HAAS',

    # Williams (stable identity)
    # Institutional continuity: PARTIAL (Dorilton Capital takeover 2020)
    'Williams': 'WILLIAMS',
    'Williams Racing': 'WILLIAMS',
    
    # Historical teams (2014-2016, now defunct)
    # These will be excluded from donor pools due to discontinuity
    'Marussia': 'MANOR MARUSSIA',  # Defunct 2015
    'Manor Marussia': 'MANOR MARUSSIA',  # Successor to Marussia, defunct 2017
    'Caterham': 'CATERHAM',  # Defunct 2014
}


# =============================================================================
# INSTITUTIONAL CONTINUITY METADATA (FOR SCM ANALYSIS)
# =============================================================================

# Teams with stable institutional continuity 2017-2024
# (safe to use in donor pools for SCM)
STABLE_TEAMS = {
    'RED BULL',      # Stable ownership/structure
    'MERCEDES',      # Stable ownership/structure
    'FERRARI',       # Stable ownership/structure
    'MCLAREN',       # Stable ownership/structure
    'SAUBER',        # Stable core team despite sponsor changes
    'RB',            # Stable as Red Bull's B-team
    'ALPINE',        # Stable (Renault rebrand, same team)
    'HAAS',          # Stable since 2016 entry
}

# Teams with major ownership/structural changes
# (use with caution in donor pools - may have confounding shocks)
UNSTABLE_TEAMS = {
    'ASTON MARTIN': {
        'shock_years': [2018, 2020],
        'description': '2018: Force India administration; 2020: Stroll investment'
    },
    'WILLIAMS': {
        'shock_years': [2020],
        'description': '2020: Dorilton Capital takeover'
    },
    'ALPINE': {
        'shock_years': [2015],
        'description': '2015: Became Renault from Lotus F1 (ownership change)'
    }
    }

# Defunct teams (exclude from analysis after their exit year)
DEFUNCT_TEAMS = {
    'MARUSSIA': 2014,   # Collapsed
    'MANOR': 2016,      # Collapsed
    'CATERHAM': 2014,   # Collapsed
}


# =============================================================================
# CANONICALIZATION FUNCTIONS
# =============================================================================

def canonicalize_team(name: str) -> str:
    """
    Map raw team name to canonical identifier.
    
    Handles team name variations from FastF1 API, historical data,
    and sponsor changes. Falls back to uppercase original if unknown.
    
    Args:
        name: Raw team name string (e.g., "Visa Cash App RB")
        
    Returns:
        Canonical team identifier (e.g., "RB")
        
    Example:
        >>> canonicalize_team('Oracle Red Bull Racing')
        'RED BULL'
        >>> canonicalize_team('Unknown Team')
        'UNKNOWN TEAM'
    """
    if name is None:
        return None
    
    return TEAM_NAME_MAP.get(name, str(name).upper())


def normalize_team_column(
    df: Union[pd.DataFrame, pd.Series],
    col: str = "team"
) -> pd.DataFrame:
    """
    Normalize team names in DataFrame using canonical mapping.
    
    Applies canonicalize_team() to specified column, logging any
    unknown team names for manual review. Handles edge cases safely.
    
    Safety Features:
    - Auto-converts Series to DataFrame if needed
    - Returns unchanged if column doesn't exist
    - Logs unknown teams for monitoring
    
    Args:
        df: DataFrame or Series containing team names
        col: Name of team column (default: "team")
        
    Returns:
        DataFrame with normalized team names
        
    Raises:
        None - handles all errors gracefully
        
    Example:
        >>> df = normalize_team_column(df, col='team')
        >>> df['team'].unique()
        array(['RED BULL', 'FERRARI', 'MERCEDES', ...])
    """
    # Handle Series input (convert to DataFrame)
    if isinstance(df, pd.Series):
        logger.warning(
            "normalize_team_column() called on Series instead of DataFrame. "
            "Auto-converting to DataFrame."
        )
        df = df.to_frame(name=col)
    
    # Handle missing column (return unchanged)
    if col not in df.columns:
        return df
    
    # Apply canonicalization
    raw_names = df[col].astype(str)
    canonical_names = raw_names.apply(canonicalize_team)
    
    # Detect and log unknown teams (those using fallback uppercase)
    unknown_mask = (
        ~raw_names.isin(TEAM_NAME_MAP.keys()) & 
        (canonical_names == raw_names.str.upper())
    )
    
    if unknown_mask.any():
        unknown_teams = sorted(raw_names[unknown_mask].unique())
        logger.warning(
            "Unknown team names encountered (using uppercase fallback): %s",
            unknown_teams
        )
    
    df[col] = canonical_names
    
    return df


# =============================================================================
# SCM-SPECIFIC HELPER FUNCTIONS
# =============================================================================

def get_stable_teams_for_scm(
    start_year: int = 2017,
    end_year: int = 2024,
    exclude_top3: bool = True
) -> list:
    """
    Get list of teams with stable institutional continuity for SCM donor pools.
    
    Returns teams that can safely be used in synthetic control analysis,
    excluding teams with major ownership changes or defunct teams.
    
    Args:
        start_year: First year of analysis period
        end_year: Last year of analysis period
        exclude_top3: If True, exclude Mercedes/Red Bull/Ferrari (default: True)
        
    Returns:
        List of canonical team names safe for SCM analysis
        
    Example:
        >>> get_stable_teams_for_scm(2017, 2024, exclude_top3=True)
        ['MCLAREN', 'SAUBER', 'RB', 'ALPINE', 'HAAS']
    """
    stable = STABLE_TEAMS.copy()
    
    # Exclude top 3 if requested (they're treated by the cost cap)
    if exclude_top3:
        stable = stable - {'RED BULL', 'MERCEDES', 'FERRARI'}
    
    # Filter by year (e.g., Haas only exists 2016+)
    if start_year >= 2016:
        return sorted(list(stable))
    else:
        # If analysis includes pre-2016, exclude Haas
        return sorted(list(stable - {'HAAS'}))


def check_team_stability(team: str, year: int) -> dict:
    """
    Check if a team had any institutional shocks in a given year.
    
    Useful for validating SCM assumptions about donor pool stability.
    
    Args:
        team: Canonical team name
        year: Year to check
        
    Returns:
        Dict with 'stable' (bool) and 'reason' (str) keys
        
    Example:
        >>> check_team_stability('WILLIAMS', 2020)
        {'stable': False, 'reason': '2020: Dorilton Capital takeover'}
        >>> check_team_stability('MCLAREN', 2020)
        {'stable': True, 'reason': 'No institutional shocks'}
    """
    if team in DEFUNCT_TEAMS:
        exit_year = DEFUNCT_TEAMS[team]
        if year >= exit_year:
            return {
                'stable': False,
                'reason': f'Team defunct after {exit_year}'
            }
    
    if team in UNSTABLE_TEAMS:
        shock_info = UNSTABLE_TEAMS[team]
        if year in shock_info['shock_years']:
            return {
                'stable': False,
                'reason': shock_info['description']
            }
    
    return {
        'stable': True,
        'reason': 'No institutional shocks'
    }


def filter_scm_data(
    df: pd.DataFrame,
    treatment_year: int = 2022,
    include_teams: list = None,
    exclude_teams: list = None
) -> pd.DataFrame:
    """
    Filter F1 data for SCM analysis, removing unstable/defunct teams.
    
    Applies institutional continuity filters to ensure clean donor pools.
    
    Args:
        df: DataFrame with normalized team names
        treatment_year: Year treatment begins (default: 2022 for cost cap)
        include_teams: If provided, only keep these teams
        exclude_teams: Teams to explicitly exclude
        
    Returns:
        Filtered DataFrame safe for SCM analysis
        
    Example:
        >>> df_clean = filter_scm_data(
        ...     df, 
        ...     treatment_year=2022,
        ...     exclude_teams=['WILLIAMS', 'ASTON MARTIN']
        ... )
    """
    df = df.copy()
    
    # Remove defunct teams
    for team, exit_year in DEFUNCT_TEAMS.items():
        df = df[~((df['team'] == team) & (df['year'] >= exit_year))]
    
    # Apply include filter if provided
    if include_teams is not None:
        df = df[df['team'].isin(include_teams)]
    
    # Apply exclude filter if provided
    if exclude_teams is not None:
        df = df[~df['team'].isin(exclude_teams)]
    
    return df