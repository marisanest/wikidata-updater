import logging
import sys
import traceback

import bot
import mailer

mail = False

args = sys.argv[1:]
for arg in args:
    if arg == '--mail':
        mail = True

try:
    logging.info('----------------------- START -----------------------')
    bot.run()

    logging.info(' Import finished')
    if mail:
        mailer.send_success()
    exit(0)

except Exception as exception:

    logging.error(' Import could not be processed: ' + traceback.print_exc())
    if mail:
        mailer.send_error()
    exit(1)


