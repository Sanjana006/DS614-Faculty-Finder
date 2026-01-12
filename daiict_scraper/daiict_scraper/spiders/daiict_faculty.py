import scrapy
import re

class DaiictFacultySpider(scrapy.Spider):
    name = "daiict_faculty"
    allowed_domains = ["daiict.ac.in"]
    start_urls = ["https://www.daiict.ac.in/faculty"]

    def clean(self, s):
        if not s:
            return None
        return re.sub(r"\s+", " ", s).replace("\xa0", " ").strip()

    def parse(self, response):
        # Collect profile links
        links = response.css("a[href*='/faculty/']::attr(href)").getall()
        for link in links:
            if link.count("/") > 2:
                yield response.follow(link, self.parse_profile)

    def parse_profile(self, response):
        # NAME
        name = response.css("div.field--name-field-faculty-names::text").get()

        # PhD
        phd = response.css("div.field--name-field-faculty-name::text").get()

        #Mail
        mail = response.css("div.field--name-field-email div.field__item::text").get()


        # BIO
        bio = response.css("div.field--name-field-biography p::text").getall()
        bio = self.clean(" ".join(bio))

        # SPECIALIZATION
        specialization = self.clean(response.xpath("//div[contains(@class,'work-exp')]//p[normalize-space()][1]").xpath("string()").get())


        # RESEARCH (may not exist)
        research = response.css("div.field--name-field-faculty-teaching p::text").getall()
        research = self.clean(" ".join(research))

        yield {
            "Name": self.clean(name),
            "PhD in which field": self.clean(phd),
            "Mail": mail,
            "Bio": bio,
            "Specialization": self.clean(specialization),
            "Research": research
        }
