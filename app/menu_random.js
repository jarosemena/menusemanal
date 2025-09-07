const fs = require('fs');

// Variables globales
let selfdesayunos = null;
let selfalmuerzos = null;
let selfcenas = null;
let selfmenu_anterior = [];
let selfidsemana = "";
let selffecha_lunes = new Date();

// Estructura para tracking de restricciones
let selfproteinas_recientes = [];
let selfcomplementos_almuerzos = new Set();
let selfcomplementos_cenas = new Set();
let selfcomplementos_desayunos = new Set();

function defineVariables(desayunos, almuerzos, cenas, menu_anterior, idsemana, fecha_lunes) {
    selfdesayunos = desayunos;
    selfalmuerzos = almuerzos;
    selfcenas = cenas;
    selfmenu_anterior = menu_anterior || [];
    selfidsemana = idsemana;
    selffecha_lunes = fecha_lunes;
}

function _filtrarPorRepeticion(opciones, tipo_comida, dia) {
    /**
     * Filtra opciones que no estén en el menú anterior mismo día
     */
    if (!selfmenu_anterior || selfmenu_anterior.length === 0) {
        return opciones;
    }
    
    // Obtener código del mismo día semana anterior
    let codigo_anterior = null;
    if (tipo_comida === 'desayuno') {
        codigo_anterior = selfmenu_anterior[dia]?.CodigoDesayuno;
    } else if (tipo_comida === 'almuerzo') {
        codigo_anterior = selfmenu_anterior[dia]?.CodigoAlmuerzo;
    } else if (tipo_comida === 'cena') {
        codigo_anterior = selfmenu_anterior[dia]?.CodigoCena;
    }
    
    return opciones.filter(op => op.id !== codigo_anterior);
}

function _filtrarProteinaReciente(opciones) {
    /**
     * Filtra opciones que rompan la regla de 3 días consecutivos misma proteína
     */
    if (selfproteinas_recientes.length < 2) {
        return opciones;
    }
    
    // Obtener últimas 2 proteínas
    const ultimas_proteinas = new Set(selfproteinas_recientes.slice(-2));
    if (ultimas_proteinas.size === 1) {
        const proteina_repetida = Array.from(ultimas_proteinas)[0];
        return opciones.filter(op => op.Proteina !== proteina_repetida);
    }
    return opciones;
}

function _seleccionarOpcion(opciones, tipo_comida, dia) {
    /**
     * Selecciona una opción validando todas las restricciones
     */
    // Filtrar por repetición semana anterior
    let opciones_filtradas = _filtrarPorRepeticion(opciones, tipo_comida, dia);
    
    // Filtrar por proteínas recientes
    opciones_filtradas = _filtrarProteinaReciente(opciones_filtradas);
    
    // Filtrar por complementos únicos esta semana
    if (tipo_comida === 'almuerzo') {
        opciones_filtradas = opciones_filtradas.filter(op => !selfcomplementos_almuerzos.has(op.Complemento));
    } else if (tipo_comida === 'cena') {
        opciones_filtradas = opciones_filtradas.filter(op => !selfcomplementos_cenas.has(op.Complemento));
    } else if (tipo_comida === 'desayuno') {
        opciones_filtradas = opciones_filtradas.filter(op => !selfcomplementos_desayunos.has(op.Complemento));
    }
    
    if (opciones_filtradas.length === 0) {
        // Relajar restricciones de complementos si no hay opciones
        return opciones[Math.floor(Math.random() * opciones.length)];
    }
    
    return opciones_filtradas[Math.floor(Math.random() * opciones_filtradas.length)];
}

function diaAIndiceSimple(dia_texto, dias_semana) {
    for (let i = 0; i < dias_semana.length; i++) {
        if (dias_semana[i].toLowerCase() === dia_texto.toLowerCase()) {
            return i;
        }
    }
    return 0;
}

function addDays(date, days) {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
}

function generarMenuSemanal() {
    // Reset trackers
    selfproteinas_recientes = [];
    selfcomplementos_almuerzos = new Set();
    selfcomplementos_cenas = new Set();
    selfcomplementos_desayunos = new Set();

    const menu = [];
    const dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];
    
    // Almuerzos especiales (solo 3 únicos)
    const almuerzos_base = [];
    const indices_aleatorios = [];
    while (indices_aleatorios.length < 3) {
        const random_index = Math.floor(Math.random() * selfalmuerzos.length);
        if (!indices_aleatorios.includes(random_index)) {
            indices_aleatorios.push(random_index);
        }
    }
    indices_aleatorios.forEach(index => almuerzos_base.push(selfalmuerzos[index]));
    
    for (let i = 0; i < dias_semana.length; i++) {
        const dia = dias_semana[i];
        
        // Determinar patrones de repetición
        if (['Miércoles', 'Jueves', 'Sábado'].includes(dia)) {
            // Usar mismo menú que el día correspondiente
            const menu_duplicado = i >= 2 ? { ...menu[i-2] } : null;
            if (menu_duplicado) {
                menu_duplicado.DiaSemana = dia;
                const daystosum = diaAIndiceSimple(dia, dias_semana);
                menu_duplicado.Fecha = daystosum > 0 ? addDays(selffecha_lunes, daystosum) : selffecha_lunes;
                menu.push(menu_duplicado);
                continue;
            }
        }

        // Seleccionar desayuno
        const desayuno = _seleccionarOpcion(selfdesayunos, 'desayuno', i);
        
        // Seleccionar almuerzo según día
        let almuerzo;
        if (['Lunes', 'Miércoles'].includes(dia)) {
            almuerzo = almuerzos_base[0];
        } else if (['Martes', 'Jueves'].includes(dia)) {
            almuerzo = almuerzos_base[1];
        } else if (['Viernes', 'Sábado'].includes(dia)) {
            almuerzo = almuerzos_base[2];
        } else { // Domingo
            almuerzo = _seleccionarOpcion(selfalmuerzos, 'almuerzo', i);
        }
        
        // Seleccionar cena
        const cena = _seleccionarOpcion(selfcenas, 'cena', i);
        
        // Actualizar trackers
        selfproteinas_recientes.push(desayuno.Proteina);
        selfproteinas_recientes.push(almuerzo.Proteina);
        selfproteinas_recientes.push(cena.Proteina);
        
        selfcomplementos_almuerzos.add(almuerzo.Complemento);
        selfcomplementos_cenas.add(cena.Complemento);
        selfcomplementos_desayunos.add(desayuno.Complemento);
        
        // Mantener solo últimos 6 días de proteínas (2 días completos)
        if (selfproteinas_recientes.length > 6) {
            selfproteinas_recientes = selfproteinas_recientes.slice(-6);
        }
        
        const daystosum = diaAIndiceSimple(dia, dias_semana);
        console.log(`daystosum = ${daystosum}`);
        
        const fecha = daystosum > 0 ? addDays(selffecha_lunes, daystosum) : selffecha_lunes;
        
        if (dia === "Domingo") {
            menu.push({
                IDSemana: selfidsemana,
                Fecha: fecha,
                DiaSemana: dia,
                CodigoDesayuno: 0,
                DescDesayuno: "LIBRE",
                CodigoAlmuerzo: 0,
                DescAlmuerzo: "LIBRE",
                CodigoCena: 0,
                DescCena: "LIBRE"
            });
        } else {
            menu.push({
                IDSemana: selfidsemana,
                Fecha: fecha,
                DiaSemana: dia,
                CodigoDesayuno: desayuno.id,
                DescDesayuno: desayuno.Descripcion,
                CodigoAlmuerzo: almuerzo.id,
                DescAlmuerzo: almuerzo.Descripcion,
                CodigoCena: cena.id,
                DescCena: cena.Descripcion
            });
        }
    }
    
    return menu;
}

function loadData(path) {
    const rawData = fs.readFileSync(path, 'utf8');
    const data = JSON.parse(rawData);

    // Caso 1: [{ "data": [...] }]
    if (Array.isArray(data) && data.length > 0 && typeof data[0] === 'object' && data[0].data) {
        return data[0].data;
    }

    // Caso 2: {"data": [...]}
    if (typeof data === 'object' && data.data) {
        return data.data;
    }

    // Caso 3: lista directa de objetos
    if (Array.isArray(data)) {
        return data;
    }

    throw new Error(`Formato inesperado en ${path}: ${typeof data}`);
}

function getData(json_string) {
    const data = JSON.parse(json_string);

    // Caso 1: [{ "data": [...] }]
    if (Array.isArray(data) && data.length > 0 && typeof data[0] === 'object' && data[0].data) {
        return data[0].data;
    }

    // Caso 2: {"data": [...]}
    if (typeof data === 'object' && data.data) {
        return data.data;
    }

    // Caso 3: lista directa de objetos
    if (Array.isArray(data)) {
        return data;
    }

    throw new Error(`Formato inesperado en json_string: ${typeof data}`);
}

function runNode() {
    const desayunos = loadData("desayunos.json");
    const almuerzos = loadData("almuerzos.json");
    const cenas = loadData("cenas.json");
    const menu_anterior = loadData("menu_anterior.json");
    const fecha_lunes = new Date('2025-09-01');
    
    defineVariables(desayunos, almuerzos, cenas, menu_anterior, '2025-36', fecha_lunes);

    const menu_semanal = generarMenuSemanal();
    return menu_semanal;
}

function runInN8n() {
    // Implementación para n8n (comentada como en el original)
    // const desayunos = getData($input.first().json.data);
    // const almuerzos = getData($input.first().json.data);
    // const cenas = getData($input.first().json.data);
    // const menu_anterior = loadData("menu_anterior.json");
    // const fecha_lunes = new Date($('Aggregate').first().json.data[3]['Fecha del siguiente lunes']);
    // defineVariables(desayunos, almuerzos, cenas, menu_anterior, $('Aggregate').first().json.data[4]['Código de semana'], fecha_lunes);
    // const menu_semanal = generarMenuSemanal();
    // return menu_semanal;
    return null;
}

// Ejecutar y mostrar resultado
const menu_semanal = runNode();

// Imprimir resultado
menu_semanal.forEach(dia => {
    console.log(`${dia.DiaSemana}:`);
    console.log(`  ID_Semana: ${dia.IDSemana}`);
    console.log(`  Fecha: ${dia.Fecha}`);
    console.log(`  Desayuno: ${dia.DescDesayuno}`);
    console.log(`  Almuerzo: ${dia.DescAlmuerzo}`);
    console.log(`  Cena: ${dia.DescCena}`);
    console.log();
});

// Exportar funciones para uso como módulo
/*
module.exports = {
    defineVariables,
    generarMenuSemanal,
    loadData,
    getData,
    runNode,
    runInN8n
};
*/