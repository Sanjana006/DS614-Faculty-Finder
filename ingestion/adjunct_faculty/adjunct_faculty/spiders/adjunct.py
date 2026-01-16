import scrapy
import re


class DaiictAdjunctFacultySpider(scrapy.Spider):
    name = "adjunct_faculty"
    allowed_domains = ["daiict.ac.in"]
    start_urls = ["https://www.daiict.ac.in/adjunct-faculty"]

    def clean(self, s):
        if not s:
            return None
        return re.sub(r"\s+", " ", s).replace("\xa0", " ").strip()

    def parse(self, response):
        # Collect only adjunct faculty profile links
        links = response.css(
            "a[href*='/adjunct-faculty/']::attr(href)"
        ).getall()

        for link in links:
            link = link.rstrip("/")

            # Skip the listing page itself (absolute + relative)
            if link in (
                "/adjunct-faculty",
                "https://www.daiict.ac.in/adjunct-faculty"
            ):
                continue

            yield response.follow(link, self.parse_profile)

    def parse_profile(self, response):
        # NAME
        name = response.css(
            "div.field--name-field-faculty-names::text"
        ).get()

        # EDUCATION
        education = response.css(
            "div.field--name-field-faculty-name::text"
        ).get()

        # MAIL
        mail = response.css(
            "div.field--name-field-email div.field__item::text"
        ).get()

        # BIO
        bio_parts = response.css(
            "div.field--name-field-biography p::text"
        ).getall()
        bio = self.clean(" ".join(bio_parts))

        # SPECIALIZATION (handles both <p> and <ul><li>)
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

        # RESEARCH / TEACHING
        research_parts = response.css(
            "div.field--name-field-faculty-teaching p::text"
        ).getall()
        research = self.clean(" ".join(research_parts))

        yield {
            "Name": self.clean(name),
            "Education": self.clean(education),
            "Mail": self.clean(mail),
            "Bio": bio,
            "Specialization": specialization,
            "Research": research
        }
