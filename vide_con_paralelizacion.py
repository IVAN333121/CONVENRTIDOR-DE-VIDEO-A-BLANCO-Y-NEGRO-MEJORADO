import cv2
import numpy as np
import os
import time

CARPETA = "D:\MARIO"
VIDEO_ORIGEN = "mario.mp4"
VIDEO_SALIDA = "blanco_negro.mp4"

ANCHO_SALIDA = 1920
ALTO_SALIDA = 1080
FPS_SALIDA = 30


TIEMPO_ESPERADO_POR_FOTOGRAMA = 0.005  
FACTOR_PENALIZACION = 2.0              


ruta_entrada = os.path.join(CARPETA, VIDEO_ORIGEN)
ruta_resultado = os.path.join(CARPETA, VIDEO_SALIDA)

print("=" * 60)
print(" Ruta de entrada:", ruta_entrada)
print(" Ruta de salida:", ruta_resultado)
print("=" * 60)


if not os.path.exists(ruta_entrada):
    print(f" ERROR: No se encontró el video en:\n   {ruta_entrada}")
    print("\n Solución: Pon el video en D:/ con el nombre VID_1.mp4")
    exit()


cap = cv2.VideoCapture(ruta_entrada)
if not cap.isOpened():
    print(" No se pudo abrir el video. Verifica el formato.")
    exit()


fps_original = cap.get(cv2.CAP_PROP_FPS)
ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_fotogramas = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print("\n INFORMACIÓN DEL VIDEO")
print(f" Original: {ancho}  {alto}")
print(f" FPS: {fps_original:.1f}")
print(f" Total fotogramas: {total_fotogramas}")
print(f" Duración aprox: {total_fotogramas / fps_original / 60:.2f} min")
print(f" Salida: {ANCHO_SALIDA}  {ALTO_SALIDA} @ {FPS_SALIDA} FPS")
print("=" * 60)

# Tiempo estimado
tiempo_estimado_total = total_fotogramas * TIEMPO_ESPERADO_POR_FOTOGRAMA
print(f" Tiempo estimado: {tiempo_estimado_total:.2f} segundos")
print(" Iniciando procesamiento...\n")

# Preparar salida
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(
    ruta_resultado, fourcc, FPS_SALIDA,
    (ANCHO_SALIDA, ALTO_SALIDA), False
)

# Variables de control
contador = 0
tiempo_inicio_proceso = time.time()
penalizacion_total = 0.0
retrasos = []

while True:
    tiempo_inicio_cuadro = time.time()
    
    ret, cuadro = cap.read()
    if not ret:
        break

    # Procesar
    cuadro_redim = cv2.resize(
        cuadro, (ANCHO_SALIDA, ALTO_SALIDA),
        interpolation=cv2.INTER_CUBIC
    )
    gris = cv2.cvtColor(cuadro_redim, cv2.COLOR_BGR2GRAY)
    out.write(gris)

    # Calcular tiempo y penalización
    tiempo_fin_cuadro = time.time()
    tiempo_real = tiempo_fin_cuadro - tiempo_inicio_cuadro
    
    if tiempo_real > TIEMPO_ESPERADO_POR_FOTOGRAMA:
        retraso = tiempo_real - TIEMPO_ESPERADO_POR_FOTOGRAMA
        penalizacion = retraso * FACTOR_PENALIZACION
        penalizacion_total += penalizacion
        retrasos.append(retraso)
    else:
        penalizacion = 0.0

    contador += 1
    if contador % 100 == 0:
        print(f" {contador}/{total_fotogramas} | Penalización acumulada: {penalizacion_total:.4f} s")

# Cerrar archivos
cap.release()
out.release()
cv2.destroyAllWindows()

tiempo_total = time.time() - tiempo_inicio_proceso


print("\n" + "=" * 60)
print(" PROCESAMIENTO FINALIZADO")
print("=" * 60)
print(f" Fotogramas procesados: {contador}")
print(f" Tiempo real total: {tiempo_total:.2f} segundos")
print(f" Tiempo estimado:     {tiempo_estimado_total:.2f} segundos")
print(f" Diferencia:          {tiempo_total - tiempo_estimado_total:.2f} segundos")
print(f" PENALIZACIÓN TOTAL:   {penalizacion_total:.4f} segundos")

if retrasos:
    print(f" Fotogramas con retraso: {len(retrasos)} de {contador}")
    print(f" Retraso máximo:       {max(retrasos):.4f} s")
    print(f" Retraso promedio:     {sum(retrasos)/len(retrasos):.4f} s")
else:
    print(" Sin retrasos detectados — dentro del tiempo esperado")

# Calificación
if penalizacion_total == 0:
    nota = "EXCELENTE  — Sin penalización"
elif penalizacion_total < 5:
    nota = "BUENA  — Penalización baja"
elif penalizacion_total < 20:
    nota = "REGULAR  — Penalización moderada"
else:
    nota = "DEFICIENTE  — Penalización alta"

print(f"\n CALIFICACIÓN: {nota}")
print(f" Archivo guardado: {ruta_resultado}")
print("=" * 60)