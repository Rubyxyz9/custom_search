# Google Custom Search CLI Tool

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

A powerful command-line interface (CLI) tool designed to leverage the Google Custom Search API for automated searching and data collection. Manage multiple API key profiles, build a persistent list of search queries, and run searches with advanced options, all from your terminal.

```
[ Google Custom Search CLI ]
       🔍  Powered by Python

```

---

## Features

-   **Profile Management**: Securely store and use multiple API Key / Search Engine ID pairs.
-   **Persistent Queries**: Add, list, and remove search queries that are saved between sessions.
-   **API Rate Limiting**: Automatically tracks your API usage to stay within the 100 requests/day free tier limit.
-   **Flexible Output**: Save results as a clean JSON list of either full URLs or just the domain names.
-   **Customizable Searches**: Specify the number of results to fetch (up to 100 per query) and the output filename.
-   **User-Friendly CLI**: Intuitive commands and a helpful interface make the tool easy to use.

---

## ⚙️ Installation

1.  **Clone the Repository**
    Clone this repository to your local machine using git.
    ```bash
    git clone https://github.com/Rubyxyz9/custom_search.git
    ```

2.  **Navigate to Directory**
    ```bash
    cd custom_search
    ```

3.  **Install Dependencies**
    Install the required Python packages using `pip`.
    ```bash
    chmod +x setup.sh
    ```
    ```
    ./setup
    ```
    
---

## 🔑 Configuration

Before you can use the tool, you need to configure it with your Google Custom Search API credentials.

1.  **Get Credentials**:
    * **API Key**: Get one from the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
    * **Search Engine ID (cx)**: Create a custom search engine at [Programmable Search Engine](https://programmablesearchengine.google.com/) and get its ID.

2.  **Run the Config Command**:
    Execute the `config` command and follow the interactive prompts. You can create multiple profiles for different sets of credentials.
    ```bash
    python3 main.py config
    ```
    You will be asked for:
    * **Profile Name**: A nickname for your credentials (e.g., `work-account`). If you just press Enter, it will be saved as `default`.
    * **API Key**: Your Google API key.
    * **Search Engine ID**: Your `cx` value.

    Your credentials will be saved securely in a `.credentials` file in the project directory.

---

## 🚀 Usage

The tool is operated through a series of simple commands.

### 1. Managing Queries

First, build your list of search queries.

* **Add a new query:**
    ```bash
    python3 main.py query add 'inurl:security.txt "Contact:"'
    ```

* **List all saved queries:**
    ```bash
    python3 main.py query list
    ```
    This will show you each query with an index number.

* **Remove a query by its index:**
    ```bash
    python3 main.py query remove 2
    ```

### 2. Running a Search

Once you have queries saved, use the `run` command to execute the search.

* **Basic Search**:
    This uses the `default` profile and saves 10 results per query to `results.json`.
    ```bash
    python3 main.py run
    ```

* **Advanced Search**:
    This example uses a specific profile named `work-account`, fetches **50** results per query, saves the **full URLs** (not just domains), and writes them to a custom file named `work_urls.json`.
    ```bash
    python3 main.py run -p work-account -n 50 --full-url -o work_urls.json
    ```

### 3. Getting Help

Use the `-h` or `--help` flag to see all available commands and options.
```bash
# See all main commands
python3 main.py -h

# See options for a specific command (e.g., run)
python3 main.py run -h
```
