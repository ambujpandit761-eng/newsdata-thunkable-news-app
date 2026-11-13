# Blocks to build in App Inventor

Open the imported project, switch to the Blocks view, and create the following. Names match the components in `Screen1.scm`.

## Global variables

- `links` = create empty list (URLs, parallel to the list rows)
- `nextCursor` = "" (only needed for the optional More button)

## Screen1.Initialize

- set `KeyBox.Text` to `TinyDB1.GetValue(tag="key", valueIfTagNotThere="")`

## KeyBox.LostFocus

- call `TinyDB1.StoreValue(tag="key", valueToStore=KeyBox.Text)`

## Procedure `load(category)`

1. if `KeyBox.Text` is empty: set `StatusLabel.Text` to "Enter your API key first"; stop.
2. set `StatusLabel.Text` to "Loading..."
3. set `Web1.Url` to `join("https://newsdata.io/api/1/latest?apikey=", KeyBox.Text, "&language=en&category=", category)`
4. call `Web1.Get`

Do not add `size`, `timeframe`, `sentiment` or `from_date`; those are paid-plan parameters.

## Button clicks

| Button | call |
|---|---|
| BtnTop | `load("top")` |
| BtnTech | `load("technology")` |
| BtnSports | `load("sports")` |
| BtnBiz | `load("business")` |
| BtnHealth | `load("health")` |

## Web1.GotText(url, responseCode, responseType, responseContent)

1. if `responseCode = 401`: StatusLabel = "Invalid API key"; stop.
2. else if `responseCode = 429`: StatusLabel = "Rate limit reached, try again later"; stop.
3. else if `responseCode  <> 200`: StatusLabel = join("Request failed: ", responseCode); stop.
4. initialize local `data` = `Web1.JsonTextDecodeWithDictionaries(responseContent)`
5. initialize local `items` = `get value for key "results"` of `data`, not found = empty list
6. if `is list empty? items`: StatusLabel = "No articles found"; ListView1.Elements = empty list; stop.
7. set `global links` to empty list; initialize local `rows` = empty list
8. for each `item` in `items`:
   - `title` = get value for key "title" of item, not found = "(untitled)"
   - `kw` = get value for key "keywords" of item, not found = "" (can be null on some articles; if it is not a list, use "")
   - `sent` = get value for key "sentiment" of item, not found = ""
   - add `join(title, if kw is a list: "\n#" + (list to csv row of kw) else "", if sent <> "": "\n[" + sent + "]" else "")` to `rows`
   - add `get value for key "link" of item, not found = ""` to `global links`
9. set `ListView1.Elements` to `rows`; set `StatusLabel.Text` to join(length of list rows, " articles")

An empty `sentiment` just leaves that line out, so a free key still gives a clean list.

## ListView1.AfterPicking

- set `ActivityStarter1.DataUri` to `select list item(global links, ListView1.SelectionIndex)`
- call `ActivityStarter1.StartActivity`

## Optional: More button

Add a button `BtnMore`. In `GotText` store `get value for key "nextPage"` of `data` in `nextCursor`. On click, call `Web1.Get` with the same URL plus `&page=` and `nextCursor`, and append the new rows to `ListView1.Elements`. Hide the button when `nextCursor` is empty or null.
