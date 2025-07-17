import random
from functools import partial

class TerminalColors:
    # Códigos ANSI para cores
    COLORS = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'orange': '\033[38;5;208m',
        'pink': '\033[38;5;213m',
        'reset': '\033[0m'
    }
    
    COLOR_NAMES = list(COLORS.keys())
    COLOR_NAMES.remove('reset')
    
    @classmethod
    def get_color_code(cls, color_name):
        color_name = color_name.lower().strip()
        if color_name in cls.COLORS:
            return cls.COLORS[color_name]
        return cls.COLORS['white']  # Default

def colored_print(*args, **kwargs):
    """
    Imprime texto colorido no terminal.
    
    Uso:
    print("cor bonita", color="Red")
    print("divisão de cor" + "cor bonita", color="Pink")
    print("divisão de cor", color="red" + "cor bonita", color="Orange")
    print("olá", color="Green" + "meu", color="Red" + "amigo!", color="Pink")
    print("colorido", color="Random")
    print("ooooooo", color="Green , Yellow , Blue , Yellow , Green")
    """
    color = kwargs.get('color', None)
    end = kwargs.get('end', '\n')
    
    # Caso especial para color="Random"
    if isinstance(color, str) and color.lower() == "random":
        color = random.choice(TerminalColors.COLOR_NAMES)
    
    # Se não houver especificação de cor, imprima normalmente
    if color is None:
        print(*args, end=end)
        return
    
    # Processa strings concatenadas com cores diferentes
    if isinstance(color, str) and ',' in color:
        color_parts = [c.strip() for c in color.split(',')]
        text_parts = []
        
        # Divide o texto em partes iguais ao número de cores
        for text in args:
            if isinstance(text, str):
                part_length = max(1, len(text) // len(color_parts))
                for i in range(len(color_parts)):
                    start = i * part_length
                    end_part = (i + 1) * part_length if i < len(color_parts) - 1 else len(text)
                    text_part = text[start:end_part]
                    color_code = TerminalColors.get_color_code(color_parts[i])
                    text_parts.append(f"{color_code}{text_part}")
        
        print(''.join(text_parts) + TerminalColors.COLORS['reset'], end=end)
        return
    
    # Processa múltiplos argumentos com cores diferentes
    color_args = []
    current_color = color
    
    for arg in args:
        if isinstance(arg, str) and arg.startswith('color='):
            current_color = arg[6:].strip('"\'')
        else:
            if isinstance(arg, str):
                color_code = TerminalColors.get_color_code(current_color)
                color_args.append(f"{color_code}{arg}")
    
    if color_args:
        print(''.join(color_args) + TerminalColors.COLORS['reset'], end=end)

def colored_input(*args, **kwargs):
    """
    Solicita entrada do usuário com texto colorido.
    
    Uso:
    input_color("Digite seu nome: ", color="Green")
    input_color("Pergunta 1", color="Blue" + "Pergunta 2", color="Yellow")
    input_color("Escolha: ", color="Random")
    """
    color = kwargs.get('color', None)
    
    # Caso especial para color="Random"
    if isinstance(color, str) and color.lower() == "random":
        color = random.choice(TerminalColors.COLOR_NAMES)
    
    # Se não houver especificação de cor, use input normal
    if color is None:
        return input(*args)
    
    # Processa strings concatenadas com cores diferentes
    if isinstance(color, str) and ',' in color:
        color_parts = [c.strip() for c in color.split(',')]
        text_parts = []
        
        # Divide o texto em partes iguais ao número de cores
        for text in args:
            if isinstance(text, str):
                part_length = max(1, len(text) // len(color_parts))
                for i in range(len(color_parts)):
                    start = i * part_length
                    end_part = (i + 1) * part_length if i < len(color_parts) - 1 else len(text)
                    text_part = text[start:end_part]
                    color_code = TerminalColors.get_color_code(color_parts[i])
                    text_parts.append(f"{color_code}{text_part}")
        
        return input(''.join(text_parts) + TerminalColors.COLORS['reset'])
    
    # Processa múltiplos argumentos com cores diferentes
    color_args = []
    current_color = color
    
    for arg in args:
        if isinstance(arg, str) and arg.startswith('color='):
            current_color = arg[6:].strip('"\'')
        else:
            if isinstance(arg, str):
                color_code = TerminalColors.get_color_code(current_color)
                color_args.append(f"{color_code}{arg}")
    
    if color_args:
        return input(''.join(color_args) + TerminalColors.COLORS['reset'])
    return input()

# Atalhos para facilitar o uso
print_color = colored_print
print_random = partial(colored_print, color="Random")
input_color = colored_input
input_random = partial(colored_input, color="Random")

# Exemplos de uso
if __name__ == "__main__":
    print("Exemplos de uso para print:")
    
    # Exemplos de print
    print_color("cor bonita", color="Red")
    print_color("divisão de cor" + "cor bonita", color="Pink")
    print_color("divisão de cor", color="red" + "cor bonita", color="Orange")
    print_color("olá", color="Green" + " meu", color="Red" + " amigo!", color="Pink")
    print_color("colorido", color="Random")
    print_color("ooooooo", color="Green , Yellow , Blue , Yellow , Green")
    print_random("Este texto terá uma cor aleatória!")
    
    print("\nExemplos de uso para input:")
    
    # Exemplos de input
    nome = input_color("Digite seu nome: ", color="Green")
    print_color(f"Olá, {nome}!", color="Blue")
    
    idade = input_color("Digite sua idade: ", color="Yellow")
    print_color(f"Você tem {idade} anos.", color="Cyan")
    
    comida = input_color("Qual sua comida favorita?", color="Red" + " Digite: ", color="Blue")
    print_color(f"{comida} é uma ótima escolha!", color="Magenta")
    
    sonho = input_color("Qual seu maior sonho? ", color="Random")
    print_color(f"Espero que você realize seu sonho de {sonho}!", color="Pink")
    
    arte = input_color("A R T E", color="Red , Green , Yellow , Blue , Magenta")
    print_color(f"Você digitou: {arte}", color="Orange")