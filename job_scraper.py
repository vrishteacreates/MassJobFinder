import requests
import os
from dotenv import load_dotenv


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")


# ==========================================
# SEARCH JOBS FUNCTION
# ==========================================

def search_jobs(
    keyword,
    location="India",
    experience="Any Experience",
    job_type="Any Type",
    results_per_page=20
):

    url = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": keyword,
        "where": location,
        "results_per_page": results_per_page,
        "content-type": "application/json"
    }


    # ==========================================
    # EXPERIENCE TERMS
    # ==========================================

    if experience != "Any Experience":

        experience_terms = {

            "Fresher": "fresher",

            "0–1 years": "entry level",

            "1–3 years": "junior",

            "3–5 years": "experienced",

            "5+ years": "senior"
        }

        if experience in experience_terms:

            params["what"] = (
                keyword
                + " "
                + experience_terms[experience]
            )


    # ==========================================
    # JOB TYPE TERMS
    # ==========================================

    if job_type != "Any Type":

        job_type_terms = {

            "Full-time": "full time",

            "Part-time": "part time",

            "Internship": "internship",

            "Contract": "contract"
        }

        if job_type in job_type_terms:

            params["what"] += (
                " "
                + job_type_terms[job_type]
            )


    # ==========================================
    # API REQUEST
    # ==========================================

    try:

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

    except requests.RequestException as error:

        print("\nREQUEST ERROR:")
        print(error)

        return []


    # ==========================================
    # CHECK API RESPONSE
    # ==========================================

    if response.status_code != 200:

        print("\nAPI ERROR:")
        print("Status Code:", response.status_code)
        print(response.text)

        return []


    # Convert API response to JSON
    data = response.json()


    # Get jobs
    results = data.get(
        "results",
        []
    )


    # ==========================================
    # CREATE JOB LIST
    # ==========================================

    jobs = []


    for job in results:


        # ======================================
        # COMPANY
        # ======================================

        company_data = job.get(
            "company"
        )

        company = None


        if isinstance(
            company_data,
            dict
        ):

            # Adzuna uses display_name
            company = company_data.get(
                "display_name"
            )


        elif isinstance(
            company_data,
            str
        ):

            company = company_data


        # Fallback
        if not company:

            company = "Not provided by source"


        # ======================================
        # LOCATION
        # ======================================

        location_data = job.get(
            "location"
        )

        job_location = None


        if isinstance(
            location_data,
            dict
        ):

            job_location = location_data.get(
                "display_name"
            )


        elif isinstance(
            location_data,
            str
        ):

            job_location = location_data


        # Fallback
        if not job_location:

            job_location = "Location not specified"


        # ======================================
        # SALARY
        # ======================================

        salary_min = job.get(
            "salary_min"
        )

        salary_max = job.get(
            "salary_max"
        )


        if (
            salary_min is not None
            and
            salary_max is not None
        ):

            salary = (
                f"₹{salary_min:,.0f}"
                f" – "
                f"₹{salary_max:,.0f}"
            )


        elif salary_min is not None:

            salary = (
                f"₹{salary_min:,.0f}+"
            )


        elif salary_max is not None:

            salary = (
                f"Up to ₹{salary_max:,.0f}"
            )


        else:

            salary = "Not specified"


        # ======================================
        # JOB URL
        # ======================================

        job_url = job.get(
            "redirect_url",
            ""
        )


        # ======================================
        # JOB TITLE
        # ======================================

        title = job.get(
            "title",
            "Title not specified"
        )


        # ======================================
        # DESCRIPTION
        # ======================================

        description = job.get(
            "description",
            ""
        )


        # ======================================
        # CREATED DATE
        # ======================================

        created = job.get(
            "created",
            ""
        )


        # ======================================
        # ADD JOB
        # ======================================

        jobs.append({

            "title": title,

            "company": company,

            "location": job_location,

            "description": description,

            "url": job_url,

            "created": created,

            "salary_min": salary_min,

            "salary_max": salary_max,

            "salary": salary
        })


    return jobs


# ==========================================
# TEST THE FUNCTION
# ==========================================

if __name__ == "__main__":

    print(
        "\nSearching for jobs...\n"
    )


    jobs = search_jobs(

        keyword="Sales Person",

        location="Mumbai",

        experience="Any Experience",

        job_type="Any Type",

        results_per_page=5
    )


    print(
        "\n=========================================="
    )

    print(
        "PROCESSED JOB RESULTS"
    )

    print(
        "=========================================="
    )


    print(
        f"\nFound {len(jobs)} jobs\n"
    )


    for i, job in enumerate(
        jobs,
        start=1
    ):

        print(
            f"Job {i}: {job['title']}"
        )

        print(
            f"Company: {job['company']}"
        )

        print(
            f"Location: {job['location']}"
        )

        print(
            f"Salary: {job['salary']}"
        )

        print(
            f"URL: {job['url']}"
        )

        print(
            "-" * 60
        )