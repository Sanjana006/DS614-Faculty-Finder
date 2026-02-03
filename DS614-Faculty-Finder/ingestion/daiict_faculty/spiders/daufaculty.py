import scrapy
import re
from scrapy.exceptions import DropItem


class DaiictFacultySpider(scrapy.Spider):
    name = "daufaculty"
    allowed_domains = ["daiict.ac.in"]

    start_urls = [
        "https://www.daiict.ac.in/faculty",
        "https://www.daiict.ac.in/adjunct-faculty",
        "https://www.daiict.ac.in/adjunct-faculty-international",
        "https://www.daiict.ac.in/distinguished-professor",
        "https://www.daiict.ac.in/professor-practice",
    ]

    # ---------- Utility ----------
    def clean(self, text):
        """
        Normalize whitespace and handle null values safely.
        """
        if not text:
            return None
        return re.sub(r"\s+", " ", text).replace("\xa0", " ").strip()

    # ---------- Requests ----------
    def start_requests(self):
        """
        Handles HTTP-level errors explicitly.
        """
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.errback_http,
            )

    def errback_http(self, failure):
        """
        Handles network / HTTP errors.
        """
        self.logger.error(
            f"HTTP error occurred: {repr(failure)}"
        )

    # ---------- Listing Page ----------
    def parse(self, response):
        """
        Extracts faculty profile links safely.
        """
        try:
            links = response.css("a[href]::attr(href)").getall()

            for link in links:
                if not link or "<" in link:
                    continue

                if link.startswith("https://www.daiict.ac.in"):
                    link = link.replace("https://www.daiict.ac.in", "")

                # Skip listing pages
                if link in (
                    "/faculty",
                    "/adjunct-faculty",
                    "/adjunct-faculty-international",
                    "/distinguished-professor",
                    "/professor-of-practice",
                ):
                    continue

                # Accept profile URLs only
                if link.startswith((
                    "/faculty/",
                    "/adjunct-faculty/",
                    "/adjunct-faculty-international/",
                    "/distinguished-professor/",
                    "/professor-of-practice/",
                )):
                    yield response.follow(
                        link,
                        callback=self.parse_profile,
                        errback=self.errback_http,
                    )

        except Exception as e:
            self.logger.error(
                f"Error parsing listing page {response.url}: {str(e)}"
            )

    # ---------- Profile Page ----------
    def parse_profile(self, response):
        """
        Extracts faculty profile details with full validation
        and exception handling.
        """
        try:
            name = self.clean(
                response.css(
                    "div.field--name-field-faculty-names::text"
                ).get()
            )

            # Mandatory field check
            if not name:
                self.logger.warning(
                    f"Skipping profile (name missing): {response.url}"
                )
                raise DropItem("Faculty name missing")

            education = self.clean(
                response.css(
                    "div.field--name-field-faculty-name::text"
                ).get()
            )

            mail = self.clean(
                response.css(
                    "div.field--name-field-email div.field__item::text"
                ).get()
            )

            # BIO
            bio_parts = response.xpath(
                "//div[contains(@class,'field--name-field-biography')]//text()"
            ).getall()
            bio = self.clean(" ".join(bio_parts))

            # SPECIALIZATION
            spec_items = response.xpath(
                "//div[contains(@class,'work-exp')]//li[normalize-space()]/text()"
            ).getall()

            specialization = (
                self.clean(", ".join(spec_items))
                if spec_items
                else self.clean(
                    response.xpath(
                        "//div[contains(@class,'work-exp')]//p[normalize-space()][1]"
                    ).xpath("string()").get()
                )
            )

            # RESEARCH
            research_parts = response.css(
                "div.field--name-field-faculty-teaching p::text"
            ).getall()
            research = self.clean(" ".join(research_parts))

            # PUBLICATIONS
            publication_items = response.xpath(
                "//div[contains(@class,'education') and contains(@class,'overflowContent')]"
                "//ul[contains(@class,'bulletText')]/li"
            )

            publications = [
                self.clean(li.xpath("string()").get())
                for li in publication_items
                if self.clean(li.xpath("string()").get())
            ] or None

            yield {
                "name": name,
                "phd_field": education,
                "mail": mail,
                "bio": bio,
                "specialization": specialization,
                "research": research,
                "publications": publications,
            }

        except DropItem:
            return

        except Exception as e:
            self.logger.error(
                f"Error parsing profile {response.url}: {str(e)}"
            )
