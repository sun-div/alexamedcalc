const Alexa = require('ask-sdk-core');
const https = require('https');

var stateChosen='';
var surgeryChosen='';

const LaunchRequestHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'LaunchRequest';
  },
  handle(handlerInput) {

    const speakOutput = 'Welcome! Please say ask med what state you live in?';

    return handlerInput.responseBuilder
      .speak(speakOutput)
      .getResponse();
  },
};

const StateIntentHandler = {
  canHandle(handlerInput) {

    return handlerInput.requestEnvelope.request.type === 'IntentRequest'
      && handlerInput.requestEnvelope.request.intent.name === 'StateIntent'
      &&  handlerInput.requestEnvelope.request.intent.slots.state.value;
  },
  handle(handlerInput) {
     stateChosen = handlerInput.requestEnvelope.request.intent.slots.state.value;

    var speakOutput = stateChosen+" is a cool state. What surgery are you planning to have?";

     return handlerInput.responseBuilder
        .addElicitSlotDirective("state")
        .speak(speakOutput)

//        .reprompt(speakOutput)

        .getResponse();

  },
};

const SurgeryIntentHandler = {
  canHandle(handlerInput) {

    return handlerInput.requestEnvelope.request.type === 'IntentRequest'
      && handlerInput.requestEnvelope.request.intent.name === 'SurgeryIntent'
      &&  handlerInput.requestEnvelope.request.intent.slots.surgery.value;
  },
  handle(handlerInput) {
     surgeryChosen = handlerInput.requestEnvelope.request.intent.slots.surgery.value;

    var speakOutput = surgeryChosen+" is the procedure you are scheduled for."+" "+"This is to be performed in"+" "+stateChosen+
    " Ask me what the cost  of"+" " + surgeryChosen+ " " + "is!";

     return handlerInput.responseBuilder
        .addElicitSlotDirective("surgery")
        .speak(speakOutput)

//        .reprompt(speakOutput)

        .getResponse();

  },
};


const heartTransplantHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'IntentRequest'
      && handlerInput.requestEnvelope.request.intent.name === 'heartTransplantIntent';
  },
  handle(handlerInput) {
    const speakOutput = 'It costs an average of $121,547.5 for a'+ ' '+ surgeryChosen;

    return handlerInput.responseBuilder
      .speak(speakOutput)
      .getResponse();

  },
};


const HelpHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'IntentRequest'
      && handlerInput.requestEnvelope.request.intent.name === 'AMAZON.HelpIntent';
  },
  handle(handlerInput) {
    const speakOutput = 'You can ask me how much it costs for a medical procedure!';
    return handlerInput.responseBuilder
      .speak(speakOutput)
      .getResponse();
  },
};

const CancelAndStopHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'IntentRequest'
      && (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent'
        || handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent');
  },
  handle(handlerInput) {
    const speakOutput = 'Goodbye!';

    return handlerInput.responseBuilder
      .speak(speakOutput)
      .getResponse();
  },
};

const SessionEndedRequestHandler = {
  canHandle(handlerInput) {
    return handlerInput.requestEnvelope.request.type === 'SessionEndedRequest';
  },
  handle(handlerInput) {
    console.log(`Session ended with reason: ${handlerInput.requestEnvelope.request.reason}`);

    return handlerInput.responseBuilder.getResponse();
  },
};

const ErrorHandler = {
  canHandle() {
    return true;
  },
  handle(handlerInput, error) {
    console.log(`Error handled: ${error.message}`);
    console.log(error.trace);

    return handlerInput.responseBuilder
      .speak('Sorry, I can\'t understand the command. Please say again.')
      // .speak('try again')
      .getResponse();
  },
};

const skillBuilder = Alexa.SkillBuilders.custom();

exports.handler = skillBuilder
  .addRequestHandlers(
    LaunchRequestHandler,
    HelpHandler,
    StateIntentHandler,
    heartTransplantHandler,
    CancelAndStopHandler,
    SurgeryIntentHandler,
    SessionEndedRequestHandler,
    )
  .addErrorHandlers(ErrorHandler)
  .lambda();
