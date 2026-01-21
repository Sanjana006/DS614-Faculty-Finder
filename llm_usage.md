# LLM Usage in the project. 

---

## Prompt 1
I am using Scrapy to crawl a university website and extract faculty profile links. I want to understand how to safely fetch all anchor tag links from a page and iterate over them, while ignoring invalid or malformed href values that could break the crawler. How can this be done in Scrapy in a clean and reliable way?

## Output
To safely extract and iterate over links in Scrapy, the response object provides selector methods that allow access to HTML elements in a structured way. Anchor tag links can be collected by selecting all href attributes from <a> tags using CSS selectors. This returns a list of link values present on the page.
Before processing each link, it is important to validate the extracted values. Empty links, None values, or malformed strings (such as those containing raw HTML fragments) should be ignored to prevent runtime errors or unintended crawling behavior. Adding simple conditional checks while iterating over the links ensures that only valid URLs are processed further.
By combining structured link extraction with basic validation and filtering, a Scrapy crawler can remain stable and reliable even when dealing with imperfect or inconsistent HTML content commonly found on real-world websites.

✅ Scrapy Code Implementation (Matching the Explanation)

    links = response.css("a[href]::attr(href)").getall()

    for link in links:
        # Skip empty or malformed href values
        if not link or "<" in link:
            continue

        # Process only valid links
        yield response.follow(link, callback=self.parse_profile)
