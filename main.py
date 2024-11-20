import gradio as gr
from cryptography.fernet import Fernet

# Generate key (CSPRNG)
KEY = Fernet.generate_key()
cipher_suite = Fernet(KEY)

# Encryption function
def encrypt_file(file):
    with open(file.name, "rb") as f:
        data = f.read()
    encrypted_data = cipher_suite.encrypt(data)
    encrypted_file = file.name + ".encrypted"
    with open(encrypted_file, "wb") as f:
        f.write(encrypted_data)
    return encrypted_file

# Decryption function
def decrypt_file(file):
    with open(file.name, "rb") as f:
        encrypted_data = f.read()
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        decrypted_file = file.name.replace(".encrypted", "")
        with open(decrypted_file, "wb") as f:
            f.write(decrypted_data)
        return decrypted_file
    except Exception as e:
        return f"Decryption failed: {str(e)}"

# Gradio UI
def create_ui():
    encrypt_interface = gr.Interface(
        fn=encrypt_file,
        inputs=gr.File(label="Upload a file to encrypt (e.g., .txt, .docx, etc.)"),
        outputs=gr.File(label="Encrypted file"),
        title="asyCrypt"
    )

    decrypt_interface = gr.Interface(
        fn=decrypt_file,
        inputs=gr.File(label="Upload an encrypted file to decrypt"),
        outputs=gr.File(label="Decrypted file"),
        title="File Decryption"
    )

    app = gr.TabbedInterface(
        interface_list=[encrypt_interface, decrypt_interface],
        tab_names=["Encrypt", "Decrypt"]
    )

    return app

if __name__ == "__main__":
    app = create_ui()
    app.launch()
