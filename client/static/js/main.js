function getRowInfo(obj) {
    let elementId = obj.attr('id')
    return { "scriptName": obj.data('name'), "elementId": elementId, "genericId": elementId.split('-')[2] }
}

$(document).ready(function () {
    $(".is-log").on("click", function () {
        let data = getRowInfo($(this))
        $("#log-window").html("<p>" + data["scriptName"] + "</p>");
    });

    $(".is-stop").on("click", function () {
        let data = getRowInfo($(this))
        $.ajax("/stop/" + data["scriptName"]).done(function () {
            $("#" + data["elementId"]).addClass('is-hide')
            $("#is-run-" + data["genericId"]).removeClass("is-hide")
            $("#is-log-" + data["genericId"]).addClass('is-hide')
        })
    });

    $(".is-run").on("click", function () {
        let data = getRowInfo($(this))
        $.ajax("/start/" + data["scriptName"]).done(function () {
            $("#" + data["elementId"]).addClass('is-hide')
            $("#is-stop-" + data["genericId"]).removeClass("is-hide")
            $("#is-log-" + data["genericId"]).removeClass('is-hide')
        })
    });

    $(".is-delete").on("click", function () {
        let data = getRowInfo($(this))
        let error = 0

        if ($("#is-run-" + data["genericId"]).hasClass('is-hide')) {
            $.ajax("/delete/" + data["scriptName"] + "/0").fail(() => { error = 1 })
        }
        else {
            $.ajax("/delete/" + data["scriptName"] + "/1").fail(() => { error = 1 })
        }

        if (!error) {
            $("#row-" + data["genericId"]).addClass('is-hide')
        }
    });
});