# 📊 Workday Application Status Tracker

Automatically track and monitor your job applications across multiple Workday career portals (NVIDIA, Adobe, and more).  
This GitHub Action checks your Workday application status every **30 minutes**, formats the response, and saves readable reports in your repository.

---

## 🚀 Features

- 🕒 Checks all configured Workday job portals every **30 minutes**
- ✨ Beautiful, human-readable formatting of application statuses
- 🗂 Supports **unlimited companies**
- 🔐 Uses GitHub Secrets for CSRF tokens and session cookies
- 📦 Saves each company's results to a separate `.txt` file  
- 📝 Automatic Git commit & push when new data is fetched
- ⚙️ Fully configurable via `companies.json`

---

## 📁 Repository Structure

```

workday-report/
├── check_workday.py        # Main Workday scraper + formatter
├── companies.json          # Configuration for all companies
├── nvidia.txt              # NVIDIA application log (auto-updated)
├── adobe.txt               # Adobe application log (auto-updated)
└── .github/
└── workflows/
└── workday-check.yml   # GitHub Action (runs every 30 mins)

````

---

## 🧠 How It Works

Each Workday company's API requires:

- A **CSRF token**
- A **session Cookie**
- A **base_url**, `type`, and `limit`

These are defined in `companies.json`, example:

```json
{
  "companies": [
    {
      "name": "nvidia",
      "base_url": "https://nvidia.wd5.myworkdayjobs.com/wday/cxs/nvidia/NVIDIAExternalCareerSite/applications",
      "type": "active",
      "limit": 20,
      "cookie_secret": "NVIDIA_COOKIE",
      "csrf_secret": "NVIDIA_CSRF"
    }
  ]
}
````

The GitHub Action reads each secret and calls the API for every company listed.

Results are cleaned, formatted, and appended to:

```
nvidia.txt
adobe.txt
your-next-company.txt
```

with timestamps.

---

## 🔐 Setup: Adding Secrets

Go to:

**GitHub → Repo Settings → Secrets → Actions → New Repository Secret**

For NVIDIA:

* `NVIDIA_COOKIE`
* `NVIDIA_CSRF`

For Adobe:

* `ADOBE_COOKIE`
* `ADOBE_CSRF`

You can add more companies later by adding their secrets and extending `companies.json`.

---

## ⚙️ Running Locally (Optional)

Set environment variables:

### macOS / Linux / WSL:

```bash
export NVIDIA_COOKIE="paste-cookie-here"
export NVIDIA_CSRF="paste-csrf-here"
export ADOBE_COOKIE="paste-cookie-here"
export ADOBE_CSRF="paste-csrf-here"
```

Run:

```bash
python3 check_workday.py
```

### Windows (PowerShell):

```powershell
setx NVIDIA_COOKIE "paste-cookie-here"
setx NVIDIA_CSRF "paste-csrf-here"
setx ADOBE_COOKIE "paste-cookie-here"
setx ADOBE_CSRF "paste-csrf-here"
```

Reopen terminal and run:

```powershell
python check_workday.py
```

---

## 🛠 GitHub Action (runs every 30 minutes)

The workflow file is located in:

```
.github/workflows/workday-check.yml
```

It:

* Checks all Workday APIs
* Formats results
* Appends them to text files
* Commits changes automatically

---

## 📄 Example Output

```
===== 2025-11-15 23:30:07 UTC =====

Job Title: Site Reliability Engineer, HPC and LSF
Requisition: JR2006583
Status: Application Received
Applied On: November 5, 2025
------------------------------

Job Title: Software Engineer, Robotics - Isaac Lab
Requisition: JR2007292
Status: Application Received
Applied On: November 3, 2025
------------------------------
```

---

## ➕ Adding More Companies

1. Add new secrets:

   ```
   AMAZON_COOKIE
   AMAZON_CSRF
   ```

2. Add new item to `companies.json`:

```json
{
  "name": "amazon",
  "base_url": "https://amazon.wd1.myworkdayjobs.com/.../applications",
  "type": "active",
  "limit": 20,
  "cookie_secret": "AMAZON_COOKIE",
  "csrf_secret": "AMAZON_CSRF"
}
```

Done — the Action will automatically include it.

---

## 🧩 Troubleshooting

| Issue           | Cause                      | Fix                                               |
| --------------- | -------------------------- | ------------------------------------------------- |
| 403 Forbidden   | Cookies expired            | Refresh Workday cookies and update GitHub Secrets |
| JSONDecodeError | Cloudflare blocked request | Update cookies, OR use Playwright auto-refresh    |
| Bot cannot push | repo permissions           | Enable **Workflow Write** permission              |
| No output       | Missing secrets            | Add secrets correctly                             |

---

## ❤️ Future Enhancements

* Automatic cookie & CSRF token refresh via Playwright
* Slack / Discord notifications when application status changes
* Per-application changelog tracking
* Web dashboard showing all your applications

---

## 📬 Contributions

PRs and feature requests are welcome!
If you want additional integrations (Meta, Tesla, Google, KPMG Workday portals), open an issue.

---

## 📄 License

This project is licensed under the MIT License.
