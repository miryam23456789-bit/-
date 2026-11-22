"""נקודת הכניסה להפעלת תרחיש חיפוש מוצר בטרמינל."""

if __package__:
    from . import catalog, chat, matcher, ui
else:
    import catalog
    import chat
    import matcher
    import ui


def main() -> None:
    """מריץ חיפוש מוצרים שוב ושוב עד שהמשתמש מזין שורה ריקה."""
    while True:
        user_request = ui.read_request()
        if not user_request.text:
            break

        try:
            search_request = chat.parse_search_request(user_request.text)
        except ValueError as error:
            ui.show_result(str(error))
            continue

        products = catalog.search_by_item_type(search_request.item_type)
        match = matcher.find_one_within_budget(
            products,
            search_request.max_budget,
        )
        ui.show_result(chat.format_match_result(match))


if __name__ == "__main__":
    main()
