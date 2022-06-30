# Agregar asistentes
# POST
# http://127.0.0.1:8000/api/v1.0/attendees_group/
# { file: "", name: "" }
# return {'ok': true, 201_CREATED}

# Eliminar grupo de asistentes
# DELETE
# http://127.0.0.1:8000/api/v1.0/attendees_group/{id_group_attendees}/delete_group_attendees/
# return 204_NO_CONTENT

# Crear evento
# POST
# http://127.0.0.1:8000/api/v1.0/events/
# {
#     "name": "Congreso FEMEG",
#     "place": "Santa Ana",
#     "start_date": "2022-07-20",
#     "finish_date": "2022-07-23",
#     "total_hours": 150,
#     "count_trade_show_hours": false,
#     "aforo": 256,
#     "attendees_group": 72
# }
# return { id: 1, ..., 201_CREATED }

# Obtener grupos de asistentes
# GET
# http://127.0.0.1:8000/api/v1.0/attendees_group/
# return [
#     {
#         "id": 72,
#         "name": "FEMECOT",
#         "total": 33
#     }
# ], 200_OK

# Obtener lista de eventos
# GET
# http://127.0.0.1:8000/api/v1.0/events/
# return [
#     {
#         "id": 3,
#         "name": "Congreso FEMEG",
#         "group_users": 72,
#         "place": "Santa Ana",
#         "date": "2022-07-23",
#         "not_hours": true,
#         "count_trade_show_hours": false
#     }
# ], 200_OK

# Crear un salon
# POST
# http://127.0.0.1:8000/api/v1.0/lounge/
# {
#     "name": "Salon 5",
#     "aforo": 30,
#     "attendees_group": 72
# }
# return {
#     "id": 9,
#     "name": "Salon 5",
#     "aforo": 30,
#     "aforo_current": 0,
#     "attendees": []
# }, 201_CREATED

# Obtener salones por grupo
# GET
# http://127.0.0.1:8000/api/v1.0/lounge/{id_group}/get_for_group/
# return [
#     {
#         "id": 8,
#         "name": "Salon 1",
#         "aforo_current": 0,
#         "aforo": 30
#     }
# ], 200_OK

# Agregar a un asistente a un salon
# POST
# http://127.0.0.1:8000/api/v1.0/attendees/add_lounge/
# {
#     "id_attendee": 386,
#     "id_lounge": 9
# }
# return {"ok": true}, 204_NO_CONTENT

# Obtener lista de asistentes con salon
# GET
# http://127.0.0.1:8000/api/v1.0/attendees_group/{id_group}/get_attends_with_lounge/
# return [
#     {
#         "id": 386,
#         "name": "MARÍA DE JESÚS",
#         "lounge": "FEMECOT"
#     }
# ], 200_OK

# Crear operadores
# POST
# http://127.0.0.1:8000/api/v1.0/operators/
# {
#     "name": "Yoel",
#     "id_lounge": 9,
#     "id_event": 1
# }
# return {"ok": True}, 201_CREATED

# Eliminar operador
# DELETE
# http://127.0.0.1:8000/api/v1.0/operators/{id_operator}/
# return 204_NO_CONTENT

# Actualizar salon de operadores
# PUT
# http://127.0.0.1:8000/api/v1.0/operators/{id_operator}/update_lounge/
# {
#     "id_lounge": 8
# }
# return 204_NO_CONTENT

# Marcar entrada de un asistente
#   - Aumentar el aforo de el salon asignado
#   - Actualizar el salon en caso de cambio
# PUT
# http://127.0.0.1:8000/api/v1.0/attendees/{id_qr_attendee}/entry_mark/
# {
#     "id_event": 3,
#     "id_operator": 10
# }
# return {
#     "ok": true,
#     "detail": "Entrada marcada con exito"
# }

# Marcar salida de un asistente
#   - Disminuir el aforo de el salon asignado
# http://127.0.0.1:8000/api/v1.0/attendees/{id_qr_attendee}/exit_mark/
# {
#     "id_event": 3,
#     "id_operator": 10
# }
# return {
#     "ok": true,
#     "detail": "Salida marcada con exito"
# }

# Obtener informacion del operador 
# GET
# http://127.0.0.1:8000/api/v1.0/operators/{id_operator}/get_data/
# return 

# Obtener lista de asistentes
# Solicitud dentro del grupo de asistentes
# {
#     id: int,
#     id_qr: int,
#     name: string,
# }
# GET
# http://127.0.0.1:8000/api/v1.0/attendees/{id_group}/get_attendees_for_group/
# return {
#     "ok": true,
#     "attendees": [{...}, {...}]
# }

# Agregar usuarios anonimos
# POST
# http://127.0.0.1:8000/api/v1.0/attendees/add_anonymous_attendee/
# {
#     'id_qr': int
# }
# return {
#     "ok": true,
#     "id_attendee": 400
# }, 200_OK

# Obtener aforo total si se eligio "No contabilizar horas" (Por evento)
# GET
# http://127.0.0.1:8000/api/v1.0/events/{id_event}/get_total_aforo/
# return {
#     "aforo_current": int,
#     "aforo_total": int
# }

# Obtener lista de asistentes con (Por evento):
#   - Horas totales
#   - Horas cubiertas
#   - Horas restantes
# GET
# http://127.0.0.1:8000/api/v1.0/events/{id_event}/get_attendees/
# return [{
#     'id': int,
#     'name': str,
#     'id_qr': int,
#     'total_hours': int,
#     'hours_covered': int,
#     'hours_left': int
# }], 200_OK

# Obtener (Por evento)
#   - Aforo
#   - Asistentes
#   - Entradas totales
#   - Salidas totales
#   - Codigos no usados
# GET
# http://127.0.0.1:8000/api/v1.0/events/{id_event}/get_statistics/
# return {
#     "aforo": 256,
#     "asistentes": 34,
#     "entradas_totales": 6,
#     "salidas_totales": 5,
#     "codigos_no_usados": 33
# }

# Obtener el evento asignado al operador
# GET
# http://127.0.0.1:8000/api/v1.0/operators/{id_operator}/get_event/
# return {
#     "id": 3,
#     "name": "Congreso FEMEG",
#     "group_users": str,
#     "place": "Santa Ana",
#     "date": "2022-07-23",
#     "not_hours": true,
#     "count_trade_show_hours": false,
# }

# yoel64
# eVzwm0