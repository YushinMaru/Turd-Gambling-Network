"""
AI Verification Module - URL scraping and claim verification
"""

import logging
import re
import asyncio
from typing import Optional, Dict, Tuple

logger = logging.getLogger(__name__)

# Cache for scraped URLs to avoid rate limits
_url_cache: Dict[str, Tuple[str, float]] = {}
CACHE_DURATION = 300  # 5 minutes


async def scrape_url(url: str) -> Optional[str]:
    """
    Scrape content from a URL.
    Returns the text content or None if failed.
    """
    import requests
    
    # Check cache first
    if url in _url_cache:
        cached_content, cached_time = _url_cache[url]
        if asyncio.get_event_loop().time() - cached_time < CACHE_DURATION:
            logger.info(f"[VERIFICATION] Using cached content for {url}")
            return cached_content
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Cache the content
            _url_cache[url] = (response.text, asyncio.get_event_loop().time())
            logger.info(f"[VERIFICATION] Successfully scraped {url}")
            return response.text
        else:
            logger.warning(f"[VERIFICATION] Failed to scrape {url}: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        logger.error(f"[VERIFICATION] Error scraping {url}: {e}")
        return None


def verify_claim(content: str, claim: str) -> Tuple[str, str]:
    """
    Verify a claim against scraped content.
    
    Supported formats:
    - Numeric comparisons: > 100, < 500, >= 50, <= 1000, == 100, != 200
    - Text contains: contains "Winner", contains Winner
    
    Returns: (result, explanation)
    - result: "WIN_A", "WIN_B", "UNCLEAR"
    - explanation: Human-readable explanation
    """
    if not content or not claim:
        return "UNCLEAR", "Missing content or claim"
    
    content_lower = content.lower()
    claim_lower = claim.lower().strip()
    
    # Check for numeric comparisons
    numeric_match = re.match(r'([<>=!]+)\s*(\d+(?:\.\d+)?)', claim_lower)
    if numeric_match:
        operator = numeric_match.group(1)
        target_value = float(numeric_match.group(2))
        
        # Try to find numbers in the content
        numbers = re.findall(r'(\d+(?:\.\d+)?)', content)
        
        if not numbers:
            return "UNCLEAR", "No numbers found in content"
        
        # Check if any number matches the condition
        found_match = False
        for num_str in numbers:
            num = float(num_str)
            
            if operator == '>':
                found_match = num > target_value
            elif operator == '<':
                found_match = num < target_value
            elif operator == '>=':
                found_match = num >= target_value
            elif operator == '<=':
                found_match = num <= target_value
            elif operator == '==':
                found_match = num == target_value
            elif operator == '!=':
                found_match = num != target_value
            
            if found_match:
                break
        
        if found_match:
            return "WIN_A", f"Found {operator} {target_value} in content"
        else:
            return "WIN_B", f"Did not find {operator} {target_value} in content"
    
    # Check for "contains" pattern
    if 'contains' in claim_lower:
        # Extract the text to search for
        text_match = re.search(r'contains\s+["\']?(.+?)["\']?\s*$', claim_lower)
        if text_match:
            search_text = text_match.group(1).strip('"\'')
            if search_text in content_lower:
                return "WIN_A", f'Found "{search_text}" in content'
            else:
                return "WIN_B", f'Did not find "{search_text}" in content'
    
    # Check for simple text match
    if claim_lower in content_lower:
        return "WIN_A", f'Found "{claim_lower}" in content'
    
    return "UNCLEAR", "Could not verify claim - try using format like '> 100' or 'contains Winner'"


async def verify_bet(bet_id: str, verification_url: str, verification_claim: str, db) -> Tuple[bool, str]:
    """
    Verify a bet using AI verification.
    
    Returns: (success, result_message)
    """
    logger.info(f"[VERIFICATION] Starting verification for bet {bet_id}")
    logger.info(f"[VERIFICATION] URL: {verification_url}")
    logger.info(f"[VERIFICATION] Claim: {verification_claim}")
    
    # Scrape the URL
    content = await scrape_url(verification_url)
    
    if not content:
        return False, "Failed to scrape URL. Please check the URL and try again."
    
    # Verify the claim
    result, explanation = verify_claim(content, verification_claim)
    
    logger.info(f"[VERIFICATION] Result for {bet_id}: {result} - {explanation}")
    
    if result == "UNCLEAR":
        return False, f"Could not verify: {explanation}"
    
    # Return the result for the caller to resolve
    return True, f"{result}|{explanation}"


def clear_cache():
    """Clear the URL cache"""
    global _url_cache
    _url_cache.clear()
    logger.info("[VERIFICATION] Cache cleared")


def compare_predictions(prediction_a: str, prediction_b: str, actual: str) -> Tuple[str, str]:
    """
    Compare predictions against actual result.
    
    Returns: (result, explanation)
    - result: "WIN_A", "WIN_B", "TIE", "UNCLEAR"
    - explanation: Human-readable explanation
    """
    if not prediction_a or not prediction_b or not actual:
        return "UNCLEAR", "Missing prediction or actual result"
    
    # Try numeric comparison first
    try:
        pred_a_num = float(prediction_a)
        pred_b_num = float(prediction_b)
        actual_num = float(actual)
        
        # Calculate distances
        dist_a = abs(pred_a_num - actual_num)
        dist_b = abs(pred_b_num - actual_num)
        
        if dist_a < dist_b:
            return "WIN_A", f"Prediction A ({pred_a_num}) is closer to actual ({actual_num})"
        elif dist_b < dist_a:
            return "WIN_B", f"Prediction B ({pred_b_num}) is closer to actual ({actual_num})"
        else:
            return "TIE", f"Both predictions are equally close to actual ({actual_num})"
    
    except ValueError:
        # Not numeric - do text comparison
        actual_lower = actual.lower()
        pred_a_lower = prediction_a.lower()
        pred_b_lower = prediction_b.lower()
        
        a_matches = pred_a_lower == actual_lower
        b_matches = pred_b_lower == actual_lower
        
        if a_matches and b_matches:
            return "TIE", "Both predictions match exactly"
        elif a_matches:
            return "WIN_A", f"Prediction A matches: '{prediction_a}'"
        elif b_matches:
            return "WIN_B", f"Prediction B matches: '{prediction_b}'"
        else:
            return "UNCLEAR", f"Neither prediction matches. Actual: '{actual}'"


async def verify_prediction(bet_id: str, db) -> Tuple[bool, str]:
    """
    Verify a bet using prediction comparison.
    
    Returns: (success, result_message)
    """
    logger.info(f"[PREDICTION] Starting prediction verification for bet {bet_id}")
    
    # Get bet data
    conn = db.get_connection()
    c = conn.cursor()
    c.execute('''SELECT prediction_a, prediction_b, prediction_actual FROM bets WHERE bet_id = ?''', (bet_id,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        return False, "Bet not found"
    
    prediction_a, prediction_b, actual = row
    
    if not prediction_a or not prediction_b:
        return False, "Predictions not yet entered by both parties"
    
    if not actual:
        return False, "Actual result not yet set"
    
    # Compare predictions
    result, explanation = compare_predictions(prediction_a, prediction_b, actual)
    
    logger.info(f"[PREDICTION] Result for {bet_id}: {result} - {explanation}")
    
    if result == "UNCLEAR":
        return False, f"Could not verify: {explanation}"
    
    if result == "TIE":
        return False, f"Tie result: {explanation}"
    
    # Return result for resolution
    return True, f"{result}|{explanation}"
