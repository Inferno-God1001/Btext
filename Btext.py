import builtins
import random
import time
import sys
import warnings

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
    def _get_color_func(cls, color_spec):
        """Retorna uma função que, dado um texto, retorna o texto colorido.
        
        Se color_spec for do tipo 'random' ou 'random_col1_col2', retorna uma função que aplica cores aleatórias por caractere.
        Caso contrário, retorna uma função que aplica a cor fixa.
        """
        if color_spec.startswith('random_'):
            base_colors = color_spec[7:].split('_')
            valid_colors = [c for c in base_colors if c in cls.COLORS]
            if not valid_colors:
                valid_colors = list(cls.COLORS.keys())
            def random_func(text):
                return ''.join(
                    f"{cls.COLORS[random.choice(valid_colors)]}{char}{cls.COLORS['reset']}"
                    for char in text
                )
            return random_func
        elif color_spec == 'random':
            def random_func(text):
                return ''.join(
                    f"{cls.COLORS[random.choice(list(cls.COLORS.keys()))]}{char}{cls.COLORS['reset']}"
                    for char in text
                )
            return random_func
        else:
            color_code = cls.COLORS.get(color_spec.lower(), cls.COLORS['white'])
            def fixed_func(text):
                return f"{color_code}{text}{cls.COLORS['reset']}"
            return fixed_func
    
    @classmethod
    def _parse_delay(cls, delay):
        if isinstance(delay, (int, float)):
            return delay
        if isinstance(delay, str):
            if delay.endswith('ms'):
                return float(delay[:-2]) / 1000
            elif delay.endswith('s'):
                return float(delay[:-1])
            else:
                return float(delay)
        return delay
    
    @classmethod
    def _animate_segment(cls, segment, color_func, direction, delay):
        """Anima um segmento de texto."""
        delay_sec = cls._parse_delay(delay)
        if direction == 'left':
            for i in range(1, len(segment)+1):
                # Aplica a cor ao subsegmento que está sendo animado
                colored_chunk = color_func(segment[:i])
                sys.stdout.write('\r' + colored_chunk)
                sys.stdout.flush()
                time.sleep(delay_sec)
            sys.stdout.write('\n')
        elif direction == 'right':
            # Para direita: começa vazio e vai preenchendo da direita para esquerda
            n = len(segment)
            for i in range(1, n+1):
                colored_chunk = color_func(segment[n-i:])
                sys.stdout.write('\r' + ' '*(n-i) + colored_chunk)
                sys.stdout.flush()
                time.sleep(delay_sec)
            sys.stdout.write('\n')
    
    @classmethod
    def print(cls, *args, **kwargs):
        # Extrai os parâmetros especiais
        color = kwargs.pop('color', 'white')
        animation = kwargs.pop('animation', False)
        direction = kwargs.pop('direction', 'left')
        delay = kwargs.pop('delay', '0.1s')
        
        # Processa os argumentos para construir segmentos
        segments = []
        current_segment = []
        current_color = color
        
        for arg in args:
            if isinstance(arg, str) and arg.startswith('+color='):
                # Encontrou uma mudança de cor
                new_color = arg[7:]
                # Adiciona o segmento atual
                if current_segment:
                    segments.append((''.join(current_segment), current_color))
                    current_segment = []
                current_color = new_color
            else:
                current_segment.append(str(arg))
        
        if current_segment:
            segments.append((''.join(current_segment), current_color))
        
        # Se não houver segmentos, sai
        if not segments:
            _original_print(**kwargs)
            return
        
        # Se animation estiver ativada, só pode ter um segmento
        if animation:
            if len(segments) > 1:
                warnings.warn("Animation is not supported for multi-color prints. Animation turned off.")
                animation = False
            else:
                text, color_spec = segments[0]
                color_func = cls._get_color_func(color_spec)
                cls._animate_segment(text, color_func, direction, delay)
                return
        
        # Caso contrário, constrói o texto colorido
        colored_text = []
        for seg, color_spec in segments:
            color_func = cls._get_color_func(color_spec)
            colored_text.append(color_func(seg))
        
        final_text = ''.join(colored_text)
        _original_print(final_text, **kwargs)
    
    @classmethod
    def input(cls, prompt='', color='white', **kwargs):
        color_func = cls._get_color_func(color)
        colored_prompt = color_func(prompt)
        return _original_input(colored_prompt, **kwargs)
    
    @classmethod
    def restore_all(cls):
        builtins.print = _original_print
        builtins.input = _original_input

builtins.print = ColorPrint.print
builtins.input = ColorPrint.input