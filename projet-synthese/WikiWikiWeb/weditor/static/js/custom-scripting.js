$(document).bind("mobileinit", function() {
    $.extend($.mobile, {
        ajaxEnabled: false,
        loadingMessage: "Chargement ...",
        pageLoadErrorMessage: "Erreur lors du chargement de la page",
    });
});