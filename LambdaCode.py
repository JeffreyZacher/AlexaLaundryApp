# -*- coding: utf-8 -*-
from PostLaundry import GetMachines

import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

STOP_MESSAGE = "Goodbye!"
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."
HELP_REPROMPT = "OOPS"

sb = SkillBuilder()

# Built-in Intent Handlers
class GetMachineAvailability(AbstractRequestHandler):
    """Handler for Skill Launch and Get Machine Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetMachineAvailability")(handler_input))

    def handle(self, handler_input: HandlerInput):

        itemSlot = handler_input.request_envelope.request.intent.slots["machine"].value

        availabilities = GetMachines()

        response = ""

        if itemSlot == "dryers":
            response = ' and '.join([' is '.join(tups) for tups in list(filter(lambda x: "Dryer" in x[0], availabilities))])
        elif itemSlot == "washing machines":
            response = ' and '.join([' is '.join(tups) for tups in list(filter(lambda x: "Washer" in x[0], availabilities))])
        elif itemSlot == "machines":
            response = ' and '.join([' is '.join(tups) for tups in list(availabilities)])

        return  handler_input.response_builder.speak(response).response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


# Register intent handlers
sb.add_request_handler(GetMachineAvailability())
sb.add_request_handler(CancelOrStopIntentHandler())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
