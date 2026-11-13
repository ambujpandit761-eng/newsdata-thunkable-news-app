# newsdata-thunkable-news-app

A small Android headline reader made with MIT App Inventor (block-based, no text code). It pulls live headlines from the newsdata.io news API (https://newsdata.io) using App Inventor's `Web` component. You need a free API key to run it.

## What it does

- Category buttons: Top, Technology, Sports, Business, Health
- Scrollable article list; each row shows the title plus the article's `keywords` (when present)
- Tap a row to open the article in the phone's browser
- API key is typed into the app once and kept in `TinyDB`; it is not stored in the project files
- Handles an invalid key (401), rate limiting (429) and empty results with a message instead of a blank list
- If a result carries a `sentiment` value (a paid response field), it is appended to the row; otherwise the row simply shows no sentiment

## A note on the .aia file

An `.aia` is a zip archive, so it is not committed here (this repo is text only). Two ways to get one:

1. **Build it from this repo**
   ```bash
   python3 build_aia.py
   ```
   This writes `dist/NewsDataReader.aia` from the files in `src/`. Import it at https://ai2.appinventor.mit.edu via *Projects > Import project (.aia) from my computer*.
2. **Rebuild by hand** with the Designer layout in `src/` plus `docs/blocks.md`.

The packed project contains the **Designer layout only** (`Screen1.scm`). The blocks (`Screen1.bky`) are not included, so after importing you add them following `docs/blocks.md`, which lists every block in order. It takes about 15 minutes. If you export the finished project from App Inventor, drop the extracted `Screen1.bky` into `src/` and `build_aia.py` will include it next time.

## Setup

1. Get a free API key from https://newsdata.io and keep it handy.
2. (Optional) check that the key works before touching the app:
   ```bash
   export NEWSDATA_API_KEY=your_key_here
   python3 check_api.py technology
   ```
3. Import the project into App Inventor (see above), add the blocks, then run it on a device with the MIT AI2 Companion app or build an APK from *Build > Android App (.apk)*.
4. On first launch paste the key into the key box and tap a category.

The key is read from the `NEWSDATA_API_KEY` environment variable only in `check_api.py`; inside the app it comes from the text box.

## Request used by the app

```
GET https://newsdata.io/api/1/latest?apikey=<key>&language=en&category=<category>
```

Only free-plan parameters are sent. Fields read from each result: `title`, `link`, `keywords`, and optionally `sentiment`. Pagination via `nextPage` is described in `docs/blocks.md` as an optional "More" button.

## Sample output of check_api.py

```
$ python3 check_api.py technology
HTTP 200, status=success, 10 results
1. Chipmaker unveils new low-power mobile processor
   keywords: chips, mobile, processors
   sentiment: (not returned on this plan)
2. ...
nextPage cursor: present
```

## Layout of the repo

```
src/Screen1.scm   Designer layout (JSON)
docs/blocks.md    blocks to build, in order
build_aia.py      packs src/ into dist/NewsDataReader.aia
check_api.py      command-line check of the API response
```

## Paid fields

Sentiment, `ai_tag` and `ai_summary` are only returned on paid newsdata.io plans. The app never requests them with query parameters; it just shows `sentiment` if the field happens to be in the response.
