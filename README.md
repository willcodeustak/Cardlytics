<h1> Brief Walkthrough</h1>

> (Just a heads up - I am not a financial advisor. You could totally just go to TCGplayer or similar sites and copy/paste recent sales into an AI chatbot yourself then prompt a request to aggregate. I basically just wanted to skip that whole website-visiting step.)

## 🐳 Docker Setup

```bash
# Build the image
docker build -t pokemon-prices .

# Run the container
docker run -it --env-file .env pokemon-prices

Why No Volume Mount is Needed (For Now)
Docker containers act like temporary mini-computers that run your application. Normally, anything saved inside the container is lost once it stops.

A volume mount is a way to connect a folder on your actual machine to the container,
so files (like exports) can be saved outside the container and persist after it closes.

Since this project does not currently save any files (e.g., Google Sheets export is still in development),
there is no need to set up a volume mount yet. Once export features are added, using a volume mount will ensure your data is saved on your local system.

```

Make sure your .env file (token) is configured correctly before running.
Youll need a Token Access from eBay

<h2> After getting lost in eBay’s Find Waldo-esque documentation on activating tokens you've finally arrived </h2>

![Screenshot 2025-06-01 at 4 02 56 AM](https://github.com/user-attachments/assets/971174ca-e9fa-470d-9520-7bb0cb42ca07)

<h2> Type the name of the card you want to search for (e.g., “Gastly”). </h2>

![Screenshot 2025-06-01 at 4 05 13 AM](https://github.com/user-attachments/assets/4f885e32-199d-46a2-a619-c4cf86e210f5)

![Screenshot 2025-06-01 at 5 44 31 AM](https://github.com/user-attachments/assets/20f81411-9b03-4b10-b324-ca84bfc2d3fd)

> This is the item we searched for. (not mine)

<h2>(Optional) Specify the set number </h2>

![Screenshot 2025-06-01 at 4 05 26 AM](https://github.com/user-attachments/assets/4ddfb5cb-1c81-483b-913d-6ae789d3cebe)

<h2>Choose listing type </h2>
Y = completed or past sales,
N = active/current sales

Export to google sheet? ( in development )

![Screenshot 2025-06-01 at 4 05 38 AM](https://github.com/user-attachments/assets/82d9b569-e684-4e6e-a68f-1c700c635a55)

<h2>All Fetchable Listings (raw, before filtering) </h2>

![Screenshot 2025-06-01 at 4 06 13 AM](https://github.com/user-attachments/assets/a2e0beef-133c-41ca-af42-b2e647104c0b)

<h2>Filtering Outliers.... </h2>

![Screenshot 2025-06-01 at 4 06 28 AM](https://github.com/user-attachments/assets/4d28b217-bfdb-48f7-995c-201e0b0850ea)

<h2>Price Summary</h2>

> We still ensure every item appears in the results—even if its condition is missing. Missing data should not cause an item to be excluded if it fits the search parameters.

![Screenshot 2025-06-01 at 4 06 45 AM](https://github.com/user-attachments/assets/d54d3472-462b-4bab-b809-da0fc40e39db)

<h2>Comparison Between Cardlytics and PriceCharting </h2>

> Data sets vary, I am ok with the range for now ---> see utils.py for 'filter_outliers_group'.
> Learned about IQR-based Outlier Detection or IQR Filtering logic.

> (Think of it as cutting off the lowest lows and highest highs that are unusually far from the middle). Interesting stuff.

| Statistic             | Cardlytics Data | Pricecharting Data | Condition Unclear |
| --------------------- | --------------- | ------------------ | ----------------- |
| **Count of Listings** | 30              | 37                 | 1                 |
| **Min Price**         | $206.50         | $224.00            | $55.00            |
| **Max Price**         | $340.00         | $417.00            | $55.00            |
| **Mean Price**        | $249.73         | $286.49            | $55.00            |
| **Median**            | $247.50         | $265.00            | $55.00            |
