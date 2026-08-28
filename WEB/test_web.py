from web_loader import load_website


# ============================================================
# WEBSITE LOADER TEST
# ============================================================

print(
    "\nWEBSITE LOADER TEST"
)

print(
    "=" * 60
)


# ============================================================
# GET URL
# ============================================================

url = input(
    "Enter website URL: "
).strip()


# ============================================================
# LOAD WEBSITE
# ============================================================

try:

    result = load_website(
        url
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

    raise SystemExit(1)


# ============================================================
# WEBSITE INFORMATION
# ============================================================

print(
    "\nWEBSITE INFORMATION"
)

print(
    "=" * 60
)

print(
    f"Title: {result['title']}"
)

print(
    f"URL: {result['url']}"
)

print(
    f"Characters: {len(result['text'])}"
)


# ============================================================
# EXTRACTED TEXT
# ============================================================

print(
    "\nEXTRACTED TEXT"
)

print(
    "=" * 60
)

print(
    result["text"][:5000]
)


print(
    "\n"
)

print(
    "Website extraction test completed."
)