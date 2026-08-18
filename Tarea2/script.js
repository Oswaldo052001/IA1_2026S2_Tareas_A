/*
 Tarea #2 - Frontend (Fase 3)
 Oswaldo Antonio Choc Cuteres - 201901844

 Captura el item ingresado en el formulario, envia el dato al backend
 usando fetch (GET) de forma asincrona, y renderiza dinamicamente en
 el DOM la respuesta JSON: total de items, lista invertida, lista
 sin duplicados y lista ordenada con duplicados.
*/

const form = document.getElementById("form-busqueda");
const resultadoDiv = document.getElementById("resultado");
const errorDiv = document.getElementById("error");

// URL del backend Flask (Fase 2). Cambiar si se corre en otro host/puerto.
const API_URL = "http://127.0.0.1:5000/inventario";

form.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const item = document.getElementById("item-input").value.trim();
    errorDiv.textContent = "";
    resultadoDiv.innerHTML = "";

    if (!item) {
        errorDiv.textContent = "Por favor ingresa un item a buscar.";
        return;
    }

    try {
        // Envia el dato ingresado como query param al backend (GET)
        const respuesta = await fetch(`${API_URL}?item=${encodeURIComponent(item)}`);
        const datos = await respuesta.json();

        if (!respuesta.ok) {
            errorDiv.textContent = datos.error || "Ocurrio un error en el servidor.";
            return;
        }

        renderizarResultado(datos);
    } catch (err) {
        errorDiv.textContent =
            "No se pudo conectar con el backend. Verifica que este corriendo en http://127.0.0.1:5000";
    }
});

function renderizarResultado(datos) {
    resultadoDiv.innerHTML = `
        <h3>Resultados para: "${datos.item_buscado}"</h3>
        <p><strong>Total de items (length/2):</strong> ${datos.total_items}</p>

        <h4>Inventario invertido (reverse/2)</h4>
        <ul>${datos.inventario_invertido.map(i => `<li>${i}</li>`).join("")}</ul>

        <h4>Inventario sin duplicados (sort/2)</h4>
        <ul>${datos.inventario_unico.map(i => `<li>${i}</li>`).join("")}</ul>

        <h4>Inventario ordenado, con duplicados (msort/2)</h4>
        <ul>${datos.inventario_ordenado.map(i => `<li>${i}</li>`).join("")}</ul>
    `;
}
