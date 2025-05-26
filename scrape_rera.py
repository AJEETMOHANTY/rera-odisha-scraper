from playwright.sync_api import sync_playwright, TimeoutError
import time

def scrape_rera_projects():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://rera.odisha.gov.in/projects/project-list", timeout=60000)
        page.wait_for_selector("a:has-text('View Details')", timeout=60000)

        project_links = page.locator("a:has-text('View Details')")
        total_projects = min(project_links.count(), 6)

        results = []

        for i in range(total_projects):
            print(f"\nProcessing project {i + 1}/{total_projects}...")

            # Refresh project links due to possible DOM changes
            project_links = page.locator("a:has-text('View Details')")

            try:
                with page.expect_navigation():
                    project_links.nth(i).click()

                # Wait for loading spinner to disappear
                try:
                    page.wait_for_selector(".ngx-overlay", timeout=2000)
                    page.wait_for_selector(".ngx-overlay", state="detached", timeout=10000)
                except TimeoutError:
                    print("Loader did not appear or disappear as expected.")

                # Extract Project Overview
                overview = {}
                try:
                    for label in ["Project Name", "RERA Regd. No."]:
                        element = page.locator(f"text={label}").first.locator("xpath=..").locator("strong")
                        overview[label] = element.inner_text().strip()
                except Exception:
                    print("Could not extract Project Overview")

                # Switch to Promoter tab
                promoter = {"Company Name": "N/A", "Registered Office Address": "N/A", "GST No": "N/A"}
                try:
                    page.click("text=Promoter Details")
                    page.wait_for_selector("app-promoter-details", timeout=10000)

                    # Wait for actual content to load
                    for _ in range(15):
                        try:
                            val = page.locator("text=Company Name").first.locator("xpath=..").locator("strong").text_content().strip()
                            if val and val != "--":
                                break
                        except:
                            pass
                        time.sleep(1)

                    # Extract promoter info
                    for label in ["Company Name", "Registered Office Address", "GST No"]:
                        try:
                            val = page.locator(f"text={label}").first.locator("xpath=..").locator("strong").text_content().strip()
                            promoter[label] = val if val else "N/A"
                        except:
                            promoter[label] = "N/A"
                except Exception as e:
                    print("Could not extract Promoter Details:", e)

                results.append({
                    "RERA Regd. No": overview.get("RERA Regd. No.", "N/A"),
                    "Project Name": overview.get("Project Name", "N/A"),
                    "Promoter Name": promoter.get("Company Name", "N/A"),
                    "Promoter Address": promoter.get("Registered Office Address", "N/A"),
                    "GST No": promoter.get("GST No", "N/A"),
                })

            except Exception as e:
                print(f"Failed to extract project: {e}")
            finally:
                page.go_back()
                page.wait_for_selector("a:has-text('View Details')", timeout=10000)

        browser.close()

        # Print all results
        for idx, proj in enumerate(results, start=1):
            print(f"\n📄 Project {idx}")
            for k, v in proj.items():
                print(f"{k}: {v}")

if __name__ == "__main__":
    scrape_rera_projects()
