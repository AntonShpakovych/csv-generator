const PATH_SCRIPT = /^\/schemas\/(\d+)\/generate_csv\/$/


if (window.location.pathname.match(PATH_SCRIPT)) {
    $(document).ready(function() {
        function updateStatusAndActions(datasetPk) {
            $.ajax({
                url: `/schemas/datasets/${datasetPk}/status/`,
                method: "GET",
                dataType: "json",
                success: function(data) {
                    const MESSAGE_ACTIONS_AVAILABLE = "Download"
                    const MESSAGE_ACTIONS_UNAVAILABLE = "WAIT: We are processing your file!!!"
                    let infoBadge = $('.status[data-dataset-pk="' + datasetPk + '"] span');
                    let actionsBadge = $('.actions[data-dataset-pk="' + datasetPk + '"] span');

                    infoBadge.removeClass();
                    actionsBadge.removeClass();
                    actionsBadge.empty();

                    if (data.status === "processing"){
                        infoBadge.addClass("badge bg-secondary");
                        actionsBadge.text(MESSAGE_ACTIONS_UNAVAILABLE);
                        actionsBadge.addClass("badge bg-secondary");
                    } else {
                        let downloadLink = $("<a>", {
                            href: "/schemas/datasets/" + datasetPk + "/download-csv/",
                            text: MESSAGE_ACTIONS_AVAILABLE,
                            style: "color: white;"
                        });
                        actionsBadge.append(downloadLink);
                        actionsBadge.addClass("badge bg-success")
                        infoBadge.addClass("badge bg-success");
                    }

                    infoBadge.text(data.status);
                }
            });
        }

        $(".status").each(function() {
            var datasetPk = $(this).data("dataset-pk");
            updateStatusAndActions(datasetPk);
            setInterval(function() {
                updateStatusAndActions(datasetPk);
            }, 5000);
        });
    });
}
