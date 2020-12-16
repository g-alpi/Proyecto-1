-- 1 Mostrar la Carta inicial más repetida por cada jugador(mostrar nombre jugador y carta). 
WITH MyRowSet
AS
(
select idparticipante,carta_inicial,count(carta_inicial) as "usos",ROW_NUMBER() OVER (PARTITION BY idparticipante) AS Primera_carta from turnos 
group by idparticipante,carta_inicial
) 
SELECT * FROM MyRowSet WHERE Primera_carta = 1;
-- 2 Jugador que realiza la apuesta más alta por partida. (Mostrar nombre jugador)
select nombre,max(apuesta),idpartida
from
(
select 
case 
when username is not null then usuario.username 
else descripcion 
end
as nombre,max(turnos.apuesta) as apuesta,partida.idpartida as idpartida from jugador
left join bot on bot.idbot=jugador.idbot
left join usuario on usuario.idusuario=jugador.idusuario
inner join participante on jugador.idjugador=participante.id_jugador
inner join turnos on participante.id_participante=turnos.idparticipante
inner join partida on turnos.idpartida=partida.idpartida
where turnos.apuesta is not null
group by partida.idpartida,username
) tabla
where (apuesta,idpartida) in (

select 
max(turnos.apuesta),partida.idpartida  as apuesta from jugador
left join bot on bot.idbot=jugador.idbot
left join usuario on usuario.idusuario=jugador.idusuario
inner join participante on jugador.idjugador=participante.id_jugador
inner join turnos on participante.id_participante=turnos.idparticipante
inner join partida on turnos.idpartida=partida.idpartida
group by partida.idpartida
order by max(turnos.apuesta) desc
)
group by idpartida;
-- 3 Jugador que realiza apuesta más baja por partida. (Mostrar nombre jugador)
select nombre,min(apuesta),idpartida
from
(
select 
case 
when username is not null then usuario.username 
else descripcion 
end
as nombre,min(turnos.apuesta) as apuesta,partida.idpartida as idpartida from jugador
left join bot on bot.idbot=jugador.idbot
left join usuario on usuario.idusuario=jugador.idusuario
inner join participante on jugador.idjugador=participante.id_jugador
inner join turnos on participante.id_participante=turnos.idparticipante
inner join partida on turnos.idpartida=partida.idpartida
where turnos.apuesta is not null
group by partida.idpartida,username
) tabla
where (apuesta,idpartida) in (

select 
min(turnos.apuesta),partida.idpartida  as apuesta from jugador
left join bot on bot.idbot=jugador.idbot
left join usuario on usuario.idusuario=jugador.idusuario
inner join participante on jugador.idjugador=participante.id_jugador
inner join turnos on participante.id_participante=turnos.idparticipante
inner join partida on turnos.idpartida=partida.idpartida
group by partida.idpartida
order by min(turnos.apuesta) desc
)
group by idpartida;
-- 4 Ratio de turnos ganados por jugador en cada partida (%),mostrar columna Nombre jugador, Nombre partida, nueva columna "porcentaje %"
SELECT p.nombre_sala, u.username as 'Usuario', COUNT(t.resultado)
FROM participante AS f
INNER JOIN turnos AS t
    ON f.id_jugador = t.idparticipante
INNER JOIN usuario AS u
    ON f.id_jugador = u.idusuario
LEFT JOIN partida AS p
    ON f.id_partida = p.idpartida
GROUP BY p.idpartida, idusuario;
-- 5 Porcentaje de partidas ganadas Bots en general. Nueva columna "porcentaje %"
select distinct bot.descripcion,partida.ganador_partida, truncate(((2/sum(partida.idpartida))*100),2) as porcentaje from partida inner join participante on partida.ganador_partida=participante.id_participante inner join jugador on participante.id_jugador=jugador.idjugador inner join bot on jugador.idbot=bot.idbot where bot.idbot is not null
-- 6 Mostrar los datos de los jugadores y el tiempo que han durado sus partidas ganadas cuya puntuación obtenida es mayor que la media puntos de las partidas ganadas totales.

-- 7 Cuántas rondas se ganan en cada partida según el palo. Ejemplo: Partida 1 - 5 rondas - Bastos como carta inicial.

-- 8 Cuantas rondas gana la banca en cada partida.
select count(t.idturnos), p.idpartida from turnos t
inner join partida p on p.idpartida = t.idpartida
where t.puntos_inicio-t.puntos_final < 0 and es_banca=1
group by idpartida;
-- 9 Cuántos usuarios han sido la banca en las partidas
select count(es_banca) as "Banca", p.idpartida from turnos t
inner join partida p on p.idpartida = t.idpartida
where es_banca=1
group by idpartida;
-- 10 Partida con la puntuación más alta final de todos los jugadores, mostrar nombre jugador, nombre partida,así como añadir una columna nueva en la que diga si ha ganado la partida o no.

-- 11 Calcular la apuesta media por partida.
select avg(t.apuesta) as "Media de las apuestas", p.idpartida from turnos t
inner join partida p on p.idpartida = t.idpartida
group by idpartida;
-- 12 Mostrar los datos de los usuarios que no son bot, así como cual ha sido su última apuesta en cada partida que ha jugado.
select distinct u.*,apuesta , max(t.numero_turno), pd.idpartida from usuario u 
inner join jugador j on u.idusuario = j.idusuario
inner join participante p on j.idjugador = p.id_jugador
inner join turnos t on p.id_participante = t.idparticipante
inner join partida pd on pd.idpartida = t.idpartida
group by idpartida,idparticipante
-- having numero_turno in  (select max(numero_turno) from turnos group by idpartida)
order by t.idpartida asc,idparticipante asc, numero_turno asc;
-- 13 Calcular el valor total de las cartas y el numero total de cartas que se han dado inicialmente en las manos en la partida. Por ejemplo, en la partida se han dado 50 cartas y el valor total de las cartas es 47,5.
select count(t.carta_inicial) as "Numero de cartas iniciales", sum((select valor from cartas where idcartas = t.carta_inicial)) as  "Valor de las cartas", p.idpartida from turnos t
inner join partida p on p.idpartida = t.idpartida
group by idpartida;
-- 14 Diferencia de puntos de los participantes de las partidas entre la ronda 1 y 5. Ejemplo: Rafa tenia 20 puntos, en la ronda 5 tiene 15, tiene -5 puntos de diferencia.
SELECT t.idpartida, u.username,(select distinct puntos_inicio from turnos where numero_turno=1) as 'Puntos_ronda_1',puntos_final, puntos_final-20 AS 'Diferencia' from usuario u 
inner join jugador j on u.idusuario = j.idusuario 
inner join participante p on j.idjugador = p.id_jugador 
inner join turnos t on p.id_participante = t.idparticipante 
where numero_turno=5 
group by t.idpartida, t.idparticipante 
order by t.idpartida asc, t.idparticipante asc;
