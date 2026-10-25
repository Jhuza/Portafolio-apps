# Portadas y movimiento · JHG

Las 18 portadas aprobadas se sirven desde `static/covers/`: ChatPDF v2 y las 17 ilustraciones de cristal. Cada PNG conserva sus 1659 × 948 píxeles (7:4). `projects.json` relaciona cada app con su archivo. Las ilustraciones representan funciones; no son evidencia de resultados de los modelos.

`server.enableStaticServing` permite cargarlas mediante `app/static/covers/…`. Se usan carga diferida, decodificación asíncrona y dimensiones explícitas: las imágenes no se incluyen en base64 en cada actualización de filtros. Las portadas SVG anteriores se conservan como material de diseño.

`portfolio_motion.js` observa la entrada de tarjetas, encabezados, textos y controles en pantalla. Aplica un desplazamiento de 14 px y un fundido de 540 ms, con un escalonado máximo de 90 ms. Cada nodo se anima una sola vez; los elementos nuevos que aparecen tras filtrar se registran de nuevo. El contenido está visible por defecto y sigue accesible si JavaScript no se ejecuta.

Cuando el encabezado sale de su posición original, la misma navegación pasa a una superficie flotante de cristal oscuro. Se reserva su altura original para evitar saltos, se coloca debajo de la barra de Streamlit y se reajusta al cambiar el ancho. Al volver al inicio recupera su posición normal. La entrada dura 340 ms. En móvil mantiene dos filas compactas y enlaces visibles.

`prefers-reduced-motion: reduce` desactiva las entradas, el desplazamiento suave y los efectos de hover. Un cambio de preferencia cancela también las animaciones activas. El código JavaScript es local y fijo: no interpola texto del usuario ni carga scripts externos. Se limpian observadores y eventos al reinstalarlo durante una actualización de Streamlit.

Validación local: tres pruebas existentes aprobadas; 18 archivos distintos con proporción exacta 7:4; revisión visual de escritorio y de 390 px; navegación flotante, regreso al inicio, anclas y búsqueda OCR comprobados. Sin desbordamiento horizontal en móvil.

Referencias: [HTML con JavaScript en Streamlit](https://docs.streamlit.io/develop/api-reference/text/st.html) y [archivos estáticos](https://docs.streamlit.io/develop/concepts/configuration/serving-static-files).
