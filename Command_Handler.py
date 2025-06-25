from telegram.ext import CommandHandler 

registered_plugins = []

def plugin(command_name, description):
    def decorator(func):
        registered_plugins.append({
            'command': command_name,
            'description': description,
            'handler': CommandHandler(command_name, func)
        })
        return func
    return decorator

def get_handlers():
    return [item['handler'] for item in registered_plugins]

def get_help_text():
    return "\n".join(
        f"/{item['command']} - {item['description']}" for item in registered_plugins
    )
