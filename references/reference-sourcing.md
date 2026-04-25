# Reference Sourcing

Gather references before you write the final prompt.

## Search order

Use web search with queries like:

- `<character name> <series> official art`
- `<character name> <series> anime official`
- `<character name> <series> promotional art`
- `<character name> <series> character page`
- `<character name> <series> anime screenshot`

## Priority

1. user-provided references
2. official anime or game website
3. publisher, distributor, or franchise promo pages
4. trusted character pages that embed official art or anime screenshots

## Exclusions

Do not default to:
- fanart
- booru sites
- Pinterest
- social reposts
- scraper pages with no official source link

## Minimum pack

Try to gather `3-5` images that cover:
- `face`
- `full-body`
- `outfit-color`
- `prop-accessory`
- `anime-lighting` or `scene`

## Saving convention

Use a folder like:

```text
refs/<character-slug>/
```

Suggested filenames:
- `01-face.*`
- `02-fullbody.*`
- `03-outfit.*`
- `04-prop.*`
- `05-scene.*`

Write a small JSON manifest with:
- file name
- role
- source URL
- page URL
- note about why the image was kept

## User references

If the user provides references:
- treat them as the top-priority version definition
- do not let supplemental web images override that version
- only use web images to fill missing information
