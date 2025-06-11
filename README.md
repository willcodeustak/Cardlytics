<h1> Brief Walkthrough</h1>

> (Just a heads up - I am not a financial advisor. You could totally just go to TCGplayer or similar sites and copy/paste recent sales into an AI chatbot yourself then prompt a request to aggregate. I basically just wanted to skip that whole website-visiting step.)

- You’ll need to generate an **eBay OAuth token** and place it in your `.env` file.

# Setting Up Google Sheets Functionality

## Create a Google Cloud Project

- Go to https://console.cloud.google.com and create a new project (or use an existing one).
- Use the search bar to find and enable the **Google Drive API** and **Google Sheets API**.  
  _You don’t need to enter payment info._

## Enable APIs

- Make sure both **Google Drive API** and **Google Sheets API** are enabled for your project.

## Create a Service Account

- Go to **IAM & Admin → Service Accounts**.
- Click **Create Service Account**, give it a name (e.g., `sheets-access`).
- After creating it, go to the **Keys** tab → **Add Key** → **JSON**.
- This will download a `.json` file - this is your credentials file.

## Save the Credentials File

- Move the downloaded file to your project directory (e.g., `src/google_credentials.json`).

* **Important:** Add it to your `.gitignore` to avoid uploading it to GitHub.

## Give the Bot Access to a Google Sheet

- Open the JSON file and find the `client_email` value.
- Create a new Google Sheet and share it with that email, giving it **edit access**.

## Add Your Email to the `.env` File

- In your `.env`, set the email you want the sheet shared with: `GOOGLE_SHEETS_SHARE_EMAIL` = yourname@gmail.com
- This email will receive access to any Sheets created by the app.

## 🐳 Run the App (After Setup Is Complete)

```bash
## 🐳 Docker Setup

# Build the image
docker build -t pokemon-prices .
# ^ Create a Docker image from current directory using Dockerfile

# Run the container
docker run -it --env-file .env pokemon-prices
# ^ -it lets you interact with the terminal (needed for input prompts)
# ^ --env-file loads environment variables from .env
```

<h2> You made it through the setup maze. Time for the fun part.</h2>

![Screenshot 2025-06-01 at 4 02 56 AM](https://github.com/user-attachments/assets/971174ca-e9fa-470d-9520-7bb0cb42ca07)

<h2> Type the name of the card you want to search for (e.g., “Gastly”). </h2>

![Screenshot 2025-06-01 at 4 05 13 AM](https://github.com/user-attachments/assets/4f885e32-199d-46a2-a619-c4cf86e210f5)

![Screenshot 2025-06-01 at 5 44 31 AM](https://github.com/user-attachments/assets/20f81411-9b03-4b10-b324-ca84bfc2d3fd)

> This is the item we searched for. (not mine)

<h2>(Optional) Specify the set number </h2>

![Screenshot 2025-06-01 at 4 05 26 AM](https://github.com/user-attachments/assets/4ddfb5cb-1c81-483b-913d-6ae789d3cebe)

<h2>Choose listing type </h2>

![Screenshot 2025-06-11 at 4 23 55 AM](https://github.com/user-attachments/assets/185e6974-0d5b-40bf-a9d6-300b41e2fe0e)

![Screenshot 2025-06-11 at 4 23 05 AM](https://github.com/user-attachments/assets/996f76be-eadf-463c-87df-c2bff3e72ea6)

<h2>All Fetchable Listings (raw, before filtering) </h2>

![Screenshot 2025-06-01 at 4 06 13 AM](https://github.com/user-attachments/assets/a2e0beef-133c-41ca-af42-b2e647104c0b)

<h2>Filtering Outliers.... </h2>

![Screenshot 2025-06-01 at 4 06 28 AM](https://github.com/user-attachments/assets/4d28b217-bfdb-48f7-995c-201e0b0850ea)

<h2>Price Summary</h2>

> We still ensure every item appears in the results—even if its condition is missing. Missing data should not cause an item to be excluded if it fits the search parameters.

![Screenshot 2025-06-01 at 4 06 45 AM](https://github.com/user-attachments/assets/d54d3472-462b-4bab-b809-da0fc40e39db)

<h2>Comparison Between Cardlytics and PriceCharting </h2>

> Data sets vary, I am ok with the range for now > see utils.py for 'filter_outliers_group'.
> Learned about IQR-based Outlier Detection or IQR Filtering logic.

> (Think of it as cutting off the lowest lows and highest highs that are unusually far from the middle). Interesting stuff.

| Statistic             | Cardlytics Data | Pricecharting Data | Condition Unclear |
| --------------------- | --------------- | ------------------ | ----------------- |
| **Count of Listings** | 37              | 30                 | 1                 |
| **Min Price**         | $224.00         | $206.50            | $55.00            |
| **Max Price**         | $417.00         | $340.00            | $55.00            |
| **Mean Price**        | $286.49         | $249.73            | $55.00            |
| **Median**            | $265.00         | $247.50            | $55.00            |
