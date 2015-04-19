## Scrapy-Insights

A simple python application to scrape a Facebook page and collect insights about the posts on the page.

## Installation

1. Create a [virtual environment](http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html) for the project:
`mkvirtualenv scrapy-insights`
2. Install requirements: `pip install requirements.txt`

## Running the application

You will need a Facebook access token with the `read_insights` and `manage_pages` permissions, as well as the Facebook
Page ID (found via `Page > Settings > Page Info > Facebook Page ID`).

Then, just run this command:

```bash
scrapy crawl page -a page=<PAGE_ID> -a token=<PAGE_TOKEN>
```

Then, insights for that pages posts will be collected and sent to RabbitMQ.

RabbitMQ configuration can be found in `insights/settings.py`.