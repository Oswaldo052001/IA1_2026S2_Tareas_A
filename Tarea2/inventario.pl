% ==========================================================
% Tarea #2 - Laboratorio Inteligencia Artificial 1 - Seccion A
% Oswaldo Antonio Choc Cuteres - 201901844
% Universidad de San Carlos de Guatemala - FIUSAC
%
% Motor de inferencia en Prolog: manejo de listas para el
% inventario de un aventurero de RPG.
% ==========================================================


% ----------------------------------------------------------
% 1. HECHOS
% ----------------------------------------------------------

% items_principales/1
% Lista de al menos 4 items del aventurero.
% Incluye un item duplicado a proposito (pocion aparece 2 veces)
% para poder demostrar despues la diferencia entre sort/2 (unico)
% y msort/2 (conserva duplicados).
items_principales([espada, pocion, escudo, pocion]).

% items_secundarios/1
% Lista de al menos 3 items distintos (sin duplicados) del aventurero.
items_secundarios([antorcha, cuerda, llave]).


% ----------------------------------------------------------
% 2. PREDICADO RECURSIVO DE RECORRIDO
% ----------------------------------------------------------

% mostrar_inventario/1
% Aridad 1: recibe una lista de items y la imprime en consola
% recorriendola de forma recursiva.

% Caso base: cuando la lista esta vacia, ya no hay nada que
% imprimir, solo se marca el fin del recorrido.
mostrar_inventario([]) :-
    format("-- Fin del inventario --~n").

% Caso recursivo: desestructura la lista en Cabeza (primer item)
% y Cola (resto de la lista), imprime la Cabeza y se llama a si
% mismo con la Cola, hasta llegar al caso base.
mostrar_inventario([Cabeza|Cola]) :-
    format(" -> Item: ~w~n", [Cabeza]),
    mostrar_inventario(Cola).


% ----------------------------------------------------------
% 3. REGLA PRINCIPAL DE PROCESAMIENTO
% ----------------------------------------------------------

% procesar_inventario/5
% Aridad 5: recibe un ItemBuscado (entrada) y devuelve por
% unificacion 4 variables de salida: TotalItems, InventarioInvertido,
% InventarioUnico e InventarioOrdenado.
procesar_inventario(ItemBuscado, TotalItems, InventarioInvertido, InventarioUnico, InventarioOrdenado) :-

    items_principales(Principales),
    items_secundarios(Secundarios),

    % append/3 (aridad 3): concatena la lista de items principales
    % con la de items secundarios en una sola lista general.
    append(Principales, Secundarios, InventarioGeneral),

    % length/2 (aridad 2): cuenta cuantos elementos tiene el
    % inventario general y lo unifica con TotalItems.
    length(InventarioGeneral, TotalItems),

    % reverse/2 (aridad 2): invierte el orden del inventario
    % general y lo unifica con InventarioInvertido.
    reverse(InventarioGeneral, InventarioInvertido),

    % sort/2 (aridad 2): ordena el inventario general Y elimina
    % los duplicados, unificando el resultado con InventarioUnico.
    sort(InventarioGeneral, InventarioUnico),

    % msort/2 (aridad 2): ordena el inventario general pero SI
    % conserva los duplicados, unificando con InventarioOrdenado.
    msort(InventarioGeneral, InventarioOrdenado),

    % member/2 (aridad 2): verifica si el ItemBuscado pertenece
    % al inventario general e informa el resultado por consola.
    (   member(ItemBuscado, InventarioGeneral)
    ->  format("El item '~w' SI esta en el inventario~n", [ItemBuscado])
    ;   format("El item '~w' NO esta en el inventario~n", [ItemBuscado])
    ),

    % Ultima instruccion de la regla: se llama al predicado
    % recursivo para imprimir todos los items del inventario
    % general en la consola del servidor.
    mostrar_inventario(InventarioGeneral).
