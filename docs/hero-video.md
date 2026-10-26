# Hero y carga del portafolio

## Comportamiento

El video avanza con el desplazamiento (scroll scrubbing). Una sección sticky conserva el hero visible durante un recorrido de 1,8 alturas de pantalla, con un mínimo de 700 px. El progreso llega al 100 % antes de liberar el hero; se añaden 120 px para contemplar el resultado. No se interceptan la rueda ni los gestos táctiles.

La posición del scroll determina el fotograma en ambas direcciones, incluso después de completar la apertura. Al volver al hero desde las apps, subir lo cierra progresivamente; al bajar vuelve a abrirse. Los cambios de filtros conservan el fotograma correspondiente a la posición actual. El botón «Saltar animación» lleva directamente a las experiencias. Con movimiento reducido o fallo del video se muestra la composición final sin recorrido adicional. Sin JavaScript quedan los controles nativos y el flujo normal de la página.

La sección ocupa todo el ancho disponible y el alto de la pantalla bajo la barra de Streamlit. El header propio se superpone. El encuadre conserva texto y tarjetas sin recortarlos; se centra y amplía dentro de esta sección. Una capa ambiental muy desenfocada rellena el fondo y las máscaras de varios pasos producen un desvanecido más amplio en todos los bordes. No se altera el arte original ni se añade otra descarga de video.

## Recursos servidos

- Portadas originales: 24.117.513 bytes en PNG.
- Las 18 variantes WebP de 960 px: 973.044 bytes en total (96 % menos).
- Las 18 variantes WebP de 640 px: 529.756 bytes en total. El navegador selecciona una variante mediante `srcset` y `sizes`; no descarga ambas por defecto. Se mantiene la carga diferida.
- Video original: 3.832.807 bytes.
- Video de scroll: 1.427.967 bytes (63 % menos), H.264, 864 × 496, 24 fps, sin audio, fotograma clave cada seis frames, sin B-frames y cabecera MP4 al comienzo. Esto facilita saltar entre tiempos sin descargar/decodificar largos grupos de frames.
- Los originales se conservan como referencia; la página solicita las versiones optimizadas.

El MP4 usa el servicio nativo de medios de Streamlit con MIME `video/mp4` y respuestas parciales 206. Los WebP usan el servicio estático con MIME `image/webp`. CSS, scripts, iconos y bytes inmutables del hero se reutilizan en el servidor. No se envían portadas ni video en base64.

El scroll se procesa con un único `requestAnimationFrame` pendiente. Solo hay una búsqueda de fotograma en curso; al terminar se aplica el objetivo más reciente. La posición sticky la gestiona CSS. Al llegar al final se usa una imagen fija; al volver hacia arriba se retoma el video desde la posición del scroll. El observador del hero ignora cambios de texto y tarjetas mientras su video siga conectado.

## Verificación

Las pruebas cubren las 18 apps, búsqueda y filtros, tablero y presupuestos de peso/resolución de las portadas. Se comprueba además en navegador la fijación del hero, progreso parcial/final, salida hacia la colección, persistencia tras filtrar y vista móvil de 390 px. Las cifras anteriores son tamaños de recursos, no una promesa de segundos de carga: la conexión y el arranque de Streamlit Cloud también influyen.
