Sistema de Recomendación de Aprendizaje con IA Explicable_

> Un sistema de recomendación de aprendizaje personalizado que utiliza IA Explicable (XAI) para mejorar la enseñanza de las matemáticas en la educación secundaria.

📝 Sobre el Proyecto

Este repositorio contiene el prototipo de un sistema de recomendación enfocado en crear rutas de aprendizaje personalizadas para estudiantes de secundaria en el área de matemáticas. A través de un enfoque híbrido de recomendación y el uso de Inteligencia Artificial Explicable (XAI), el sistema no solo sugiere contenido relevante, sino que también explica el porqué de sus recomendaciones, buscando aumentar la confianza del usuario y la efectividad del proceso de aprendizaje.

✨ Características

    🤖 Motor de Recomendación Híbrido: Combina filtrado colaborativo y basado en contenido para sugerencias precisas.

    🧠 IA Explicable (XAI): Ofrece transparencia sobre las sugerencias del sistema utilizando técnicas como SHAP y LIME.

    📊 Rutas de Aprendizaje Dinámicas: Adapta los contenidos y ejercicios al progreso individual de cada estudiante.

    💻 Interfaz Intuitiva: UI/UX diseñada para ser amigable tanto para estudiantes como para educadores.

💻 Tech Stack

Este proyecto está construido con las siguientes tecnologías:

  Frontend:

  * React
  * Vite

  Backend:

  * Python

  Base de Datos:

  * PostgreSQL / MySQL
  *  Docker

  Machine Learning:

  * Scikit-learn
  * TensorFlow / PyTorch

🚀 Getting Started

Para obtener una copia local y ponerla en marcha, sigue estos sencillos pasos.

Prerrequisitos

Asegúrate de tener instaladas las siguientes herramientas en tu sistema: node y npm

    npm install npm@latest -g

    python 3.8+

    docker y docker-compose

Instalación

    Clona el repositorio
    Bash

    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio

Inicia la Base de Datos con Docker
Este comando levantará el servicio de la base de datos. El script init.sql se ejecutará automáticamente para configurar el esquema inicial y las tablas.
Bash

    docker-compose up -d

# Configura el Backend (Python)
Bash

Navega al directorio del backend

    cd backend/
    
Crea y activa un entorno virtual

    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

Instala las dependencias

    pip install -r requirements.txt

Ejecuta el servidor

    python run.py

# Configura el Frontend (React + Vite)
Bash

Desde la raíz, navega al directorio del frontend

    cd frontend/

Instala las dependencias

    npm install

Inicia el servidor de desarrollo

    npm run dev

Tu aplicación estará disponible en http://localhost:5173.
