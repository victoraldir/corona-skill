# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK.
import logging

from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_model import Response

from data.country_translation import countries
from data.globalstats.get_globalstats import get_status_by_country

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ask_country = 'Me pergunte a situação de algum país'
ask_other_country = 'Me pergunte a situação de algum outro país'


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Olá, bem-vindo ao infecções covid. De qual país você deseja saber detalhes?"
        handler_input.response_builder.speak(speech_text).ask(ask_country)
        return handler_input.response_builder.response


class CountryStatusIntentHandler(AbstractRequestHandler):
    """Handler for Country Status Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("CountryStatusIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        slots = handler_input.request_envelope.request.intent.slots
        country = slots['Country']
        country_translated = countries[country.value.lower()]

        print('country_translated', country_translated)

        country_stats = get_status_by_country(country_translated)

        print('country_stats', country_stats)

        pronoun = 'No'

        if country.value.lower().endswith('os'):
            pronoun = 'Nos'
        elif country.value.lower().endswith('as'):
            pronoun = 'Nas'
        elif country.value.lower().endswith('a'):
            pronoun = 'Na'

        speech_text = "{0} {1}, são {2} casos confirmados e {3} óbitos até o momento.".format(
            pronoun, country.value.lower(), country_stats['cases'], country_stats['deaths'])
        handler_input.response_builder.speak(speech_text).ask(ask_other_country)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Você pode me perguntar qual é a situação em um país. Por exemplo: Qual é a situação no Brasil?"
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Até mais!"
        handler_input.response_builder.speak(speech_text)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


# The intent reflector is used for interaction model testing and debugging.
# It will simply repeat the intent the user said. You can create custom handlers
# for your intents by defining them above, then also adding them to the request
# handler chain below.
class IntentReflectorHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = handler_input.request_envelope.request.intent.name
        speech_text = ("You just triggered {}").format(intent_name)
        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


# Generic error handling to capture any syntax or routing errors. If you receive an error
# stating the request handler chain is not found, you have not implemented a handler for
# the intent being invoked or included it in the skill builder below.
class ErrorHandler(AbstractExceptionHandler):
    """Catch-all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        speech_text = "Desculpe, eu não entendi. Tente novamente. De qual país você deseja saber detalhes?"
        handler_input.response_builder.speak(speech_text).ask(speech_text)
        return handler_input.response_builder.response


# This handler acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.
sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CountryStatusIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(
    IntentReflectorHandler())  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(ErrorHandler())

handler = sb.lambda_handler()
