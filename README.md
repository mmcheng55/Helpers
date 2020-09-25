# Helpers
This is some useful function to use. You can check example or check Wiki tab for more.<br>

> **Commanders**
```python
import helpers.Commander

command = Commander("!")

@command()
def ping():
    print("Pong!")

command.run("!ping")
```