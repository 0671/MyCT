# coding:utf-8
import sys
import logging
import traceback
from lib.core.data import logger,args
from lib.parser.parser import parseArgs
from lib.core.static import CUSTOM_LOGGING
from lib.core.common import setPaths,initWinStdout,printBanner,callGraph
from lib.core.config import initConfig
from lib.loader.loader import loadModule,loadTarget
from lib.controller.engine import run as runEngine


@callGraph
def main():
	try:
		logger.log(CUSTOM_LOGGING.INFO,'Start the initialization work ...')

		# Set program path
		logger.log(CUSTOM_LOGGING.SUCCESS,'Start setting program path ...')
		setPaths()

		# Parse command line parameters
		logger.log(CUSTOM_LOGGING.INFO,'Start parsing parameters ...')
		args=parseArgs()

		# Adjust color output
		logger.log(CUSTOM_LOGGING.INFO,'Start adjusting color output ...')
		initWinStdout()

		# Output banner information
		logger.log(CUSTOM_LOGGING.INFO,'Start printing banner ...')
		printBanner()
		
		# Print banner information
		logger.log(CUSTOM_LOGGING.INFO,'Start initial configuration ...')
		initConfig(args)

		# Load concurrent target
		logger.log(CUSTOM_LOGGING.INFO,'Start to initialize the concurrent target ...')
		loadTarget()

		# Load modules (preprocessing and processing)
		logger.log(CUSTOM_LOGGING.INFO,'Start to initialize the concurrent module ...')
		loadModule()

		# So far, all initialization work of the program is completed
		logger.log(CUSTOM_LOGGING.INFO,'So far, Initialization work has been completed')

		# Run concurrency engine
		logger.log(CUSTOM_LOGGING.INFO,'Start running the concurrent engine ...')
		runEngine()

		# End of program
		logger.log(CUSTOM_LOGGING.INFO,'End of program.')
		sys.exit(0)

	except KeyboardInterrupt as e:
		# If the KeyboardInterrupt exception occurs during the program, it means that the user has pressed ctrl+c, that is, the user voluntarily exits
		logger.error('User Quit')
		sys.exit(0)

	except Exception as e:
		# If other exceptions occur in the program, print the exception traceback message
		errMsg=traceback.format_exc()
		logger.error('An exception has occurred in the MyCT.\n Exception : \n%s'%errMsg)
		logger.error('The program exits unexpectedly.')
		sys.exit(-1)