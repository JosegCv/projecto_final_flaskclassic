# My Wallet Lite

My Wallet Lite es una sencilla aplicación web construida con Flask que permite a los usuarios hacer un seguimiento de sus inversiones en criptomonedas y ver un resumen de su cartera.

## Características

- Agregar, actualizar transacciones de criptomonedas.
- Ver el valor actual de cada criptomoneda en Euros basado en los tipos de cambio en tiempo real.
- Calcular la inversión total y el valor de la cartera en Euros.
- Almacenar las transacciones de criptomonedas en una base de datos SQLite para persistencia de datos.

## Requisitos

Para ejecutar esta aplicación, necesitas tener las siguientes dependencias instaladas:

- Python 3.6 o superior
- Flask
- Requests

Puedes instalar todas las dependencias necesarias utilizando el archivo `requirements.txt`. Simplemente ejecuta el siguiente comando:

pip install -r requirements.txt

2.Configura las variables de entorno creando un archivo `.env` en el directorio principal. El archivo `.env` debe contener la siguiente información:

SECRET_KEY="lolailo" (dejalo asi mon, ahora lolailo sera mi clave para todo)
FLASK_APP="main.py" 
FLASK_DEBUG="True" # Establece en "False" para producción
FLASK_API_KEY="tu_api_key_aqui"
FLASK_PATH_SQLITE=la direccion de tu base de datos (se recomienda usar "data/" seguido del nombre de la base de datos deseada para  asi se mantener un orden con las base de datos deseada)

**Nota:** Reemplaza `tu_api_key_aqui` con tu clave API real para los tipos de cambio de criptomonedas.

## Uso

Para iniciar la aplicación, utiliza el siguiente comando:
flask run

La aplicación estará disponible en `http://127.0.0.1:5000/` en tu navegador web.

## Cómo utilizar

1. Abre la aplicación web en tu navegador.
2. Usa los formularios proporcionados para agregar o actualizar transacciones de criptomonedas.
3. La aplicación obtendrá los tipos de cambio en tiempo real para calcular el valor actual de tus criptomonedas en Euros.
4. Verás un resumen de tu cartera, incluyendo la inversión total y el valor de la cartera en Euros.

