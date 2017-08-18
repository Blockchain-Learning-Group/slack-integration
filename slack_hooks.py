import requests
import threading
import time
from constants import *

web_hook_url = 'https://hooks.slack.com/services/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'

msg_data_template = {
    ATTACHMENTS: [
        {
            "color": "#36a64f",
            PRE_TEXT: "",
            TITLE: "",
            TITLE_LINK: "",
            "footer": "BLG Bot",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
        }
    ]
}


def init_web_hooks():
    """ Init all threads for each hook, small delay between each """
    print('init hooks...')
    ether_block_stats = threading.Thread(target=get_ether_block_stats)
    ether_block_stats.start()

    time.sleep(60)

    ether_price = threading.Thread(target=get_ether_price)
    ether_price.start()


def get_ether_price():
    """ Ether price, v btc, v usd and timestamp """
    msg_data = msg_data_template.copy()
    msg_attachments = msg_data[ATTACHMENTS][0]
    msg_attachments[PRE_TEXT] = 'Real-time ether price, vs. btc and usd.'
    msg_attachments[TITLE] = 'Current Ethereum Price'
    msg_attachments[TITLE_LINK] = 'https://etherscan.io/charts'

    while True:
        res = requests.get('https://api.etherscan.io/api?module=stats&action=ethprice').json()

        print('\nNew Ether price data')

        msg_attachments[FIELDS] = [
            {
                'title': 'ETH / BTC',
                'value': res[RESULT]['ethbtc']
            }, {
                'title': 'ETH / USD',
                'value': res[RESULT]['ethusd']
            }
        ]

        requests.post(web_hook_url, json=msg_data)

        # hourly updates
        time.sleep(3600)


def get_ether_block_stats():
    """ Check block height daily """
    msg_data = msg_data_template.copy()
    msg_attachments = msg_data[ATTACHMENTS][0]
    msg_attachments[PRE_TEXT]= 'Real-time values of the Ethereum blockchain.'
    msg_attachments[TITLE] = 'Ethereum Network Stats'
    msg_attachments[TITLE_LINK] = 'https://etherchain.org/'

    while True:
        res = requests.get('https://etherchain.org/api/blocks/0/1').json()

        print('\nNew Ether blockchain data')

        msg_attachments[FIELDS] = [
            {
                'title': 'Network',
                'value': 'Mainnet',
                'short': True
            }, {
                'title': 'Block Number',
                'value': res[DATA][0]["number"],
                'short': True
            }, {
                'title': 'Block Hash',
                'value': res[DATA][0]['hash'],
            }, {
                'title': 'Timestamp',
                'value': res[DATA][0]['time'],
                'short': True
            }, {
                'title': 'Tx Count',
                'value': res[DATA][0]['tx_count'],
                'short': True
            }, {
                'title': 'Gas Limit',
                'value': res[DATA][0]['gasLimit'],
                'short': True
            }, {
                'title': 'Gas Used',
                'value': res[DATA][0]['gasUsed'],
                'short': True
            }, {
                'title': 'Size',
                'value': res[DATA][0]['size'],
                'short': True
            }, {
                'title': 'Block Time',
                'value': res[DATA][0]['blockTime'],
                'short': True
            }, {
                'title': 'Reward',
                'value': res[DATA][0]['reward'],
                'short': True
            }, {
                'title': 'Total Fee',
                'value': res[DATA][0]['totalFee'],
                'short': True
            }
        ]

        requests.post(web_hook_url, json=msg_data)

        # hourly updates
        time.sleep(3600)


if __name__ == '__main__':
    init_web_hooks()
