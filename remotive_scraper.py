import requests
import re


REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"

# Approximate USD to INR conversion.
# This is used only for display and should not be treated as an exact live rate.
USD_TO_INR = 92


def convert_usd_salary_to_inr(salary_text):
    """
    Convert clearly annual USD salary ranges into approximate INR.
    Hourly salaries are kept unchanged.
    """

    if not salary_text:
        return {
            "salary_inr": "Not specified",
            "salary_min_inr": None,
            "salary_max_inr": None
        }

    text = salary_text.strip()

    # Do not convert hourly salaries.
    if "hour" in text.lower():
        return {
            "salary_inr": text,
            "salary_min_inr": None,
            "salary_max_inr": None
        }

    # Find values such as:
    # $20k - $35k
    # $90k - $105k
    # $10K-$20K
    # OTE $25k - $35k
    matches = re.findall(
        r"\$?\s*([\d,.]+)\s*([kKmM]?)",
        text
    )

    values = []

    for number, suffix in matches:

        try:
            value = float(number.replace(",", ""))

            if suffix.lower() == "k":
                value *= 1000
            elif suffix.lower() == "m":
                value *= 1000000

            values.append(value)

        except ValueError:
            continue

    if not values:
        return {
            "salary_inr": text,
            "salary_min_inr": None,
            "salary_max_inr": None
        }

    converted = [value * USD_TO_INR for value in values]

    if len(converted) >= 2:

        minimum = converted[0]
        maximum = converted[1]

        return {
            "salary_inr": (
                f"₹{minimum:,.0f} – ₹{maximum:,.0f} approx."
            ),
            "salary_min_inr": minimum,
            "salary_max_inr": maximum
        }

    value = converted[0]

    return {
        "salary_inr": f"₹{value:,.0f} approx.",
        "salary_min_inr": value,
        "salary_max_inr": value
    }


def search_remotive_jobs(keyword="", limit=50):

    params = {
        "limit": limit
    }

    if keyword.strip():
        params["search"] = keyword.strip()

    try:

        response = requests.get(
            REMOTIVE_API_URL,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        jobs = data.get("jobs", [])

        results = []

        for job in jobs:

            title = job.get(
                "title",
                "Untitled Job"
            )

            company = job.get(
                "company_name",
                "Not provided by source"
            )

            location = job.get(
                "candidate_required_location",
                "Remote / Worldwide"
            )

            description = job.get(
                "description",
                ""
            )

            url = job.get(
                "url",
                ""
            )

            created = job.get(
                "publication_date",
                ""
            )

            salary = job.get(
                "salary",
                ""
            )

            if not salary:
                salary = "Not specified"

            salary_data = convert_usd_salary_to_inr(
                salary
            )

            job_type = job.get(
                "job_type",
                "Not specified"
            )

            category = job.get(
                "category",
                "Not specified"
            )

            results.append({

                "title": title,

                "company": company,

                "location": location,

                "description": description,

                "url": url,

                "created": created,

                # Original Remotive salary
                "salary_original": salary,

                # INR display salary
                "salary": salary_data["salary_inr"],

                # Used by salary filtering
                "salary_min": salary_data["salary_min_inr"],

                "salary_max": salary_data["salary_max_inr"],

                "job_type": job_type,

                "category": category,

                "source": "Remotive",

                "work_mode": "Remote"
            })

        return results

    except requests.exceptions.RequestException as e:

        print(f"Remotive API error: {e}")

        return []

    except Exception as e:

        print(f"Unexpected Remotive error: {e}")

        return []


if __name__ == "__main__":

    jobs = search_remotive_jobs(
        keyword="Python",
        limit=10
    )

    print(
        f"\nFound {len(jobs)} Remotive jobs.\n"
    )

    for job in jobs:

        print("=" * 60)

        print("Title:", job["title"])

        print("Company:", job["company"])

        print("Location:", job["location"])

        print(
            "Original Salary:",
            job["salary_original"]
        )

        print(
            "INR Salary:",
            job["salary"]
        )

        print("Job Type:", job["job_type"])

        print("Source:", job["source"])

        print("URL:", job["url"])