function getRowInfo(obj) {
    let elementId = obj.attr('id')
    return { "scriptName": obj.data('name'), "elementId": elementId, "genericId": elementId.split('-')[2] }
}

$(document).ready(function () {
    let colCounter = 0
    $(".is-log").on("click", function () {
        let data = getRowInfo($(this))

        $("#log-title").html(": " + data["scriptName"]);

        let code = ""

        $.ajax("/log/" + data["scriptName"]).done(function (logs) {
            $.each(logs["result"], (key, value) => {
                if (colCounter % 4 == 0)
                    code += '<div class="row">'

                code += '<div class="col-lg-3">' + key + ' '

                if (value == true)
                    code += ' <i class="fas fa-check" style="color: green"></i>'

                else
                    code += ' <i class="fas fa-times" style="color:red"></i>'

                code += '</div>'
                colCounter++

                if (colCounter % 4 == 0)
                    code += '</div>'
            })
            $("#log-data").html(code);
        })
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

        if ($("#is-run-" + data["genericId"]).hasClass('is-hide'))
            $.ajax("/delete/" + data["scriptName"] + "/0").fail(() => { error = 1 })

        else
            $.ajax("/delete/" + data["scriptName"] + "/1").fail(() => { error = 1 })

        if (!error)
            $("#row-" + data["genericId"]).addClass('is-hide')
    });

    $("#is-update").on("click", function () {
        console.log($('#server-data').serialize())
    });

    $("#is-refresh").on("click", function () {
        $.ajax("/status").done(function (status) {

            if ($("#server-up-text").hasClass('is-hide') == true && status["result"]["online"] == true) {
                $("#server-up-text").removeClass('is-hide')
                $("#server-up-icon").removeClass('is-hide')
                $("#server-down-text").addClass('is-hide')
                $("#server-down-icon").addClass('is-hide')
                $('button[id^=is-run').prop('disabled', false);
            }

            else if (($("#server-down-text").hasClass('is-hide') == true && status["result"]["online"] == false)) {
                $("#server-down-text").removeClass('is-hide')
                $("#server-down-icon").removeClass('is-hide')
                $("#server-up-text").addClass('is-hide')
                $("#server-up-icon").addClass('is-hide')
                $('button[id^=is-run').prop('disabled', true);
            }
        });
    });
});