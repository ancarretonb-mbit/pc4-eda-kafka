# PC4 – Arquitectura Basada en Eventos con Kafka y Redis

Proyecto de consolidación de conocimientos de Arquitecturas Basadas en Eventos (EDA).

El sistema implementa una arquitectura event-driven usando Kafka como bus de eventos y Redis como almacenamiento de estado derivado, incluyendo idempotencia y manejo de errores mediante Dead Letter Queue (DLQ).

## Caso de uso

Plataforma de eventos de usuario que procesa acciones como clicks y compras en tiempo casi real.
Los eventos se generan de forma continua, se publican en Kafka y se procesan de manera asíncrona para mantener agregados de negocio por usuario.

## Arquitectura

La arquitectura se basa en los siguientes componentes:

- Producer Python: genera eventos JSON simulando acciones de usuarios.
- Kafka: actúa como log distribuido y canal de eventos (pub/sub).
- Consumer Python: procesa eventos de forma asíncrona.
- Redis: almacena estado derivado (contadores y acumulados).
- Dead Letter Queue (DLQ): topic Kafka para eventos que no pueden procesarse.

## Diagrama de arquitectura

![Architecture](Architecture.png)

## Flujo de eventos

1. El producer genera eventos JSON y los publica en el topic `user-events`.
2. Kafka almacena los eventos y los distribuye a los consumidores.
3. El consumer:
   - Valida y deserializa los eventos.
   - Aplica idempotencia usando Redis.
   - Actualiza estado agregado en Redis.
   - Envía eventos fallidos a la DLQ.
4. Redis mantiene el estado derivado de forma incremental.

## Idempotencia y manejo de errores

- Idempotencia:
  - Se utiliza el campo `event_id`.
  - Redis almacena los IDs de eventos ya procesados.
  - Los duplicados se descartan sin afectar al estado.

- Manejo de errores:
  - Eventos inválidos o con errores de procesamiento se envían a un topic DLQ (`user-events-dlq`).
  - El sistema continúa procesando sin caerse.

## Decisiones técnicas

- Kafka se utiliza como bus de eventos por su modelo de log distribuido y soporte de consumer groups.
- Redis se emplea como almacenamiento de estado derivado por su baja latencia y operaciones atómicas.
- El procesamiento sigue un modelo at-least-once con idempotencia para garantizar consistencia.
- Se implementa una Dead Letter Queue (DLQ) para aislar eventos problemáticos sin detener el sistema.

## Escalabilidad

La arquitectura permite escalar horizontalmente los consumidores mediante particiones de Kafka y consumer groups, manteniendo el desacoplamiento entre productores y consumidores.


## Ejecución

### Producer
```bash
python -m uv run python producer.py
```

### Consumer
```bash
python -m uv run python consumer.py
```
