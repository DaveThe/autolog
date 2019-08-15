
from PyInquirer import Token, style_from_dict

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


general_questions = [
    {
        'type': 'expand',
        'name': 'enviroment',
        'message': 'What kind of enviroment do you need?',
        'choices': [
            {
                'key': 'p',
                'name': 'run in car',
                'value': 'production'
            },
            {
                'key': 'd',
                'name': 'debug mode',
                'value': 'debug'
            }
        ]
    },
    {
        'type': 'confirm',
        'message': 'Do you want to pairing a new device?',
        'name': 'pairing',
        'default': False,
    },
    {
        'type': 'input',
        'name': 'port',
        'message': 'What\'s the obd port',
        'default': 'rfcomm0'
    }
]

continue_question = [
    {
        'type': 'confirm',
        'message': 'Do you want to continue?',
        'name': 'continue',
        'default': True,
    }]
exit_question = [
    {
        'type': 'confirm',
        'message': 'Do you want to exit?',
        'name': 'exit',
        'default': False,
    }]

retry_question = [
    {
        'type': 'confirm',
        'message': 'Do you want to retry?',
        'name': 'exit',
        'default': False,
    }]
