import logging
import random
import gettext
import json
import boto3
import botocore
import ast
import ask_sdk_core
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_intent_name, get_dialog_state, get_slot_value

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


from ask_sdk_model.dialog import (
     ElicitSlotDirective, DelegateDirective)
from ask_sdk_model import (
     Response, IntentRequest, DialogState, SlotConfirmationStatus, Slot)
from ask_sdk_model.slu.entityresolution import StatusCode

skill_builder = SkillBuilder()
# abstractrequest = AbsractRequestHandler()

s3 = boto3.client('s3')
bucket = 'sourcedivya'
key = 'data/final_hospitaldata.json'





logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stateChosen = ''
surgeryChosen = ''
CostCalculated = ''
DisplayCost = ''
class LaunchRequestHandler(AbstractRequestHandler):
     """Handler for Skill Launch."""
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool

         return ask_utils.is_request_type("LaunchRequest")(handler_input)

     def handle(self, handler_input):
         # type: (HandlerInput) -> Response
         speak_output = "Welcome! Ready to start?"


         return (

             handler_input.response_builder
                 .speak(speak_output)
                 .ask(speak_output)
                 .response
         )



class StateIntentHandler(AbstractRequestHandler):
#     """Handler for Hello World Intent."""
     print("BEGIN STATE")
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool

         return is_intent_name("StateIntent")(
            handler_input)
     def handle(self, handler_input):
          print("INSIDE")
#          # type: (HandlerInput) -> Response
          global stateChosen
          stateChosen = get_slot_value(handler_input=handler_input, slot_name="state")
          if stateChosen:
            speech_text = "You live in {}!".format(stateChosen) +" "+ "Now for the next step say open medical file"
          else:
            speech_text = "Hello! I'm sorry, I don't yet know the state you live in."

          return handler_input.response_builder.speak(speech_text).response


class operationIntentHandler(AbstractRequestHandler):
#     """Handler for Hello World Intent."""
     print("BEGIN SURGERY")
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool

         return is_intent_name("operationIntent")(
            handler_input)
     def handle(self, handler_input):
          print("INSIDE SURGERY")
#          # type: (HandlerInput) -> Response
          global surgeryChosen
          surgeryChosen = get_slot_value(handler_input=handler_input, slot_name="surgery")
          if surgeryChosen:
            speech_text = "Medical condition picked is , {}".format(surgeryChosen)+" "+ " and the state chosen is "+" " +stateChosen+ " "+". Say Find Cost if you would like me to look up the price of your procedure"

          else:
            speech_text = "Hello! I'm sorry, I don't yet know the surgery you plan to have."

          return handler_input.response_builder.speak(speech_text).response


class CostIntentHandler(AbstractRequestHandler):
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool

          return is_intent_name("CostIntent")(
            handler_input)

     def handle(self, handler_input):
         # type: (HandlerInput) -> Response
          print ("INSIDE S3 DATA BLOCK")
          try:
             global CostCalculated
             global DisplayCost
             data = s3.get_object(Bucket=bucket, Key=key)
             json_data = data['Body'].read().decode("utf-8")
             json_data_indexable = ast.literal_eval(json_data)
             price = "Not Available"
             for i in range(len(json_data_indexable)):
                 if(json_data_indexable[i]["State"] == stateChosen and json_data_indexable[i]["procedure"] == surgeryChosen):
                     price = "Cost of your procedure is"+ " "+ json_data_indexable[i]["Payment"]
        # return "Price for "+surgeryChosen+"="+ price
            #  CostCalculated = json_data_indexable[0]['Payment']
            #  DisplayCost = 'Your '+surgeryChosen+" at "+stateChosen+" seems to cost" + CostCalculated
            #  return handler_input.response_builder.speak(DisplayCost).response
             return handler_input.response_builder.speak(price+ " "+ ". Hope that helped. You can say Ask medcalc to restart another procedure or Good bye").response
          except Exception as e:
             print(e)
             raise e


class heartTransplantIntentHandler(AbstractRequestHandler):
#     """Handler for Hello World Intent."""
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool
         return ask_utils.is_intent_name("heartTransplantIntent")(handler_input)
     def handle(self, handler_input):
         # type: (HandlerInput) -> Response
         surgeryChosen = str(intent['slots']['surgery']['value'])
         heart= 'Well, a '+surgeryChosen+' costs approximately $200,000 in '+ stateChosen;

         return handler_input.response_builder.speak(
             prompt).ask(prompt).add_directive(
             ElicitSlotDirective(slot_to_elicit=surgery.name)
             ).response

class HelpIntentHandler(AbstractRequestHandler):
#     """Handler for Help Intent."""
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool
         return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)
     def handle(self, handler_input):
         # type: (HandlerInput) -> Response
         speak_output = "I can help you find the price of medical treatments. Please say help me"

         return (
             handler_input.response_builder
                 .speak(speak_output)
                 .ask(speak_output)
                 .response
         )


class CancelOrStopIntentHandler(AbstractRequestHandler):
#     """Single handler for Cancel and Stop Intent."""
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool
         return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                 ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))
     def handle(self, handler_input):
         # type: (HandlerInput) -> Response
         speak_output = "Goodbye!"

         return (
             handler_input.response_builder
                 .speak(speak_output)
                 .response
         )


class SessionEndedRequestHandler(AbstractRequestHandler):
#     """Handler for Session End."""
     def can_handle(self, handler_input):
         # type: (HandlerInput) -> bool
         return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

     def handle(self, handler_input):
         # type: (HandlerInput) -> Response
         # Any cleanup logic goes here.
         return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):
#     """Generic error handling to capture any syntax or routing errors. If you receive an error
#    stating the request handler chain is not found, you have not implemented a handler for
#     the intent being invoked or included it in the skill builder below.
#     """
     def can_handle(self, handler_input, exception):
         # type: (HandlerInput, Exception) -> bool
         return True

     def handle(self, handler_input, exception):
         # type: (HandlerInput, Exception) -> Response
         logger.error(exception, exc_info=True)

         speak_output = "Sorry, I had trouble doing what you asked. Please try again."

         return (
             handler_input.response_builder
                 .speak(speak_output)
                 .ask(speak_output)
                 .response
         )


# # The SkillBuilder object acts as the entry point for your skill, routing all request and response
# # payloads to the handlers above. Make sure any new handlers or interceptors you've
# # defined are included below. The order matters - they're processed top to bottom.

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
#sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(StateIntentHandler())
sb.add_request_handler(CostIntentHandler())
sb.add_request_handler(operationIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())

#sb.add_request_handler(heartTransplantHandler())
sb.add_request_handler(SessionEndedRequestHandler())
#sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
