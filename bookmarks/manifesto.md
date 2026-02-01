# bookmarks

## Rules

This project is one of principal. As such, the following rules should be enforced when generating projects:
- No client side javascript event handling if possible. HTMX provides the tools for success
- Embrace HTMX style. If it can be done simpler, do it
- WET Principal - DO Repeat Yourself if you must, to make the code readable and simple
    If you repeat yourself exactly more than 3 times, you may abstract.
- Segment the API appropriately, each endpoint prefix should do one thing.
- Do not use CDNs directly at runtime if possible
- Do not retain any of the boiletplate code that you have received. You may keep the navigation logic if it suits your app, but the other pages are just to inform you of the standards