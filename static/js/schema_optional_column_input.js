function toggleIntegerFieldsVisibility(selectElement, inputFrom, inputTo, labelFrom, labelTo) {
        if (selectElement.value === "integer") {
            inputFrom.type = "number"
            inputTo.type = "number"

            labelFrom.style.display = "inline"
            labelTo.style.display = "inline"
        } else {
            inputFrom.type = "hidden"
            inputTo.type = "hidden"

            labelFrom.style.display = "none"
            labelTo.style.display = "none"
        }
    }

function getIntegerInputAndLabels(columnForm) {
    const inputTo = columnForm.querySelector("input.column-integer_to")
    const inputFrom = columnForm.querySelector("input.column-integer_from")

    return [
        inputFrom,
        inputTo,
        document.querySelector(`label[for="${inputFrom.id}"]`),
        document.querySelector(`label[for="${inputTo.id}"]`)
    ]
}

function schemaOptionalColumnInputOnChange(element) {
    const columnForm = element.closest(".column-form")
    let [inputFrom, inputTo, labelFrom, labelTo] = getIntegerInputAndLabels(columnForm)

    toggleIntegerFieldsVisibility(element, inputFrom, inputTo, labelFrom, labelTo)
}


function schemaOptionalColumnInputOnReload() {
    let columnForms = document.getElementById("column-forms").querySelectorAll(".column-form")

    for (let i=0; i < columnForms.length; i++) {
        let selectType = columnForms[i].querySelector(`select#id_columns-${i}-type`)
        let [inputFrom, inputTo, labelFrom, labelTo] = getIntegerInputAndLabels(columnForms[i])

        toggleIntegerFieldsVisibility(selectType, inputFrom, inputTo, labelFrom, labelTo);
    }
}

window.addEventListener("load", function() {
    const update_path = /^\/schemas\/(\d+)\/update\/$/
    const create_path = "/schemas/create/"

    if (window.location.pathname === create_path || window.location.pathname.match(update_path)) {
        schemaOptionalColumnInputOnReload()
    }
});
