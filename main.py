from playwright.sync_api import sync_playwright, TimeoutError
import time
import json


def get_jobs(filter_1, filter_2, filter_3):
    """
    This function navigates the iCapital career website.

    Args:
        filter_1: Department Filter
        filter_2: Office Filter
        filter_3: Employement Type Filter

    Returns:
        list of jobs.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://icapital.com/")

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)") #scroll to bottom
        page.locator('//a[text()="Careers"]').nth(0).click()
        time.sleep(5)
        page.evaluate("window.scrollTo(0, 1000)")

        dropdown_1 = page.locator("//select[contains(@id, 'filter_dep')]")
        dropdown_1.select_option(label=filter_1)
        dropdown_2 = page.locator("//select[contains(@id, 'filter_office')]")
        dropdown_2.select_option(label=filter_2)
        dropdown_3 = page.locator("//select[contains(@id, 'filter_emp_type')]")
        dropdown_3.select_option(label=filter_3)
        time.sleep(5)

        page.evaluate("window.scrollTo(0, 1500)")
        jobs = page.locator("div.all_jobs div.jobs div")
        process_jobs(jobs=jobs)
        browser.close()

def process_jobs(jobs):
    """
    Convert the jobs to a JSON file.

    Args:
        jobs: All available jobs

    Output:
        Creates a JSON file that contains job title, location and description.
    """
    job_list = []

    for i in range(jobs.count()):
        div = jobs.nth(i)
        if div.is_visible(): # get only visible jobs
            try:
                job_list.append(
                    {
                        "job_title": div.locator("h2").text_content(),
                        "location": div.locator("div.display_location").text_content(),
                        "description": div.locator("div.display_description").text_content()
                    }
                )
            except TimeoutError:
                continue

    data = {"jobs": job_list}
    with open("iCapital_jobs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def main():
    """Scrape the jobs from https://icapital.com/"""
    filter_1 = "All Departments" 
    filter_2 = "CA ON - Toronto"
    filter_3 = "Full-time"
    print("Scrape processing ....")
    get_jobs(filter_1, filter_2, filter_3)
    print("iCapital website scrape finished!")
   

if __name__ == "__main__":
    """Entry point"""
    main()
