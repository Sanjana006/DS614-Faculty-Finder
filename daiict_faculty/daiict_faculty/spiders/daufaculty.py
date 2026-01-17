import scrapy
import re


class DaiictFacultySpider(scrapy.Spider):
    name = "daufaculty"
    allowed_domains = ["daiict.ac.in"]

    start_urls = [
        "https://www.daiict.ac.in/faculty",
        "https://www.daiict.ac.in/adjunct-faculty",
        "https://www.daiict.ac.in/adjunct-faculty-international",
        "https://www.daiict.ac.in/distinguished-professor",
        "https://www.daiict.ac.in/professor-of-practice"
    ]

    def clean(self, s):
        if not s:
            return None
        return re.sub(r"\s+", " ", s).replace("\xa0", " ").strip()

    def parse(self, response):
        links = response.css("a[href]::attr(href)").getall()

        for link in links:
            if not link or "<" in link:
                continue

            if link.startswith("https://www.daiict.ac.in"):
                link = link.replace("https://www.daiict.ac.in", "")

            # skip listing pages only
            if link in (
                "/faculty",
                "/adjunct-faculty",
                "/adjunct-faculty-international",
                "/distinguished-professor",
                "/professor-of-practice",
            ):
                continue

            # accept all profile URLs
            if (
                link.startswith("/faculty/")
                or link.startswith("/adjunct-faculty/")
                or link.startswith("/adjunct-faculty-international/")
                or link.startswith("/distinguished-professor/")
                or link.startswith("/professor-of-practice/")
            ):
                yield response.follow(link, self.parse_profile)

    def parse_profile(self, response):
        name = response.css(
            "div.field--name-field-faculty-names::text"
        ).get()

        education = response.css(
            "div.field--name-field-faculty-name::text"
        ).get()

        mail = response.css(
            "div.field--name-field-email div.field__item::text"
        ).get()

        # BIO: works for p + li + mixed content
        bio_parts = response.xpath(
            "//div[contains(@class,'field--name-field-biography')]//text()"
        ).getall()
        bio = self.clean(" ".join(bio_parts))

        spec_items = response.xpath(
            "//div[contains(@class,'work-exp')]//li[normalize-space()]/text()"
        ).getall()

        if spec_items:
            specialization = self.clean(", ".join(spec_items))
        else:
            specialization = self.clean(
                response.xpath(
                    "//div[contains(@class,'work-exp')]//p[normalize-space()][1]"
                ).xpath("string()").get()
            )

        research_parts = response.css(
            "div.field--name-field-faculty-teaching p::text"
        ).getall()
        research = self.clean(" ".join(research_parts))

        # PUBLICATIONS (journal + conference + others)
        publication_items = response.xpath(
            "//div[contains(@class,'education') and contains(@class,'overflowContent')]"
            "//ul[contains(@class,'bulletText')]/li"
        )

        publications = []
        for li in publication_items:
            text = self.clean(li.xpath("string()").get())
            if text:
                publications.append(text)

        if not publications:
            publications = None


        yield {
            "Name": self.clean(name),
            "Education / PhD": self.clean(education),
            "Mail": self.clean(mail),
            "Bio": bio,
            "Specialization": specialization,
            "Research": research,
            "Publications": publications
        }
