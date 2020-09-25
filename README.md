# Helpers
This is some useful function to use. You can check example or check Wiki tab for more.<br>

Wiki page: [Wiki Page](https://github.com/mmcheng55/Helpers/wiki)
> **Commanders**
```python
import helpers.Commander

command = Commander("!")

@command()
def ping():
    print("Pong!")

command.run("!ping")
```
