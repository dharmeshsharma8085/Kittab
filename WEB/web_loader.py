import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


# ============================================================
# CONFIGURATION
# ============================================================

REQUEST_TIMEOUT = 20

# Maximum amount of text Kittab will extract
MAX_TEXT_CHARACTERS = 50_000

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}


# ============================================================
# URL VALIDATION
# ============================================================

def validate_url(
    url: str
) -> str:
    """
    Validate and normalize a website URL.
    """

    if not url:
        raise ValueError(
            "Website URL cannot be empty."
        )

    url = url.strip()

    # Add HTTPS if protocol is missing
    if not url.startswith(
        ("http://", "https://")
    ):
        url = "https://" + url

    parsed = urlparse(
        url
    )

    if not parsed.netloc:
        raise ValueError(
            "Invalid website URL."
        )

    return url


# ============================================================
# FETCH HTML
# ============================================================

def fetch_html(
    url: str
) -> str:
    """
    Download webpage HTML.
    """

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

    except requests.Timeout as exc:

        raise RuntimeError(
            "Website request timed out."
        ) from exc

    except requests.RequestException as exc:

        raise RuntimeError(
            f"Failed to fetch website:\n{exc}"
        ) from exc

    # --------------------------------------------------------
    # Check content type
    # --------------------------------------------------------

    content_type = response.headers.get(
        "Content-Type",
        ""
    ).lower()

    if (
        content_type
        and "text/html" not in content_type
    ):
        raise ValueError(
            "The provided URL does not appear "
            "to contain an HTML webpage.\n"
            f"Content-Type: {content_type}"
        )

    return response.text


# ============================================================
# CLEAN HTML
# ============================================================

def clean_html(
    html: str
) -> tuple[str, str]:
    """
    Extract title and readable text from HTML.
    """

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # --------------------------------------------------------
    # Remove unwanted HTML elements
    # --------------------------------------------------------

    unwanted_tags = [
        "script",
        "style",
        "noscript",
        "iframe",
        "svg",
        "canvas",
        "nav",
        "footer",
        "form",
        "aside",
        "header"
    ]

    for tag in soup.find_all(
        unwanted_tags
    ):
        tag.decompose()

    # --------------------------------------------------------
    # Extract title
    # --------------------------------------------------------

    title = ""

    if soup.title:

        title = soup.title.get_text(
            strip=True
        )

    # --------------------------------------------------------
    # Find main content
    # --------------------------------------------------------

    main_content = (
        soup.find("article")
        or soup.find("main")
        or soup.body
        or soup
    )

    # --------------------------------------------------------
    # Extract text
    # --------------------------------------------------------

    text = main_content.get_text(
        separator="\n",
        strip=True
    )

    # --------------------------------------------------------
    # Clean individual lines
    # --------------------------------------------------------

    lines = []

    for line in text.splitlines():

        line = re.sub(
            r"\s+",
            " ",
            line
        ).strip()

        if line:
            lines.append(
                line
            )

    text = "\n".join(
        lines
    )

    # --------------------------------------------------------
    # Remove excessive duplicate blank lines
    # --------------------------------------------------------

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    # --------------------------------------------------------
    # Character limit
    # --------------------------------------------------------

    if len(text) > MAX_TEXT_CHARACTERS:

        print(
            "\n⚠️ Website content is very large."
        )

        print(
            f"Maximum allowed: "
            f"{MAX_TEXT_CHARACTERS:,} characters"
        )

        print(
            f"Original size: "
            f"{len(text):,} characters"
        )

        text = text[
            :MAX_TEXT_CHARACTERS
        ]

        print(
            f"Kept: "
            f"{len(text):,} characters"
        )

    return title, text


# ============================================================
# LOAD WEBSITE
# ============================================================

def load_website(
    url: str
) -> dict:
    """
    Load a website and return structured data.

    Returns:

        {
            "url": "...",
            "title": "...",
            "text": "..."
        }
    """

    # --------------------------------------------------------
    # Validate URL
    # --------------------------------------------------------

    url = validate_url(
        url
    )

    print(
        "\nLoading website..."
    )

    print(
        f"URL: {url}"
    )

    # --------------------------------------------------------
    # Fetch HTML
    # --------------------------------------------------------

    html = fetch_html(
        url
    )

    print(
        "HTML downloaded successfully."
    )

    # --------------------------------------------------------
    # Clean HTML
    # --------------------------------------------------------

    title, text = clean_html(
        html
    )

    # --------------------------------------------------------
    # Validate extracted text
    # --------------------------------------------------------

    if not text.strip():

        raise RuntimeError(
            "No readable text found on this webpage."
        )

    # --------------------------------------------------------
    # Success
    # --------------------------------------------------------

    print(
        "\nWebsite loaded successfully."
    )

    print(
        f"Title: {title or 'No title found'}"
    )

    print(
        f"Characters extracted: "
        f"{len(text):,}"
    )

    return {
        "url": url,
        "title": title,
        "text": text
    }


# ============================================================
# EXTRACT TEXT ONLY
# ============================================================

def extract_text_from_url(
    url: str
) -> str:
    """
    Load website and return only clean text.
    """

    result = load_website(
        url
    )

    return result["text"]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\nKITTAB WEBSITE LOADER"
    )

    print(
        "=" * 60
    )

    url = input(
        "Enter website URL: "
    ).strip()

    try:

        result = load_website(
            url
        )

        print(
            "\nWEBSITE INFORMATION"
        )

        print(
            "=" * 60
        )

        print(
            f"Title: "
            f"{result['title'] or 'No title found'}"
        )

        print(
            f"URL: "
            f"{result['url']}"
        )

        print(
            f"Characters: "
            f"{len(result['text']):,}"
        )

        print(
            "\nEXTRACTED TEXT"
        )

        print(
            "=" * 60
        )

        print(
            result["text"][:5000]
        )

        if len(result["text"]) > 5000:

            print(
                "\n... remaining text truncated "
                "for terminal display ..."
            )

    except Exception as exc:

        print(
            "\n❌ ERROR"
        )

        print(
            "=" * 60
        )

        print(
            exc
        )