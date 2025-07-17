import builtins
import random
import time
import sys
from functools import partial

_original_print = builtins.print
_original_input = builtins.input

class ColorPrint:
    """Classe para impressão colorida com animações funcionais"""
    
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
    
    @staticmethod
    def _parse_delay(delay):
        """Converte delay para segundos"""
        if isinstance(delay, (int, float)):
            return delay
        if isinstance(delay, str):
            if 'ms' in delay:
                return float(delay.replace('ms', '')) / 1000
            return float(delay.replace('s', ''))
        return 0.1
    
    @classmethod
    def _get_color_func(cls, color):
        """Retorna função de coloração baseada na especificação"""
        if color.startswith('random_'):
            colors = color[7:].split('_')
            valid_colors = [c for c in colors if c in cls.COLORS]
            if not valid_colors:
                valid_colors = list(cls.COLORS.keys())
            
            def func(text):
                return ''.join(f"{cls.COLORS[random.choice(valid_colors)]}{c}{cls.COLORS['reset']}" for c in text)
            return func
        
        if color == 'random':
            def func(text):
                return ''.join(f"{cls.COLORS[random.choice(list(cls.COLORS.keys()))]}{c}{cls.COLORS['reset']}" for c in text)
            return func
        
        color_code = cls.COLORS.get(color.lower(), cls.COLORS['white'])
        return lambda text: f"{color_code}{text}{cls.COLORS['reset']}"
    
    @classmethod
    def _animate(cls, text, color_func, direction, delay):
        """Executa animação do texto"""
        delay_sec = cls._parse_delay(delay)
        if direction == 'left':
            for i in range(1, len(text)+1):
                sys.stdout.write('\r' + color_func(text[:i]))
                sys.stdout.flush()
                time.sleep(delay_sec)
            sys.stdout.write('\n')
        else:
            spaces = ' ' * len(text)
            for i in range(len(text)+1):
                sys.stdout.write('\r' + spaces[:len(text)-i] + color_func(text[-i:] if i > 0 else ''))
                sys.stdout.flush()
                time.sleep(delay_sec)
            sys.stdout.write('\n')
    
    @classmethod
    def print(cls, *args, **kwargs):
        """Print com cores e animação funcionais"""
        color = kwargs.pop('color', 'white')
        animation = kwargs.pop('animation', False)
        direction = kwargs.pop('direction', 'left')
        delay = kwargs.pop('delay', '0.1s')
        
        # Processa todos os argumentos como texto
        text = ' '.join(str(arg) for arg in args)
        
        # Remove marcadores de cor se existirem
        text = text.replace('+color=', '')
        
        color_func = cls._get_color_func(color)
        colored_text = color_func(text)
        
        if animation:
            cls._animate(text, color_func, direction, delay)
        else:
            _original_print(colored_text, **kwargs)
    
    @classmethod
    def input(cls, prompt='', color='white'):
        """Input colorido funcional"""
        color_func = cls._get_color_func(color)
        colored_prompt = color_func(prompt)
        return _original_input(colored_prompt)
    
    @classmethod
    def restore(cls):
        """Restaura funções originais"""
        builtins.print = _original_print
        builtins.input = _original_input

# Substitui as funções built-in
builtins.print = ColorPrint.print
builtins.input = ColorPrint.input