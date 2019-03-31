import config
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import utils

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi, Send me any message containing links and I will detect'
                              ' any HTTP redirects in between them and final destination.')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def detect_message_url_redirects(update, context):
    """Find urls in user messages and detect their HTTP redirects. If any, will reply the result."""
    redirect_data = []
    replay_texts = []
    urls = utils.url_detector(update.message.text)
    for url in urls:
        redirects, final_url = utils.detect_redirects(url)
        redirect_data.append({'url': url, 'redirects': redirects, 'final_url': final_url})
    for element in redirect_data:
        if element['redirects']:
            text = '%s does %d HTTP redirect(s) before reaching %s .' % (element['url'], len(element['redirects'])
                                                                       , element['final_url'])
            replay_texts.append(text)

    if replay_texts:
        update.message.reply_text('\n'.join(replay_texts))


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config.tg_bot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # log all errors
    dp.add_error_handler(error)

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, detect_message_url_redirects))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
