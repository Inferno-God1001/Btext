import builtins
import random
import time
import sys
import threading
from functools import partial

_original_print = builtins.print
_original_input = builtins.input

class ColorPrint:
    """Classe avançada para impressão colorida com múltiplas cores e animações"""
    
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
    def _get_color_code(cls, color):
        """Obtém o código ANSI para a cor especificada"""
        if color.startswith('random_'):
            base_colors = color[7:].split('_')
            valid_colors = [c for c in base_colors if c in cls.COLORS]
            if not valid_colors:
                valid_colors = list(cls.COLORS.keys())
            return partial(cls._random_color, colors=valid_colors)
        elif color == 'random':
            return partial(cls._random_color, colors=list(cls.COLORS.keys()))
        return cls.COLORS.get(color.lower(), cls.COLORS['white'])
    
    @classmethod
    def _random_color(cls, text, colors):
        """Aplica cores aleatórias a cada caractere"""
        return ''.join(
            f"{cls.COLORS[random.choice(colors)]}{char}{cls.COLORS['reset']}"
            for char in text
        )
    
    @classmethod
    def _animate_text(cls, text, color_func, direction='left', delay=0.1):
        """Cria efeito de animação para o texto"""
        delay = cls._parse_delay(delay)
        if direction == 'left':
            for i in range(len(text) + 1):
                sys.stdout.write('\r' + color_func(text[:i]))
                sys.stdout.flush()
                time.sleep(delay)
            print()
        else:  # right
            for i in range(len(text), 0, -1):
                sys.stdout.write('\r' + ' '*(len(text)-i) + color_func(text[-i:]))
                sys.stdout.flush()
                time.sleep(delay)
            print()
    
    @classmethod
    def _parse_delay(cls, delay):
        """Converte delay em segundos (aceita '3s' ou '50ms')"""
        if isinstance(delay, (int, float)):
            return delay
        if 'ms' in delay:
            return float(delay.replace('ms', '')) / 1000
        return float(delay.replace('s', ''))
    
    @classmethod
    def print(cls, *args, color='white', animation=False, direction='left', delay='0.1s', **kwargs):
        """Print avançado com suporte a múltiplas cores e animações"""
        segments = []
        colors = []
        current_text = []
        current_color = color
        
        # Processa argumentos para detectar mudanças de cor
        for arg in args:
            if isinstance(arg, str):
                if '+color=' in arg:
                    parts = arg.split('+color=')
                    current_text.append(parts[0])
                    segments.append(''.join(current_text))
                    colors.append(current_color)
                    current_text = []
                    current_color = parts[1]
                else:
                    current_text.append(arg)
            else:
                current_text.append(str(arg))
        
        if current_text:
            segments.append(''.join(current_text))
            colors.append(current_color)
        
        # Constrói o texto colorido
        colored_text = []
        for seg, col in zip(segments, colors):
            color_code = cls._get_color_code(col)
            if callable(color_code):
                colored_text.append(color_code(seg))
            else:
                colored_text.append(f"{color_code}{seg}{cls.COLORS['reset']}")
        
        final_text = ''.join(colored_text)
        
        # Animação
        if animation:
            color_func = lambda x: cls._get_color_code(color)(x) if not callable(cls._get_color_code(color)) else cls._get_color_code(color)(x)
            cls._animate_text(final_text, color_func, direction, delay)
        else:
            _original_print(final_text, **kwargs)
    
    @classmethod
    def input(cls, prompt='', color='white'):
        """Input colorido"""
        color_code = cls._get_color_code(color)
        if callable(color_code):
            prompt = color_code(prompt)
        else:
            prompt = f"{color_code}{prompt}{cls.COLORS['reset']}"
        return _original_input(prompt)
    
    @classmethod
    def restore_all(cls):
        """Restaura as funções originais"""
        builtins.print = _original_print
        builtins.input = _original_input

# Substitui as funções built-in
builtins.print = ColorPrint.print
builtins.input = ColorPrint.input