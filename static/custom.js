$(document).ready(function() {
    // Agregar el controlador de eventos click al botón Limpiar
    $("#clear_button").click(function() {
        // Limpiar la conversación y el contexto
        $("#console").empty();
        // Mostrar la notificación "Contexto limpiado"
        $("#clear-context").fadeIn();
        // Ocultar la notificación "Contexto limpiado" después de 3 segundos
        setTimeout(function() {
            $("#clear-context").fadeOut();
        }, 3000);
        $.get("/clear")
    });
    // Agregar el controlador de eventos click al botón de envío
    $("#send_button").click(function() {
        send();
    });
    // Agregar el controlador de eventos keypress al input de texto
    $("#user_input").keypress(function(event) {
        if (event.which === 13) {
            send();
        }
    });

    // Agregar evento de clic al botón de retroalimentación
    $(document).on("click", ".feedback-btn", function() {
        // Establecer el texto de la respuesta del bot en el modal emergente
        $("#feedback-modal-label").text("Proporcionar retroalimentación para: " + $("#question-cache").val());
    });

    // Agregar evento de clic al botón de enviar retroalimentación
    $("#btn-submit-feedback").click(function() {
        var msg = $("#expected-response").val();
        var tmp = $("#question-cache").val();
        if (msg) {
            $.get("/feedback", { msg, tmp }, function(data) {
                $("#expected-response").val('');
            });
        }
        $("#feedback-modal").modal("hide");
    });
});

function send() {
    var consoleOutput = document.getElementById("console");
    // Obtener el valor del input
    var msg = $("#user_input").val();
    $("#console").append("<p><b>&gt;&gt;</b> " + msg + "</p>");
    // Enviar una solicitud HTTP POST a Flask utilizando $.get()
    $.get("/get", { msg }, function(data) {
        // Mostrar la respuesta del bot en la página web
        $(".feedback-btn").remove();
        consoleOutput.innerHTML += "<p><b>&gt; " + data + '</b> <button type="button" class="btn btn-sm btn-outline-secondary feedback-btn" data-toggle="modal" data-target="#feedback-modal"> <i class="fas fa-comment"></i></button></p> ';
        consoleOutput.scrollTop = consoleOutput.scrollHeight;
    });
    $("#question-cache").val(msg);
    $("#user_input").val("");
};