import command_handlers
import event_handlers

from handlers import register

command_handlers_registry = register(command_handlers)
event_handlers_registry = register(event_handlers)

for name, handler in command_handlers_registry.items(): print(name, handler)
for name, handler in event_handlers_registry.items(): print(name, handler)