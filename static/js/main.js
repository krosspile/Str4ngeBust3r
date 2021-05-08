function getRowInfo(obj) {
    let elementId = obj.attr('id')
    return { "scriptName": obj.data('name'), "elementId": elementId, "genericId": elementId.split('-')[2] }
}

function refreshStatus() {
    let state = ["down", "up"];
    let preStatus

    $.ajax("/status").done((status) => {
        if ($("#server-up-text").hasClass('is-hide') == true && status["online"] == true) {
            preStatus = 0;
            $('button[id^=is-run').prop('disabled', false);
            $('button[id^=is-log').prop('disabled', false);
        }

        else if (($("#server-down-text").hasClass('is-hide') == true && status["online"] == false)) {
            preStatus = 1;
            $('button[id^=is-run').prop('disabled', true);
            $('button[id^=is-log').prop('disabled', true);
        }

        $("#server-" + state[1 - preStatus] + "-text").removeClass('is-hide');
        $("#server-" + state[1 - preStatus] + "-icon").removeClass('is-hide');
        $("#server-" + state[preStatus] + "-text").addClass('is-hide');
        $("#server-" + state[preStatus] + "-icon").addClass('is-hide');
    });
}

function refreshStats() {

    $.ajax("/stats").done((stats) => {
        let code = "";
        $.each(stats, (key, value) => {
            code += '<div class="row mt-2">';
            code += '<div class="col-lg-4">' + key + '</div>';
            $.each(value, (i, val) => {
                code += '<div class="col-lg-4" style="text-align: center">' + val + '</div>';
            });
            code += '</div>';
            $("#stats-data").html(code);
        });
    });
}

async function autoRefresh() {
    while (1) {
        refreshStatus();
        refreshStats();
        await new Promise(r => setTimeout(r, 60000));
    }
}

$(document).ready(() => {
    $(".is-log").on("click", function () {
        let colCounter = 0;
        let data = getRowInfo($(this));

        $("#log-title").html(": " + data["scriptName"]);

        let code = "";

        $.ajax("/log/" + data["scriptName"]).done(function (logs) {
            $.each(logs, (key, value) => {
                if (colCounter % 3 == 0)
                    code += '<div class="row">';

                code += '<div class="col-lg-2">' + key + '</div>';
                code += '<div class="col-lg-2">';
                if (value == true)
                    code += '<i class="fas fa-check" style="color: green"></i>';

                else
                    code += '<i class="fas fa-times" style="color:red"></i>';

                code += '</div>';
                colCounter++;

                if (colCounter % 3 == 0)
                    code += '</div>';
            });
            $("#log-data").html(code);
        });
    });

    $(".is-stop").on("click", () => {
        let data = getRowInfo($(this));
        $.ajax("/stop/" + data["scriptName"]).done(() => {
            $("#" + data["elementId"]).addClass('is-hide');
            $("#is-run-" + data["genericId"]).removeClass("is-hide");
            $("#is-log-" + data["genericId"]).addClass('is-hide');
        });
    });

    $(".is-run").on("click", () => {
        let data = getRowInfo($(this));
        $.ajax("/start/" + data["scriptName"]).done(() => {
            $("#" + data["elementId"]).addClass('is-hide');
            $("#is-stop-" + data["genericId"]).removeClass("is-hide");
            $("#is-log-" + data["genericId"]).removeClass('is-hide');
        });
    });

    $(".is-delete").on("click", function () {
        let data = getRowInfo($(this));
        let error = 0;

        if ($("#is-run-" + data["genericId"]).hasClass('is-hide'))
            $.ajax("/delete/" + data["scriptName"] + "/0").fail(() => { error = 1; });

        else
            $.ajax("/delete/" + data["scriptName"] + "/1").fail(() => { error = 1; });

        if (!error)
            $("#row-" + data["genericId"]).addClass('is-hide');
    });

    $("#is-update").on("click", function () {
        $('#server-data').serialize();
    });

    $("#is-refresh").on("click", function () {
        refreshStatus();
    });

    autoRefresh();
});