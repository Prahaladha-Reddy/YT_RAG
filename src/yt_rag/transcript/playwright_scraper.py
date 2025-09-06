from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import time

def timestamp_to_seconds(timestamp_str: str) -> int:
    time_parts = timestamp_str.split(':')
    if len(time_parts) == 3:  
        hours, minutes, seconds = map(int, time_parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(time_parts) == 2: 
        minutes, seconds = map(int, time_parts)
        return minutes * 60 + seconds
    else:  
        return int(time_parts[0])


def ensure_english_subtitles(page):
    """
    Navigate to settings and select English subtitles if available
    """
    # Open settings
    page.click('button.ytp-settings-button', timeout=5000)
    page.wait_for_selector('.ytp-menuitem', timeout=5000)

    # Find the Subtitles/CC menu item
    subtitles_item = page.query_selector('div.ytp-menuitem-label:has-text("Subtitles/CC")')
    if not subtitles_item:
        print("No subtitles/CC option found (video may not support captions).")
        return False

    # Get parent container of Subtitles/CC
    container = subtitles_item.evaluate_handle('node => node.parentElement')

    # Get text inside .ytp-menuitem-content (current language)
    content_el = container.query_selector('.ytp-menuitem-content')
    content_text = content_el.inner_text() if content_el else ""

    print(f"Content Text on Subtitle item: {content_text}")

    if content_text == "English":
        print("Already English subtitles.")
        return True

    # Not English → click to open submenu
    container.click()
    page.wait_for_selector('.ytp-menuitem', timeout=5000)
    
    # Re-query fresh menu items to avoid previous menu items
    options = page.query_selector_all('.ytp-menuitem')
    for i in range(len(options)):
        opt = page.query_selector(f'.ytp-menuitem:nth-child({i+1})')
        if not opt:
            continue
        text = opt.inner_text()
        if text == "English":
            opt.click(force=True)
            print("Switched to English subtitles.")
            return True
        
    print(f"English subtitles not avaliable.")
    return False


def extract_transcript(video_url: str):
    """
    Uses playwright to automate browser navigation
    and BeautifulSoup to scrape the transcript

    Args:
        video_url (str) - url of youtube video
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(video_url, wait_until="domcontentloaded", timeout=120000)

        # Step 1: Ensure English subtitles
        ensure_english_subtitles(page)

        # Step 2: Click "Show more"
        try:
            page.click('tp-yt-paper-button#expand', timeout=5000)
        except:
            print("No 'Show more' button found.")

        # Step 3: Click "Show transcript"
        try:
            page.click('button:has-text("Show transcript")', timeout=5000)
        except:
            print("Transcript button not found. Maybe this video has no transcript.")
            browser.close()
            return []

        # Step 4: Wait for transcript elements
        page.wait_for_selector('ytd-transcript-segment-renderer', timeout=10000)

        # Step 5: Extract transcript
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")

        transcript_data = []
        for segment in soup.select("ytd-transcript-segment-renderer"):
            timestamp = segment.select_one(".segment-timestamp")
            text = segment.select_one(".segment-text")
            
            if timestamp and text:
                timestamp_str = timestamp.get_text(strip=True)
                
                transcript_data.append({
                    "timestamp": timestamp_str,
                    "seconds": timestamp_to_seconds(timestamp_str),
                    "text": text.get_text(" ", strip=True)
                })

        browser.close()
        return transcript_data


if __name__ == '__main__':
    start_time = time.time()
    video_url = "https://www.youtube.com/watch?v=wn-tTeOmVRE"
    transcript = extract_transcript(video_url)
    end_time = time.time()
    print(f"Transcript extracted in {end_time-start_time:.2f} seconds")

    with open("transcript1.json", "w", encoding="utf-8") as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2)
