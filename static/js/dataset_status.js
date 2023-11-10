const PATH_SCRIPT = /^\/schemas\/(\d+)\/generate_csv\/$/


if (window.location.pathname.match(PATH_SCRIPT)) {
    $(document).ready(function() {
        function updateStatus(datasetPk) {
            $.ajax({
                url: `/schemas/datasets/${datasetPk}/status/`,
                method: "GET",
                dataType: "json",
                success: function(data) {
                    let infoBadge = $('.status[data-dataset-pk="' + datasetPk + '"] span')
                    infoBadge.removeClass()
                    if (data.status === "processing"){
                        infoBadge.addClass("badge bg-secondary");
                    } else {
                        infoBadge.addClass("badge bg-success");
                    }

                    infoBadge.text(data.status)
                }
            });
        }

        $(".status").each(function() {
            var datasetPk = $(this).data("dataset-pk");
            updateStatus(datasetPk);
            setInterval(function() {
                updateStatus(datasetPk);
            }, 5000);
        });
    });
}
