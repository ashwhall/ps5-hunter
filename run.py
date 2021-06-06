import argparse
import time
import datetime

import mailer
import scrape


CHECK_INTERVAL_MINUTES = 5

def parse_args():
    """Parses CLA"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--headless',
                        help='Run Chrome in headless mode so no browser window is opened.',
                        action='store_true',
                        required=False)
    parser.add_argument('--skip-first-scrape',
                        help='Don\'t scrape on launch, wait the predetermined time first.',
                        action='store_true',
                        required=False)

    return parser.parse_args()


def check_for_stock(headless):
    stock_str = scrape.scrape(headless=headless)
    if stock_str:
        print('Sending the notification email!')
        mailer.send(stock_str)


if __name__ == '__main__':
    args = parse_args()
    mailer.set_login_credentials()

    if args.skip_first_scrape:
        time.sleep(CHECK_INTERVAL_MINUTES * 60)
    while True:
        start_time = time.time()
        check_for_stock(headless=args.headless)
        duration = time.time() - start_time
        print(f'\nCheck complete at {datetime.datetime.now()}')
        print(f'Duration: {round(duration)} seconds.')
        print(f'Sleeping for {CHECK_INTERVAL_MINUTES} minutes...\n')

        time.sleep(CHECK_INTERVAL_MINUTES * 60)
