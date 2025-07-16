import builtins

_original_print = builtins.print
_original_input = builtins.input

class ColorPrint:
    
    COLORS = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m'
    }
    
    @classmethod
    def print(cls, *args, color='white', **kwargs):
        color_code = cls.COLORS.get(color.lower(), cls.COLORS['white'])
        text = ' '.join(str(arg) for arg in args)
        _original_print(f"{color_code}{text}{cls.COLORS['reset']}", **kwargs)
    
    @classmethod
    def input(cls, prompt='', color='white'):
        """Substitui a função input padrão com suporte a cores"""
        color_code = cls.COLORS.get(color.lower(), cls.COLORS['white'])
        colored_prompt = f"{color_code}{prompt}{cls.COLORS['reset']}"
        return _original_input(colored_prompt)
    
    @classmethod
    def restore_all(cls):
        builtins.print = _original_print
        builtins.input = _original_input

builtins.print = ColorPrint.print
builtins.input = ColorPrint.input