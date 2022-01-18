import requests
from bs4 import BeautifulSoup


def scrape_quote():
    """
    Returns a quote dictionary scraped from www.time.ir that contains quote, quote_author and
    an identifier for saving unique quotes to database in case of need.
    if the quote is a not formatted in a single html tag (like poetries), it makes 
    a recursive call. see time.ir for understanding how the quote is represented.
    in case of connection errors related to requests library, it will raise ConnectionError.
    """

    quote = {}
    try:
        data = requests.get('https://www.time.ir/').text
        soup = BeautifulSoup(data, 'lxml')
        random_quote = soup.find('div', class_='randomQuote')

        # checks if the quote is formated in more than one html tag.
        # in that case it will calls itself to get another quote.
        if random_quote.span.contents[0].next_sibling:
            return scrape_quote()
        else:
            quote['quote'] = random_quote.span.text
            quote['quote_author'] = random_quote.div.a.text
            # identifier is a unique key for each quote, containing quote_author and first and last letters of each quote.
            quote['identifier'] = f"{quote['quote_author']}_{quote['quote'][0:5]}_{quote['quote'][-7:-1]}"
            print(quote)

    except requests.exceptions.RequestException:
        raise ConnectionError('Can Not Connect To The Website')
