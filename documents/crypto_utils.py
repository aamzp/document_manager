from Crypto.PublicKey import RSA

# Generar claves RSA (clave privada y clave pública)
def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    # Guardar las claves en archivos
    with open("private.pem", "wb") as priv_file:
        priv_file.write(private_key)

    with open("public.pem", "wb") as pub_file:
        pub_file.write(public_key)

    print("Claves generadas y guardadas en 'private.pem' y 'public.pem'")

# Ejecutar la función una sola vez para generar las claves
if __name__ == "__main__":
    generate_keys()