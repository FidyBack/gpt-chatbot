# import re

# def create_inverted_index(data):
#     inverted_index = {}
#     for url, content in data.items():
#         # Split the content considering that is a html file
#         words = re.split(r"[^a-zA-Z0-9]", content)
#         print(words)

#         # Update the inverted index
#         for word in words:
#             if word not in inverted_index:
#                 inverted_index[word] = set()
#             inverted_index[word].add(url)

#     return inverted_index


# def search_keywords(inverted_index, keywords):
#     result = set()
#     for keyword in keywords:
#         if keyword in inverted_index:
#             # print(inverted_index)
#             result.update(inverted_index[keyword])

#     return result


# # Example usage
# data = {
#     "https://example.com/page1": """
# <!doctype html>
# <html>
# <head>
#     <title>Example Domain</title>

#     <meta charset="utf-8" />
#     <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
#     <meta name="viewport" content="width=device-width, initial-scale=1" />
#     <style type="text/css">
#     body {
#         background-color: #f0f0f2;
#         margin: 0;
#         padding: 0;
#         font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", "Open Sans", "Helvetica Neue", Helvetica, Arial, sans-serif;

#     }
#     div {
#         width: 600px;
#         margin: 5em auto;
#         padding: 2em;
#         background-color: #fdfdff;
#         border-radius: 0.5em;
#         box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);
#     }
#     a:link, a:visited {
#         color: #38488f;
#         text-decoration: none;
#     }
#     @media (max-width: 700px) {
#         div {
#             margin: 0 auto;
#             width: auto;
#         }
#     }
#     </style>
# </head>

# <body>
# <div>
#     <h1>Example Domain</h1>
#     <p>This domain is for use in illustrative examples in documents. You may use this
#     domain in literature without prior coordination or asking for permission.</p>
#     <p><a href="https://www.iana.org/domains/example">More information...</a></p>
# </div>
# </body>
# </html>
#     """,
#     "https://example.com/page2": "Here is the content of page 2",
#     "https://example.com/page3": "Page 3 content with some keywords",
# }

# inverted_index = create_inverted_index(data)

# keywords_to_search = ["domain"]
# search_result = search_keywords(inverted_index, keywords_to_search)

# print("Search Result:")
# for url in search_result:
#     print(url)


import requests

crawl_request = requests.get("https://example.com/")
crawl_data = crawl_request.text

# Extracts just the content of the page
crawl_data = crawl_data[crawl_data.find("<body"):crawl_data.find("</body>")]


print(crawl_data)



