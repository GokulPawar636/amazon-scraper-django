from django.shortcuts import render
from .forms import URLForm
from .utils import scrape_amazon_product
import pandas as pd
import os
from django.conf import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def scrape_view(request):
    product = None
    error_message = None
    download_link = None
    form = URLForm()

    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                product = scrape_amazon_product(url)

                if not product or product['title'] == "Title not found":
                    error_message = "⚠️ Unable to extract product details. The page may be dynamic or blocked."
                else:
                    # Create timestamped filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"scraped_product_{timestamp}.csv"
                    csv_path = os.path.join(settings.MEDIA_ROOT, filename)

                    # Save to CSV
                    df = pd.DataFrame([{
                        "Title": product['title'],
                        "Price": product['price'],
                        "Rating": product['rating'],
                        "URL": url
                    }])
                    df.to_csv(csv_path, index=False)

                    # Generate download link
                    download_link = f"/media/{filename}"

            except Exception as e:
                logger.error(f"Scraping failed: {e}")
                error_message = "❌ An error occurred while scraping. Please check the URL or try again later."

    return render(request, 'scraper/scrape.html', {
        'form': form,
        'product': product,
        'error_message': error_message,
        'download_link': download_link
    })
