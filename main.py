from pynput import keyboard

# String para acumular os caracteres do código
barcode_buffer = []


def on_press(key):
    try:
        # Verifica se a tecla é um caractere alfanumérico
        if hasattr(key, 'char') and key.char is not None:
            barcode_buffer.append(key.char)

        # O leitor USB geralmente envia a tecla 'Enter' ao final
        elif key == keyboard.Key.enter:
            codigo_completo = "".join(barcode_buffer)
            if codigo_completo:
                processar_dados(codigo_completo)
                barcode_buffer.clear()  # Limpa para a próxima leitura

    except Exception as e:
        print(f"Erro: {e}")


def processar_dados(codigo):
    print(f"Processando código: {codigo}")
    # Aqui entra sua lógica de Data Science ou integração com Saúde


print("Ouvindo o leitor USB em segundo plano...")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
