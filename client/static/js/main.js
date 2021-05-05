function getRowInfo(obj) {
    let elementId = obj.attr('id')
    return { "scriptName": obj.data('name'), "elementId": elementId, "genericId": elementId.split('-')[2] }
}

$(document).ready(function () {
    $(".is-log").on("click", function () {
        let colCounter = 0
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
        let state = ["down", "up"];

        $.ajax("/status").done(function (status) {
            if ($("#server-up-text").hasClass('is-hide') == true && status["result"]["online"] == true) {
                preStatus = 0
                $('button[id^=is-run').prop('disabled', false);
            }

            else if (($("#server-down-text").hasClass('is-hide') == true && status["result"]["online"] == false)) {
                preStatus = 1
                $('button[id^=is-run').prop('disabled', true);
            }

            $("#server-" + state[1 - preStatus] + "-text").removeClass('is-hide')
            $("#server-" + state[1 - preStatus] + "-icon").removeClass('is-hide')
            $("#server-" + state[preStatus] + "-text").addClass('is-hide')
            $("#server-" + state[preStatus] + "-icon").addClass('is-hide')
        });
    });
});