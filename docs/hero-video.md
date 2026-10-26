# Hero de video

El original de Magnific se conserva en `assets/hero/jhg-unlock.mp4`: H.264, 864 × 496, 24 fps, 5,04 segundos y 3,8 MB. No se amplía ni recodifica. Streamlit lo sirve con su reproductor nativo y soporte de rangos; no se incrusta en base64 ni se sirve como archivo estático genérico.

La primera bajada con el hero visible inicia la apertura sin sonido. También existe un botón accesible para iniciar o pausar. Se pausa fuera de pantalla o al ocultar la pestaña y continúa al regresar. Al terminar se muestra el fotograma final como imagen: el brillo permanece visible, sin reproducir de nuevo la apertura ni consumir reproducción continua. Es un estado final estático, no un bucle animado de estrellas.

El estado permanece en la ventana durante los cambios de filtros; una recarga completa lo reinicia. Con preferencia de movimiento reducido se muestra el fotograma final y solo se reproduce por una acción explícita. Si falla el video, permanece la imagen final. Si JavaScript no funciona, siguen disponibles los controles nativos.

El encuadre completo se adapta al ancho y a la altura de pantalla sin cortar el texto ni las tarjetas. `static/hero/closed.jpg` y `open.jpg` son fotogramas extraídos del original.

Comprobación manual: carga inicial pausada; bajar para iniciar; pausa y continuación; salida y regreso al hero; final persistente tras filtrar; recarga reinicia; vista móvil de 390 px sin desbordamiento.
